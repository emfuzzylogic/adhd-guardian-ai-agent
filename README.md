# ADHD Guardian ✨

## Your AI Partner for Navigating Focus Flow

> "For those of us with ADHD, starting tasks isn't just about discipline—it's about overcoming invisible executive function barriers that others don't see. ADHD Guardian is the empathetic AI companion I wish I'd had throughout my own journey."



## 🌟 Project Overview

**ADHD Guardian** is an AI-powered web application specifically designed as a supportive work companion for professionals and students with ADHD. It aims to mitigate executive function challenges by providing AI-driven task decomposition, prioritization assistance, and positive reinforcement—all while integrating seamlessly with Microsoft productivity tools.

### 📊 The Challenge: The ADHD "Wall of Awful"

For the estimated 4-5% of adults worldwide living with ADHD (approximately 366 million people), initiating tasks—especially complex or open-ended ones—can feel like hitting an invisible barrier, often referred to as the "Wall of Awful." This executive function challenge involves difficulties with:

- Planning and organizing work
- Sequencing steps in logical order
- Prioritizing competing demands
- Overcoming the mental inertia required to simply start

Standard productivity tools often feel rigid or even add to the overwhelm, lacking the specific support needed to bridge the gap between intention and action. The result? Frustration, procrastination, missed deadlines, and untapped potential—all contributing to the estimated $67 billion in lost workplace productivity annually attributed to ADHD.

### 💡 Solution

ADHD Guardian acts as a non-judgmental, supportive co-pilot specifically designed to help neurodivergent individuals navigate executive function hurdles. Instead of just listing tasks, it tackles the critical first step: **task initiation**.

The application leverages Azure OpenAI (GPT-4o) through an AI persona named "Em" to:

1. **Decompose Overwhelm**: Users input a task or objective they find daunting
2. **Generate Actionable Steps**: Em breaks the task down into 3-5 small, concrete, achievable first steps
3. **Provide Sincere Encouragement**: Crucially, Em offers brief, gentle understanding focused only on starting the very first step—validating the difficulty without judgment

The goal is not to replace planning tools but to provide the scaffolding and dopamine boost needed to overcome initiation paralysis and build momentum.


## 🏗️ Technical Architecture

### High-Level Architecture

