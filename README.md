# 🎬 SentimentAI: Movie Review Sentiment Analysis Dashboard

![Demo](https://github.com/Omkarok2510/Sentiment-Analysis-Dashboard/blob/main/images/demo.gif?raw=true)

A full-stack web application for analyzing the sentiment of movie reviews. This project allows users to perform instant sentiment checks on single reviews and conduct batch analysis on multiple reviews uploaded via a text file, displaying the overall sentiment distribution.

---

## ✨ Features

- **Instant Sentiment Check**: Analyze individual movie reviews for sentiment (positive, negative, or neutral) using a simple input form.
- **Batch Sentiment Analysis**: Upload a `.txt` file with multiple reviews and get sentiment counts for each category.
- **Interactive UI**: Sleek glassmorphism dashboard styled with Tailwind CSS.
- **Sidebar Navigation**: Access Dashboard, Reports, Analytics, Settings, and About pages.
- **Backend Integration**: Powered by Flask and Gemini AI for smart analysis.

---

## 🛠️ Technologies Used

**Frontend**:
- HTML5
- Tailwind CSS
- JavaScript (ES6+)

**Backend**:
- Python 3.x
- Flask
- Flask-CORS
- Requests
- Google Gemini API (`gemini-2.0-flash`)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip
- Git

---

### 1. Get Your Gemini API Key

- Go to [Google AI Studio](https://makersuite.google.com/app)
- Log in with your Google account
- Generate an API key and copy it

---

### 2. Clone the Repository
```bash
git clone https://github.com/Omkarok2510/Sentiment-Analysis-Dashboard.git
cd Sentiment-Analysis-Dashboard
```
### 3. 🔧 Set Up Your Environment
3.1 Create and activate a virtual environment
```bash
python -m venv venv

# Activate it:
# Windows CMD
.\venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```
3.2 Install dependencies
```
pip install -r requirements.txt
```
3.3 Set your Gemini API key as an environment variable

Use the same terminal session for running the app.
```bash
# Windows CMD
set GEMINI_API_KEY=YOUR_API_KEY_HERE

# PowerShell
$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"

# macOS/Linux
export GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 4. ▶️ Run the Application
```bash
python app.py
```
Visit the app in your browser at http://127.0.0.1:5000


### 📂 Project Structure
```
Sentiment-Analysis-Dashboard/
├── app.py                  # Flask backend with API logic
├── templates/
│   └── dashboard.html      # Main frontend UI
├── images/
│   └── demo.gif            # Demo GIF
├── requirements.txt        # Backend dependencies
├── .gitignore              # Ignored files
└── README.md               # Project documentation

```
### 📞 Contact
**Made with ❤️ by Omkar**

📧 **Email: omkarok25@gmail.com**

🌐 **GitHub: @Omkarok2510**
