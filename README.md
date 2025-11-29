# 🎯 AI Interview Agent

An intelligent Streamlit application that automates the interview process by generating tailored questions based on job descriptions and resumes, then evaluating candidate responses using Google's Gemini AI.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Workflow Diagram](#-workflow-diagram)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [API Configuration](#-api-configuration)
- [How It Works](#-how-it-works)

---

## ✨ Features

- **Smart Document Processing**: Upload job descriptions and resumes in PDF, DOCX, or TXT formats
- **AI-Powered Question Generation**: Automatically generates 5 tailored interview questions
- **Skills Extraction**: Intelligent extraction of technical and soft skills from documents
- **Answer Evaluation**: Comprehensive scoring (0-10) with detailed feedback
- **Follow-up Questions**: Generate deeper questions based on candidate responses
- **Progress Tracking**: Navigate through questions with progress indicators
- **Evaluation Reports**: Export detailed evaluation reports in Markdown format
- **Token Optimization**: Efficient prompting to minimize API costs

---

## 🛠 Tech Stack

### **Frontend**

- **Streamlit 1.40.2**: Interactive web interface with multi-tab layout

### **AI/ML**

- **Google Gemini 2.5 Flash**: Latest AI model for question generation and evaluation
- **LangChain 0.3.13**: AI orchestration framework
- **LangChain Google GenAI 3.2.0**: Gemini integration

### **Document Processing**

- **PyPDF2 3.0.1**: PDF text extraction
- **python-docx 1.1.2**: DOCX file processing

### **Environment**

- **Python 3.13+**: Core programming language
- **python-dotenv 1.0.1**: Environment variable management

---

## 🏗 System Architecture

```
┌────────────────────────────────────────────────────────────┐
│                     STREAMLIT WEB APP                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Upload     │  │  Questions   │  │  Evaluation  │      │
│  │  Documents   │  │     Tab      │  │     Tab      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────┬────────────────┬─────────────────┬────────────┘
             │                │                 │
             ▼                ▼                 ▼
┌────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Document    │  │  Question    │  │   Answer     │      │
│  │  Processor   │  │  Generator   │  │  Evaluator   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────┬────────────────┬─────────────────┬────────────┘
             │                │                 │
             ▼                ▼                 ▼
┌────────────────────────────────────────────────────────────┐
│                        AI LAYER                            │
│          ┌────────────────────────────────┐                │
│          │   Google Gemini 2.5 Flash      │                │
│          │   via LangChain Integration    │                │
│          └────────────────────────────────┘                │
└────────────────────────────────────────────────────────────┘
```

---

## 🔄 Workflow Diagram

```
          START
            │
            ▼
┌─────────────────────────┐
│ 1. Upload Job           │
│    Description & Resume │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 2. Extract Skills       │
│    - Gemini: Job Desc   │
│    - Local: Resume      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 3. Generate Questions   │
│    - Skills Comparison  │
│    - 5 Questions Created│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 4. Candidate Answers    │
│    - Text Input         │
│    - Navigation Support │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 5. AI Evaluation        │
│    - Score: 0-10        │
│    - Detailed Feedback  │
│    - Strengths/Weaknesses│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 6. Optional Follow-up   │
│    - Deeper Questions   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 7. Export Report        │
│    - Markdown Format    │
└─────────────────────────┘
            │
            ▼
           END
```

---

## 📦 Installation

### **Prerequisites**

- Python 3.13 or higher
- Google Gemini API key ([Get it here](https://aistudio.google.com/app/apikey))

### **Step 1: Clone or Download**

```powershell
# Clone repository (if using Git)
git clone <repository-url>
cd Interview_Agent

# Or download and extract ZIP file to your desired location
```

### **Step 2: Create Virtual Environment**

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

### **Step 3: Install Dependencies**

```powershell
pip install -r requirements.txt
```

### **Step 4: Configure API Key**

```powershell
# Copy example environment file
copy .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

---

## 🚀 Usage Guide

### **Starting the Application**

```powershell
# Make sure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Run Streamlit app
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

### **Using the Application**

#### **Tab 1: Upload Documents** 📤

1. **Job Description**

   - Choose upload method: File or Text
   - Supported formats: PDF, DOCX, TXT
   - Paste text directly if preferred

2. **Resume**

   - Choose upload method: File or Text
   - Supported formats: PDF, DOCX, TXT
   - Paste text directly if preferred

3. **Generate Questions**
   - Click "🎯 Generate Interview Questions"
   - Wait 5-10 seconds for AI processing
   - 5 tailored questions will be created

#### **Tab 2: Questions** ❓

1. **Navigation**

   - Use "⬅️ Previous" and "Next ➡️" buttons
   - Progress bar shows completion status

2. **Answering Questions**

   - Type candidate's answer in text area
   - Click "📊 Evaluate This Answer" for scoring

3. **Follow-up Questions**
   - Click "🔄 Generate Follow-up Question"
   - AI creates deeper question based on answer
   - Follow-up added to question list

#### **Tab 3: Evaluation** 📊

1. **Summary Metrics**

   - Total questions count
   - Answered questions count
   - Average score

2. **Detailed Feedback**

   - Expandable sections per question
   - Score (0-10)
   - Detailed feedback
   - Strengths and improvements

3. **Export Report**
   - Click "📥 Export Evaluation Report"
   - Download Markdown file
   - Share with team or archive

---

## 📁 Project Structure

```
Interview_Agent/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore rules
├── check_models.py            # Utility to check available models
│
├── utils/
│   ├── __init__.py           # Makes utils a package
│   ├── document_processor.py # PDF/DOCX/TXT extraction
│   ├── question_generator.py # AI question generation
│   └── answer_evaluator.py   # AI answer evaluation
│
└── README.md                  # This file
```

---

## 🔑 API Configuration

### **Getting Google Gemini API Key**

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in `.env` file

### **Available Models**

This application uses **`models/gemini-2.5-flash`**:

- ✅ Latest stable model
- ✅ Fast response times
- ✅ Generous free tier
- ✅ Excellent for text generation

### **Free Tier Limits**

- **15 requests per minute**
- **1 million tokens per day**
- **1,500 requests per day**

More than sufficient for typical interview workflows!

---

## ⚙️ How It Works

### **1. Skills Extraction**

**Job Description (Gemini AI)**

```
Input: Full job description text (first 1500 chars)
Prompt: "List ONLY the technical skills (comma-separated, max 10)"
Output: ["Python", "React", "AWS", "Docker", ...]
```

**Resume (Local Keyword Matching)**

```
Input: Full resume text
Method: Match against 50+ tech keywords
Output: ["Python", "Flask", "SQL", ...]
Benefit: Saves API calls and tokens!
```

### **2. Question Generation**

```
Input: Skills comparison summary
Skills Required: Python, React, AWS, Docker
Skills Candidate Has: Python, Flask, SQL

Prompt: "Generate 5 interview questions (mix technical/behavioral)"
Output: 5 tailored questions with categories
```

### **3. Answer Evaluation**

```
Input: Question + Answer only (no extra context)
Prompt: "Rate 0-10 with feedback, strengths, improvements"
Output: {
  score: 8,
  feedback: "Strong technical answer with examples",
  strengths: ["Clear communication", "Specific examples"],
  weaknesses: ["Could mention error handling"]
}
```

### **Token Optimization Strategy**

✅ **What We Send:**

- Skills summaries (not full documents)
- Only Q&A pairs for evaluation
- Concise prompts (< 200 tokens)

❌ **What We Don't Send:**

- Full job descriptions
- Full resumes
- Unnecessary context

**Result:** ~90% reduction in token usage vs. naive approach!

---

## 🎨 Interaction Flow

```
User Actions              →    System Response
─────────────────────────────────────────────────
Upload documents          →    Extract & preview text
Click Generate            →    AI extracts skills
                          →    AI generates 5 questions
Navigate questions        →    Show current question
Type answer               →    Store response
Click Evaluate            →    AI scores answer (0-10)
                          →    Display feedback
Click Follow-up           →    AI creates deeper question
View Evaluation Tab       →    Show all scores & metrics
Click Export              →    Download Markdown report
```

---

## 🐛 Troubleshooting

### **Issue: API Key Not Found**

```powershell
# Check .env file exists
ls .env

# Verify content
cat .env

# Restart Streamlit after editing .env
```

### **Issue: Module Not Found**

```powershell
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### **Issue: Model Not Found Error**

```powershell
# Check available models
python check_models.py

# Verify correct model name in code (models/gemini-2.5-flash)
```

---

## 📝 Best Practices

1. **Document Quality**

   - Provide detailed job descriptions
   - Include complete resume information
   - Use clear, professional language

2. **Question Answering**

   - Encourage detailed responses (50+ words)
   - Include specific examples
   - Mention technical details

3. **API Usage**

   - Monitor free tier limits
   - Avoid rapid-fire requests
   - Cache results when possible

4. **Evaluation**
   - Review AI feedback for accuracy
   - Use as guidance, not absolute truth
   - Combine with human judgment

---

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application!

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🎉 Acknowledgments

- **Google Gemini** for providing powerful AI capabilities
- **Streamlit** for the excellent web framework
- **LangChain** for AI orchestration tools

---

**Made with ❤️ for better interviews**