![High-Level Architecture](https://github.com/emfuzzylogic/adhd-guardian-ai-agent/blob/main/System%20Design/Architecture.png)

### Authentication Flow

![Authentication Flow](https://github.com/emfuzzylogic/adhd-guardian-ai-agent/blob/main/System%20Design/Authentication%20Flow.png)

### Component Diagram

![Component Diagram](https://github.com/emfuzzylogic/adhd-guardian-ai-agent/blob/main/System%20Design/Component%20breakdown.png)


### Technology Stack

![Technology Stack](https://github.com/emfuzzylogic/adhd-guardian-ai-agent/blob/main/System%20Design/Technology%20Stack.png)



## ✨ Key Features (Current MVP)

- **AI-Powered Task Decomposition**: Uses Azure OpenAI (GPT-4o) to break down user-inputted tasks
- **Contextual Encouragement**: Provides tailored, non-judgmental prompts focused on the first action step
- **Microsoft Account Authentication**: Secure login via Azure AD using MSAL for Python
- **Simple Web Interface**: Clean UI built with Flask, HTML, and Tailwind CSS
- **(Demo) Task & Calendar Views**: Placeholder pages showing hardcoded tasks and basic calendar fetching via Microsoft Graph API (requires user consent)


### AI Agent UI Page Screenshots

#### Login Screen
![Login Screen](https://github.com/emfuzzylogic/adhd-guardian-ai-agent/blob/main/UI/home%20page-not%20logged%20in.png)

#### Main Interface - Task Input
![Main Interface](https://github.com/emfuzzylogic/adhd-guardian-ai-agent/blob/main/UI/homepage%20after%20loggin.png)

#### Calendar View
![calendars page.png](https://github.com/emfuzzylogic/adhd-guardian-ai-agent/blob/main/UI/calendars%20page.png)

#### To-Do Task List
![Task List](https://github.com/emfuzzylogic/adhd-guardian-ai-agent/blob/main/UI/tasks%20page.png)

#### Task Breakdown Example
![Task Breakdown](https://github.com/emfuzzylogic/adhd-guardian-ai-agent/blob/main/UI/after%20break%20down%20tasks.png)

                


## 📱 Real-World Scenarios

### Scenario 1: The Looming Work Project

**The Struggle**: Alex, a marketing professional with ADHD, has been assigned to create a comprehensive campaign strategy. The deadline is two weeks away, but the open-ended nature of the task feels overwhelming. Every time Alex tries to start, they find themselves paralyzed, resorting to checking email or tackling smaller, less important tasks instead. As the deadline approaches, anxiety increases—yet starting still feels impossible.

**How ADHD Guardian Helps**: Alex opens ADHD Guardian and types: "Create comprehensive marketing campaign strategy for new product launch." Em immediately breaks this down into specific, actionable first steps:

1. Open a new document and title it "Product X Campaign Strategy - Draft"
2. Write down the 3 main target audiences for this product
3. List 5 key product features/benefits these audiences would care about

Em then provides gentle encouragement: "Just focus on opening that document and giving it a title right now. That's all. Getting started is often the hardest part for ADHD brains, and that's okay. This small step is actually huge—and I'm here whenever you need the next step."

This concrete first step feels doable, reducing Alex's activation energy and helping them overcome the initial resistance.

### Scenario 2: The Overwhelming Assignment

**The Struggle**: Jamie, a graduate student with ADHD, needs to write a 20-page research paper. Despite being genuinely interested in the topic, they've procrastinated for weeks because they can't figure out how to start or organize their thoughts. Every time Jamie sits down to work, they feel overwhelmed by all the research they've collected and end up scrolling social media instead. Self-doubt creeps in ("Maybe I'm not cut out for grad school"), creating a negative feedback loop.

**How ADHD Guardian Helps**: Trinity logs into ADHD Guardian using their Microsoft account and enters: "Write 20-page research paper on climate change impacts on marine ecosystems." Em provides this breakdown:

1. Create a new document titled "Marine Ecosystems Paper - Working Draft"
2. Without any pressure for quality, write 3-5 sentences about why you personally find this topic interesting
3. List the 3 main areas of marine ecosystems you want to cover

Em adds: "Hey Trinity, let's just focus on creating that document and writing those few sentences about your interest in the topic. Don't worry about perfection or even the full paper yet. Your ADHD brain might resist getting started because it's seeing the entire mountain instead of the first step. This tiny action will help build momentum. I'll be here when you're ready for what comes next."

This approach reduces the perceived scope, provides a concrete starting point, and acknowledges the executive function challenges without judgment.




## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- An Azure account with access to Azure AD and Azure OpenAI
- A registered application in Azure AD

### Setup Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd adhd-guardian
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your `.env` file:
   ```
   # Azure OpenAI
   AZURE_OPENAI_ENDPOINT="YOUR_AZURE_OPENAI_ENDPOINT"
   AZURE_OPENAI_KEY="YOUR_AZURE_OPENAI_KEY"
   AZURE_OPENAI_DEPLOYMENT_NAME="YOUR_MODEL_DEPLOYMENT_NAME"

   # Azure AD App Registration
   CLIENT_ID="YOUR_APP_REGISTRATION_CLIENT_ID"
   CLIENT_SECRET="YOUR_APP_REGISTRATION_CLIENT_SECRET_VALUE"
   AUTHORITY="https://login.microsoftonline.com/common" # Or your specific tenant
   REDIRECT_PATH="/getAToken"
   SCOPE="User.Read Calendars.Read Tasks.Read email" # Required scopes

   # Flask Session
   SECRET_KEY="generate-a-strong-random-secret-key-here"
   ```

5. Run the application:
   ```bash
   flask run --port 5001
   ```

6. Access the application at `http://localhost:5001`




## 🏆 Hackathon Alignment

This submission for the Microsoft AI Agents Hackathon 2025 (Python Track) aligns with the judging criteria as follows:

### Innovation

As someone who has personally struggled with ADHD, I recognized that most productivity tools miss the specific executive function support needed for task initiation. ADHD Guardian innovates by:

- **Premise**: Addressing the specific, often overlooked neurodiversity challenge of ADHD task initiation in a work/academic context using an AI agent paradigm
- **Technology Implementation**: Leveraging Azure OpenAI not just for generation, but for empathetic interaction through prompt engineering focused on a non-judgmental, supportive persona ("Em") tailored to ADHD user needs
- **Beyond Task Management**: Moving past simple to-do lists to provide the specific scaffolding needed for breaking through initiation paralysis

### Impact

The impact of ADHD Guardian extends far beyond simple productivity gains:

- **Population Affected**: With 4-5% of adults worldwide living with ADHD (approximately 366 million people), and many more undiagnosed, the potential reach is significant
- **Employment Challenges**: Adults with ADHD are 60% more likely to lose their jobs and earn 17% less than neurotypical peers—largely due to executive function barriers that this tool directly addresses
- **Educational Support**: The academic dropout rate for students with ADHD is 2-3 times higher than their peers, often due to difficulties with task initiation and follow-through
- **Mental Health Benefits**: By reducing task-related anxiety and building a sense of capability, ADHD Guardian has the potential to improve self-esteem and reduce the negative self-talk common among ADHDers
- **Accessibility Focus**: Many cannot access formal ADHD coaching or therapy due to cost or availability barriers—this tool democratizes access to evidence-based executive function support techniques

As someone who has tried countless productivity apps only to abandon them when they added to my cognitive load rather than reducing it, I built ADHD Guardian to fill a gap in supportive technology that truly understands the ADHD brain.

### Usability

- **Real-world Scenarios**: Addresses common daily situations where ADHDers struggle to initiate tasks despite genuine desire to complete them
- **Practical Interface**: Simple web UI designed to minimize distraction and cognitive load
- **Familiar Authentication**: Microsoft Account login provides secure, frictionless access
- **User-Centered Design**: Every aspect of the interaction is designed based on research into ADHD executive function needs and my own lived experience
- **Responsible AI**: 
  - Non-judgmental, supportive tone built into prompt engineering
  - Clear limitations acknowledged (not a replacement for therapy)
  - Explicit consent for Microsoft data access
  - Human-in-the-loop design principles for AI suggestion refinement

### Solution Quality

- **Functional Implementation**: Working Flask web application with clear frontend/backend architecture
- **Security Focus**: Proper authentication flows and token handling
- **Documentation**: Comprehensive README, code comments, and architecture diagrams
- **Technical Integration**: Demonstrates seamless integration of Flask, Azure AD authentication (MSAL), Azure OpenAI API, and Microsoft Graph API

### Python Track Alignment

- **Backend Development**: Core application logic built entirely in Python using Flask
- **Service Integration**: Python libraries used for API interactions (requests, msal)
- **Environment Management**: Python best practices for dependencies and configuration
- **AI Implementation**: Azure OpenAI integration central to the core value proposition, not just an add-on feature

## 🔮 Future Roadmap

- **Full Microsoft Integration**: Complete integration with Microsoft Outlook Calendar and To-Do
- **Task Completion & Sync**: Implement writing back to Microsoft To-Do when tasks are completed
- **Persistent Views**: Add options for browser notifications or dedicated views to keep tasks visible
- **Proactive Suggestions**: AI-driven proactive breakdown suggestions for complex upcoming tasks
- **Prioritization Engine**: AI assistance in prioritizing combined tasks and events
- **Mobile Application**: Develop companion mobile app for on-the-go support

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 🙏 Acknowledgments

- Special thanks to people and organizations who support and advocate for neurodivergent
- All neurodivergent individuals whose unique perspectives drive innovation

---

Built with ❤️ by Emily F. - Microsoft AI Agents Hackathon 2025
