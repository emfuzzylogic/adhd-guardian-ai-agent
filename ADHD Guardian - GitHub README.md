# **ADHD Guardian ✨ \- Focus Flow Engine**

**Your AI partner for navigating actionable task initiation.**

**(Microsoft AI Agents Hackathon 2025 Submission \- Python Track)**

### **The Challenge: The ADHD "Wall of Awful"**

For individuals with ADHD, initiating tasks, especially complex or open-ended ones, can feel like hitting an invisible barrier – often referred to as the "Wall of Awful". This executive function challenge involves difficulties with planning, sequencing, prioritizing, and overcoming the mental inertia required to simply *start*. Standard productivity tools can sometimes feel rigid or even add to the overwhelm, lacking the specific support needed to bridge the gap between intention and action. The result? Frustration, procrastination, and missed potential.

### **Our Solution: ADHD Guardian**

ADHD Guardian is a web-based AI agent designed specifically to act as a **non-judgmental, supportive co-pilot** for professionals and students navigating these executive function hurdles. It tackles the critical first step: **task initiation**.

Instead of just listing tasks, ADHD Guardian leverages the power of Azure OpenAI (specifically, a GPT-4o deployment) to:

1. **Decompose Overwhelm:** Users input a task or objective they find daunting.  
2. **Generate Actionable Steps:** The AI ("Em") breaks the task down into 3-5 small, concrete, achievable first steps.  
3. **Provide Sincere Encouragement:** Crucially, Em offers a brief, gentle, and understanding message focused *only* on starting the very first step, validating the difficulty without judgment.

The goal is not to replace planning tools but to provide the **scaffolding and dopamine hit** needed to overcome initiation paralysis and build momentum.

### **Key Features (Current MVP)**

* **AI-Powered Task Decomposition:** Uses Azure OpenAI (GPT-4o) to break down user-inputted tasks.  
* **Contextual Encouragement:** Provides tailored, non-judgmental prompts focused on the first action step.  
* **Microsoft Account Authentication:** Secure login via Azure AD using MSAL for Python.  
* **Simple Web Interface:** Clean UI built with Flask, HTML, and Tailwind CSS.  
* **(Demo) Task & Calendar Views:** Placeholder pages showing hardcoded tasks and basic calendar fetching via Microsoft Graph API (requires user consent).

### **Alignment with Hackathon Criteria**

We believe ADHD Guardian strongly aligns with the hackathon's judging criteria:

1. **Innovation (20%):**  
   * **Premise:** Addresses the specific, often overlooked neurodiversity challenge of ADHD task initiation in a work context using an AI agent paradigm.  
   * **Technology Implementation:** Leverages Azure OpenAI not just for generation, but specifically for empathetic interaction – prompt engineering focuses on a non-judgmental, supportive persona ("Em") tailored to ADHD user needs, moving beyond generic task management.  
   * **Demo:** The video showcases the core loop of user input \-\> AI breakdown \-\> tailored encouragement, demonstrating a practical application.  
2. **Impact (20%):**  
   * **Usefulness:** Directly tackles a significant real-world pain point for a large user group, potentially improving productivity, reducing work-related stress, and fostering a sense of capability. Many individuals and organizations could benefit.  
   * **Value/Purpose:** The value is clear – providing immediate, actionable steps and crucial motivational support *at the point of struggle* (task initiation), helping users overcome executive function barriers.  
3. **Usability (20%):**  
   * **Real-world Scenario:** Addresses the common daily scenario of facing a complex task and feeling unable to start.  
   * **Practicality:** The simple web interface allows users to quickly input a task and get immediate support. Authentication via Microsoft accounts provides a familiar entry point.  
   * **Responsible AI:** Designed from the ground up to be non-judgmental and supportive, avoiding criticism or pressure. The AI persona ("Em") is instructed to be gentle and understanding. Limitations (not a replacement for therapy or full planning tools) are acknowledged. User data access (for planned features) relies on explicit consent via standard Microsoft mechanisms. *Human-in-the-Loop for refining AI suggestions is a key area for future work.*  
4. **Solution Quality (20%):**  
   * **Completeness:** Provides a functional Flask web application with distinct frontend and backend components. Code includes comments explaining core logic. A clear README outlines setup and architecture. Secure handling of secrets via .env file.  
   * **Technical Implementation:** Demonstrates integration of Flask, Azure AD authentication (MSAL), Azure OpenAI API calls, basic HTML/CSS/JS frontend, and session management. The core technical substance lies in the AI prompt engineering and the orchestration of these services. It's more than just sample code; it's an integrated solution addressing a specific problem.  
   * **Architecture:** A clear architecture diagram and explanation are provided below.  
5. **Alignment with Hackathon Category (Python Track \- 20%):**  
   * **Agent & Language:** The solution's backend logic, authentication handling, and AI interaction are built primarily using **Python** with the **Flask** framework.  
   * **Showcasing Python:** Effectively uses Python for web serving, API integration (requests, msal), environment management (venv, dotenv), and core application logic.  
   * **AI Implementation:** Azure OpenAI is **central** to the agent's core value proposition (task decomposition and encouragement), not just an add-on feature.

### **Technical Architecture**

*(Referencing diagram from adhd\_guardian\_arch\_design\_v2)*

The application uses a client-server model:

