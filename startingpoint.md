Here is the complete project documentation and implementation plan. You can copy this summary directly to present to your management or IT team to explain exactly what you are building, how it works, and what resources are required.

*

# *Project Plan: AI-Powered Purchase Requisition (PR) Pre-Approval System*

### *1. Executive Summary*
The objective of this project is to build a standalone, AI-driven application for the Equipment Engineering team to pre-assess Purchase Requisitions (PRs). By enforcing a mandatory template and using AI to evaluate the technical logic of the request, this system will eliminate incomplete submissions, reduce manual review time, and maintain a centralized database of all PR activity.

### *2. System Architecture*
The application is built on a modern, decoupled architecture, meaning the user interface (Frontend) is separated from the AI processing and data storage (Backend).

* *The Frontend (User Interface):* A lightweight HTML/JavaScript web form embedded directly into the team's existing SharePoint site. It requires zero installation for end-users.
* *The Backend (Processing Engine):* A Python-based API (using the FastAPI framework) hosted on an internal server. It handles incoming requests, runs validation, and communicates with the AI.
* *The AI Engine:* A Large Language Model (e.g., Google Gemini or OpenAI) that receives the PR data, evaluates the engineering logic, and returns a structured Approve/Reject recommendation.
* *The Database:* A lightweight SQLite database, managed automatically by the Python backend, to log every submission, timestamp, and AI decision.
* *Reporting:* An automated Excel export feature (using Pandas) to download historical PR data for auditing and management review.

### *3. Required Infrastructure & Approvals*
To take this to production, the following resources are required from IT/Management:
1.  *Internal Server Hosting:* A basic Virtual Machine (VM) or internal cloud environment to run the Python backend continuously.
2.  *Network Permissions:* IT must allow the internal SharePoint site to communicate with the newly hosted Python API server (CORS configuration).
3.  *AI API Key:* Approval to procure a standard developer API key from an enterprise LLM provider (e.g., Google Cloud or OpenAI) to power the reasoning engine.

### *4. Implementation Roadmap*

*Phase 1: Local Prototyping (Completed)*
* Write the initial Python code using mock AI logic.
* Design the HTML form for the mandatory 5-field template (Requestor, Area/Dept, Problem Statement, Current Situation, Next Step).
* Test the connection between the HTML file and the local Python API.

*Phase 2: Backend Deployment & Database Setup*
* Move the Python script (api.py) to the dedicated internal server.
* Install required Python libraries (fastapi, uvicorn, pydantic, pandas, openpyxl).
* Integrate the real AI API key into the script.
* Initialize the SQLite database to ensure it begins logging data.
* Start the server and acquire the official internal URL (e.g., http://ee-pr-api.internal:8000).

*Phase 3: SharePoint Integration*
* Navigate to the Equipment Engineering SharePoint page.
* Add an "Embed" or "Script Editor" web part.
* Paste the HTML/JavaScript code into the web part.
* Update the JavaScript fetch URL to point to the new internal Python server.

*Phase 4: Testing & Rollout*
* Submit 5–10 test PRs through the SharePoint form.
* Verify that incomplete fields or poor technical justifications are correctly rejected by the AI with coaching feedback.
* Verify that logical requests are approved.
* Click the "Download Excel Report" button to ensure the SQLite database successfully exports the logged history.
* Roll out the tool to the engineering team.
