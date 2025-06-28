# 🗓️ TailorTalk – Calendar Slot Booking Agent

TailorTalk is an intelligent calendar slot booking agent built with **FastAPI**, **Streamlit**, and **Google Calendar API**. It uses natural language understanding to parse user requests like:

- “Book a call tomorrow 3-4 pm”
- “Schedule meeting Tuesday afternoon”
- “Book a meeting between 3-5 PM next week”

and automatically books calendar events for you.

---

## 🚀 Features

✅ Extracts datetime slots from user input  
✅ Supports phrases like _tomorrow_, _Sunday_, _afternoon_, _evening_, etc.  
✅ Checks for conflicting events before booking  
✅ Books slots directly to your Google Calendar  
✅ FastAPI backend for integrations  
✅ Streamlit interface for testing and demos  
✅ Timezone-aware scheduling using `dateparser` and `zoneinfo`

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** – API endpoints
- **Streamlit** – Chat UI (optional)
- **Google Calendar API** – Event creation
- **dateparser, python-dateutil, regex** – Natural language datetime parsing
- **dotenv** – Environment management

---

## 🔧 Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/yourusername/TailorTalk.git
cd TailorTalk
```

### 2. Create virtual environment and activate

```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Set up environment variables

#### Create a .env file with:

- **OPENAI_API_KEY** – Your OpenAI API key for using GPT models
- **GOOGLE_CLIENT_SECRET_FILE** – Path to your Google API credentials JSON file
- **GOOGLE_CALENDAR_ID** – Your Google Calendar ID (`primary` for your default calendar)

_(Make sure `credentials.json` exists in your project root or adjust the path accordingly.)_

## 💻 Running the project

### ▶️ Run FastAPI server

```
uvicorn main:app --reload
```

## ▶️ Run Streamlit demo

```
streamlit run app.py
```