graph TD  
    subgraph User Environment  
        A\[User Browser (HTML/JS/Tailwind)\]  
    end

    subgraph Application Backend (Local Development Server)  
        B(Flask Server \- app.py)  
        B \-- Manages \--\> C{User Session (Flask-Session)};  
        B \-- Uses \--\> D\[Auth Module (MSAL)\];  
        B \-- Uses \--\> E\[AI Module (Azure OpenAI)\];  
        B \-- Uses \--\> F\[Graph API Module (Demo/Planned)\];  
    end

    subgraph Azure Cloud Services  
        G\[Microsoft Identity Platform (Azure AD)\];  
        H\[Azure OpenAI Service (gpt-4o)\];  
        I\[Microsoft Graph API\];  
    end

    A \-- HTTPS Request \--\> B;  
    B \-- Renders \--\> A;  
    D \-- OAuth 2.0 Flow \--\> G;  
    G \-- ID/Access Tokens \--\> D;  
    E \-- REST API Call (HTTPS \+ API Key) \--\> H;  
    H \-- LLM Response \--\> E;  
    F \-- REST API Call (HTTPS \+ Access Token) \--\> I;  
    I \-- User Data (Calendar/Tasks) \--\> F;

    style User Environment fill:\#D2E3C8,stroke:\#333  
    style Application Backend fill:\#FFF3C7,stroke:\#333  
    style Azure Cloud Services fill:\#C3B9DD,stroke:\#333

* **Frontend:** HTML, Tailwind CSS (via CDN), Vanilla JavaScript.  
* **Backend:** Python 3.x, Flask, Flask-Session.  
* **Authentication:** Microsoft Identity Platform (Azure AD) using MSAL for Python.  
* **AI:** Azure OpenAI Service (using a GPT-4o deployment).  
* **Data (Demo/Planned):** Microsoft Graph API (Outlook Calendar, To Do).  
* **Libraries:** requests, python-dotenv, msal, Flask-Session.

*(See adhd\_guardian\_arch\_design\_v2 for detailed component breakdown and flow diagrams)*

### **Setup & Running Locally**

1. **Clone Repository:** git clone \<your-repo-url\>  
2. **Navigate to Folder:** cd ADHD\_Agent  
3. **Create Virtual Environment:** python \-m venv venv  
4. **Activate Virtual Environment:**  
   * Windows: .\\venv\\Scripts\\activate  
   * Mac/Linux: source venv/bin/activate  
5. **Install Dependencies:** pip install Flask requests python-dotenv msal Flask-Session requests\_oauthlib  
6. **Azure AD App Registration:**  
   * Register an app in Azure AD.  
   * Configure a **Web** platform Redirect URI: http://localhost:5001/getAToken  
   * Create a **Client Secret**.  
   * Add **API Permissions** (Delegated) for Microsoft Graph: User.Read, Calendars.Read, Tasks.Read, email, openid, profile, offline\_access. Grant admin consent if needed.  
7. **Azure OpenAI Setup:**  
   * Create an Azure OpenAI resource.  
   * Deploy a **chat-compatible model** (e.g., gpt-4o). Note the **Deployment Name**.  
   * Get the resource **Endpoint** and an **API Key**.  
8. **Configure .env File:**  
   * Create a file named .env in the project root.  
   * Add the following, replacing placeholders with your actual values:  
     \# Azure OpenAI  
     AZURE\_OPENAI\_ENDPOINT="YOUR\_AZURE\_OPENAI\_ENDPOINT"  
     AZURE\_OPENAI\_KEY="YOUR\_AZURE\_OPENAI\_KEY"  
     AZURE\_OPENAI\_DEPLOYMENT\_NAME="YOUR\_MODEL\_DEPLOYMENT\_NAME"

     \# Azure AD App Registration  
     CLIENT\_ID="YOUR\_APP\_REGISTRATION\_CLIENT\_ID"  
     CLIENT\_SECRET="YOUR\_APP\_REGISTRATION\_CLIENT\_SECRET\_VALUE"  
     AUTHORITY="https://login.microsoftonline.com/common" \# Or your specific tenant  
     REDIRECT\_PATH="/getAToken"  
     SCOPE="User.Read Calendars.Read Tasks.Read email" \# Exclude reserved scopes

     \# Flask Session  
     SECRET\_KEY="generate-a-strong-random-secret-key-here"

9. **Run the App:** flask run \--port 5001  
10. **Access:** Open your browser to http://localhost:5001/

### **Demo Video**

*(Link to your demo video will go here)*

### **Future Work**

* **Live Microsoft Graph Integration:** Replace demo task data with live fetching from user's selected To Do lists and display relevant calendar events dynamically on the main dashboard.  
* **Task Completion Sync:** Allow marking tasks "done" within the agent and sync this status back to Microsoft To Do.  
* **Proactive Suggestions:** Agent could analyze upcoming deadlines or complex tasks and proactively offer breakdowns.  
* **Contextual Awareness:** Use calendar data to understand user's schedule (e.g., meetings) and tailor suggestions or focus timers.  
* **Enhanced UI:** Implement progress bars, more sophisticated task views, and customizable settings.  
* **Persistent Storage:** Move beyond filesystem sessions for more robust token/state management.

Thank you for checking out ADHD Guardian\!