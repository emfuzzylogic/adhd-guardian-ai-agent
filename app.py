# app.py - Backend for the ADHD Agent (v2.7 - Reverted Syntax Fix)

import os
import uuid # For generating state values in auth flow
import requests
import json
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_session import Session # Import Flask-Session
from dotenv import load_dotenv
import msal # Import MSAL for Python
import datetime # For calculating date ranges for calendar view
import logging # Import logging library
import re # Import regular expressions for parsing

# Basic Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# --- Configuration ---
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = "2024-02-01"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = os.getenv("AUTHORITY", "https://login.microsoftonline.com/common")
REDIRECT_PATH = os.getenv("REDIRECT_PATH", "/getAToken")
DEFAULT_SCOPES = "User.Read Calendars.Read Tasks.Read email"
SCOPE = os.getenv("SCOPE", DEFAULT_SCOPES).split()

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-please-change")
GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0/'

# --- Config Checks ---
config_ok = True
if not all([CLIENT_ID, CLIENT_SECRET]):
    logging.error("Azure AD CLIENT_ID and CLIENT_SECRET environment variables not set.")
    config_ok = False
openai_config_missing = False
if not all([AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT_NAME]):
    logging.warning("Azure OpenAI environment variables (ENDPOINT, KEY, DEPLOYMENT_NAME) not set. AI features will fail.")
    openai_config_missing = True

# --- Flask App Initialization ---
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

# --- Jinja Filters ---
@app.template_filter('format_datetime')
def format_datetime(value, format='%Y-%m-%d %H:%M'):
    """Formats an ISO datetime string for display."""
    if not value: return ""
    try:
        dt_obj = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt_obj.strftime(format)
    except (ValueError, TypeError): return value

@app.template_filter('capitalize')
def capitalize_filter(s):
    """Capitalizes the first letter of a string."""
    return s.capitalize() if isinstance(s, str) else s

# --- MSAL Client Initialization ---
msal_app = None
if config_ok:
    try:
        msal_app = msal.ConfidentialClientApplication(
            CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
        )
    except Exception as e: logging.error(f"Failed to initialize MSAL client: {e}")
else: logging.error("Cannot initialize MSAL client due to missing configuration.")


# --- Helper Functions ---
def _build_auth_url(scopes=None, state=None):
    """Builds the URL for the authorization request."""
    if not msal_app: logging.error("MSAL app not initialized..."); return None
    return msal_app.get_authorization_request_url(
        scopes or SCOPE,
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True, _scheme='http')
    )

def _get_token_from_cache(scope=None):
    """Retrieves an access token from the cache for the logged-in user."""
    if not msal_app: logging.error("MSAL app not initialized..."); return None
    accounts = msal_app.get_accounts()
    user_claims = session.get("user")
    if user_claims and accounts:
        target_account = None
        for acc in accounts:
            if user_claims and (acc['home_account_id'].split('.')[0] == user_claims.get('oid') or
                acc.get('username') == user_claims.get('preferred_username')):
                target_account = acc
                break
        if target_account:
            result = msal_app.acquire_token_silent(scope or SCOPE, account=target_account)
            if not result: logging.info(f"No suitable token found in cache for user {user_claims.get('preferred_username')} and scopes {scope or SCOPE}")
            return result
        else: logging.warning("No matching account found in cache for session user.")
    if not user_claims: logging.warning("No user claims found in session for token cache lookup.")
    elif not accounts: logging.info("No accounts found in MSAL cache.")
    return None

