# AI-Powered Purchase Requisition (PR) Pre-Approval System

A professional engineering tool for the Equipment Engineering team to pre-assess Purchase Requisitions. It uses Google Gemini AI to evaluate engineering logic and Firebase Firestore for cloud data logging.

## 🚀 Features
- **✨ AI Refinement:** Automatically transforms rough user notes into structured engineering statements.
- **🧠 Intelligent Review:** Evaluates PRs against a "Gold Standard" rubric (specificity, logic, troubleshooting).
- **📋 Cloud Logging:** Saves every request, AI decision, and coaching tip to Firebase Firestore.
- **📊 Excel Reporting:** One-click download of the entire PR history for management audit.
- **🛡️ Secure Architecture:** Decoupled Frontend/Backend with environment-variable secret protection.

## 📂 Project Structure & File Details

### Root Directory
- **`README.md`**: This document; project overview and setup guide.
- **`firebase.json`**: Configuration file for Firebase. It tells Firebase Hosting to serve files from the `frontend/` folder and ignores backend files.
- **`.firebaserc`**: Stores your Firebase project ID (`purchase-requisition-962f9`) to ensure commands target the correct cloud project.
- **`.gitignore`**: Security file that prevents sensitive data (`.env`, `serviceAccountKey.json`) and temporary files from being uploaded to GitHub.
- **`startingpoint.md`**: The original project scope and roadmap document.

### `frontend/` (The User Interface)
- **`index.html`**: A standalone web application.
  - **HTML5/CSS3**: Modern, responsive layout styled for professional engineering use.
  - **JavaScript (Async/Fetch)**: Communicates with the Python API. It includes:
    - `refineField()`: Sends rough notes to AI for professional rewriting.
    - `submitPR()`: Validates inputs locally before sending the final PR for AI evaluation.
    - `exportReport()`: Triggers the Excel download from the backend.

### `backend/` (The AI & Database Engine)
- **`api.py`**: The core "Brain" of the system built with **FastAPI**.
  - **FastAPI Endpoints**:
    - `/submit-pr`: Receives PR data, runs it through the Gemini rubric, logs results to Firestore, and returns the decision.
    - `/refine-field`: Provides quick AI-assisted documentation cleanup.
    - `/export-report`: Streams data from Firestore and converts it to a `.xlsx` file.
  - **Gemini Integration**: Uses the `google-genai` SDK with a strict engineering rubric.
  - **Firebase Admin SDK**: Securely writes and reads data from Firestore.
- **`.env`**: (Private) Stores your `GEMINI_API_KEY`.
- **`serviceAccountKey.json`**: (Private) Your secret "keycard" from Firebase that allows the Python code to talk to your database.

## 🛠️ Setup Instructions

### 1. Backend Configuration
- Navigate to `backend/`.
- Create a `.env` file and add: `GEMINI_API_KEY=your_key_here`.
- Place your Firebase `serviceAccountKey.json` in the `backend/` folder.
- Install dependencies:
  ```bash
  pip install fastapi uvicorn pydantic firebase-admin google-genai pandas openpyxl python-dotenv
  ```
- Run the server: `python api.py`.

### 2. Frontend Configuration
- The `index.html` is configured to look for the backend at `localhost:8000` (or your ngrok URL).
- Deploy to Firebase Hosting:
  ```bash
  firebase deploy --only hosting
  ```

## 📝 License
Internal Use - Equipment Engineering Team.