def call_microsoft_graph(endpoint, token_dict):
    """Calls a Microsoft Graph endpoint using the provided access token dictionary."""
    if not token_dict or 'access_token' not in token_dict: logging.error("Graph Call: Invalid token"); return None
    graph_url = GRAPH_ENDPOINT + endpoint
    headers = {'Authorization': 'Bearer ' + token_dict['access_token']}
    response = None
    try:
        logging.info(f"Calling Graph API: {endpoint}")
        response = requests.get(graph_url, headers=headers, timeout=30)
        response.raise_for_status()
        if response.content: return response.json()
        else: return {}
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling Microsoft Graph ({endpoint}): {e}")
        if response is not None: logging.error(f"Graph Status: {response.status_code}, Body: {response.text}")
        return None
    except json.JSONDecodeError:
        response_text = response.text if response is not None else "No response object"
        logging.error(f"Error decoding JSON from Graph ({endpoint}). Response: {response_text}")
        return None

# --- AI Helper Function ---
def get_ai_decomposition(task_description):
    """Calls the Azure OpenAI API with updated prompt for natural output."""
    if openai_config_missing: logging.error("AI Config Missing"); return None
    if not all([AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT_NAME]):
        logging.error("AI Config Vars Missing/None"); return None

    endpoint = AZURE_OPENAI_ENDPOINT.rstrip('/') + '/'
    api_url = f"{endpoint}openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
    logging.info(f"Calling Azure OpenAI: {AZURE_OPENAI_DEPLOYMENT_NAME}")

    system_prompt = """You are Em, a supportive, non-judgmental AI assistant for users with ADHD. Your goal is to help users start tasks they feel overwhelmed by. Be gentle, understanding, sincere, and focus on breaking things down into 3-5 small, concrete, actionable first steps. Avoid demanding or overly cheerful language."""

    user_prompt = f"""I'm feeling overwhelmed by this task: '{task_description}'.

Can you help me figure out just the first few steps to get started? Keep it simple and clear. Please list the steps first (maybe numbered or bulleted). After the steps, please provide a separate, brief (1-2 sentences) encouraging thought focused specifically on tackling the very first step you listed. Sound sincere and understanding."""

    # --- Payload Definition - Ensure correct dictionary syntax ---
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None
    }
    # --- End of Payload Definition ---

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }
    response = None
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        response_data = response.json()
        logging.info(f"Raw AI Response: {response_data}")

        if response_data.get("choices") and len(response_data["choices"]) > 0:
            message_content = response_data["choices"][0].get("message", {}).get("content", "").strip()
            # --- Parsing Logic ---
            steps = "Could not identify clear steps in the response."
            encouragement = "Remember, just starting is a win!"
            step_pattern = r"^(?:\s*(?:[1-9][.)]|[*\-+])\s+.*(?:\n|$))+"
            step_match = re.search(step_pattern, message_content, re.MULTILINE)
            paragraphs = re.split(r'\n\s*\n', message_content)
            paragraphs = [p.strip() for p in paragraphs if p.strip()]

            if step_match and len(paragraphs) > 1:
                steps = step_match.group(0).strip()
                potential_encouragement = paragraphs[-1]
                if not re.match(r"^\s*(?:[1-9][.)]|[*\-+])\s+", potential_encouragement):
                     encouragement = potential_encouragement
                else: encouragement = "Focus on that first step, you can do it!"
            elif len(paragraphs) > 1:
                 steps = "\n\n".join(paragraphs[:-1])
                 encouragement = paragraphs[-1]
            elif len(paragraphs) == 1:
                 if step_match: steps = message_content; encouragement = "Just taking the first step is progress!"
                 else: steps = "No specific steps identified."; encouragement = message_content
            else: logging.warning("Could not parse steps/encouragement."); steps = message_content; encouragement = "Remember to take it one step at a time."

            logging.info(f"Parsed Steps:\n{steps}")
            logging.info(f"Parsed Encouragement:\n{encouragement}")
            return {"steps": steps, "encouragement": encouragement}
        else:
            logging.error(f"Unexpected AI response format (No choices): {response_data}")
            return None
    # --- Reverted Exception Handling (Simpler) ---
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during AI call: {e}")
        if response is not None:
            logging.error(f"Status Code: {response.status_code}, Response: {response.text}")
        return None
    except Exception as e:
        logging.error(f"Generic error in get_ai_decomposition: {e}", exc_info=True)
        if response is not None:
             logging.error(f"Status Code: {response.status_code}, Response: {response.text}")
        return None
    # --- END OF REVERT ---

# --- Routes ---
@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route("/login")
def login():
    if not msal_app: return "Error: Auth client not configured.", 500
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(state=session["state"])
    if not auth_url: return "Error: Could not generate auth URL.", 500
    logging.info(f"Redirecting to Microsoft login...")
    return redirect(auth_url)

@app.route(REDIRECT_PATH)
def authorized():
    if not msal_app: return "Error: Auth client not configured.", 500
    try:
        if request.args.get('state') != session.get("state"): logging.warning("State mismatch."); return redirect(url_for("index"))
        if "error" in request.args: logging.error(f"MS Login Error: {request.args.get('error')}"); return render_template("auth_error.html", result=request.args)
        if request.args.get('code'):
            result = msal_app.acquire_token_by_authorization_code( request.args['code'], scopes=SCOPE, redirect_uri=url_for("authorized", _external=True, _scheme='http') )
            if "error" in result: logging.error(f"MSAL Token Error: {result.get('error')}"); return render_template("auth_error.html", result=result)
            session["user"] = result.get("id_token_claims")
            if session.get("user"): logging.info(f"User logged in: {session['user'].get('name')}")
            else: logging.warning("User claims not found post-token acquisition.")
    except Exception as e: logging.error(f"Auth callback error: {e}"); return redirect(url_for("index"))
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
     session.clear()
     logout_redirect_uri = url_for('index', _external=True, _scheme='http')
     logout_url = (AUTHORITY + "/oauth2/v2.0/logout" + "?post_logout_redirect_uri=" + logout_redirect_uri)
     logging.info(f"Redirecting to logout...")
     return redirect(logout_url)

@app.route('/decompose', methods=['POST'])
def decompose_task():
    if not session.get("user"): return jsonify({"error": "User not authenticated"}), 401
    if not request.is_json: return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    task_description = data.get('task_description')
    if not task_description: return jsonify({"error": "Missing 'task_description'"}), 400
    logging.info(f"Received task for decomposition: '{task_description}'")
    result = get_ai_decomposition(task_description) # Calls updated function
    if result: logging.info("Successfully decomposed task."); return jsonify(result)
    else: logging.error("Failed to get decomposition from AI service."); return jsonify({"error": "Failed to get decomposition from AI service."}), 500

@app.route("/calendar")
def get_calendar():
    if not session.get("user"): return redirect(url_for("login"))
    token = _get_token_from_cache(SCOPE)
    if not token: logging.warning("No token for /calendar"); return redirect(url_for("login"))
    now = datetime.datetime.utcnow()
    start_time = now.isoformat() + "Z"; end_time = (now + datetime.timedelta(days=7)).isoformat() + "Z"
    query_params = f"startDateTime={start_time}&endDateTime={end_time}&$select=subject,start,end&$orderby=start/dateTime&$top=25"
    calendar_data = call_microsoft_graph(f"me/calendarview?{query_params}", token)
    return render_template("calendar.html", events=calendar_data.get('value', []) if calendar_data else [])

@app.route("/tasks")
def get_tasks():
    if not session.get("user"): return redirect(url_for("login"))
    token = _get_token_from_cache(SCOPE)
    if not token: logging.warning("No token for /tasks"); return redirect(url_for("login"))
    default_list_id = "Tasks"
    # Select fields needed, including dueDateTime
    select_fields = "id,title,status,importance,dueDateTime"
    tasks_data = call_microsoft_graph(f"me/todo/lists/{default_list_id}/tasks?$filter=status ne 'completed'&$select={select_fields}", token)
    return render_template("tasks.html", tasks=tasks_data.get('value', []) if tasks_data else [])

# --- Main execution block ---
if __name__ == '__main__':
    logging.info("Starting Flask development server...")
    app.run(debug=True, port=5001) # Keep debug=True for development
