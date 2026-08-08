# 📊 Smart Data Analyst

An AI-powered data analysis platform built with **Python**, **Streamlit**, **Pandas**, **Plotly**, and **OpenAI/Gemini APIs**. The application enables users to upload CSV or Excel datasets, perform automated exploratory data analysis (EDA), generate AI-powered business insights, ask questions in natural language, create interactive visualizations, and export professional HTML reports.

---

## 🚀 Features

- 📂 Upload CSV and Excel datasets
- 📊 Automated Exploratory Data Analysis (EDA)
- 🤖 AI-powered business insights using OpenAI/Gemini
- 💬 Natural Language Querying (Ask questions about your data)
- 📈 Interactive charts and visualizations
- 🔍 Missing value and duplicate detection
- 📋 Statistical summaries
- 📄 HTML report generation
- ⚡ User-friendly Streamlit interface

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- OpenAI API / Google Gemini API
- Matplotlib
- Scikit-learn

---

## 📂 Project Structure

```text
AI-Data-Analyst/
│
├── app.py                     # Main Streamlit application
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignored files
├── .env.example               # Environment variables template
│
├── sample_data/
│   └── sample_sales.csv       # Sample dataset for testing
│
└── src/
    ├── __init__.py            # Initializes the Python package
    ├── ai_engine.py           # AI model integration (OpenAI/Gemini)
    ├── chart_generator.py     # Interactive chart generation
    ├── data_loader.py         # Dataset loading and preprocessing
    ├── insights.py            # Automated data insights generation
    ├── nl_query.py            # Natural language query processing
    └── report_exporter.py     # HTML report generation and export
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-data-analyst.git
cd ai-data-analyst
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Keys

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

---

## ▶️ Run the Application
=======
# 📊 AI Data Analyst

An AI-powered data analysis web app built with **Streamlit**, **Pandas**, **Plotly**, and the **OpenAI / Gemini API**.

Upload a CSV or Excel file and it will:

- Profile the dataset (rows, columns, missing data, duplicates, types)
- Generate plain-English **business insights** using AI (with a rule-based fallback if you don't have an API key)
- Let you **ask natural language questions** about your data ("Which product sold the most?") and get answers computed live with pandas
- Automatically generate relevant **charts** (bar, histogram, correlation heatmap, time series, pie)
- **Export** everything as a single self-contained HTML report

It works fully **without any API key** in a rule-based fallback mode, so you can demo it immediately — then flip on AI for smarter summaries and free-text Q&A.

---

## 1. Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) configure an AI provider
cp .env.example .env
# then edit .env and add your OPENAI_API_KEY or GEMINI_API_KEY
```

Requires Python 3.10+.

## 2. Run
>>>>>>> 1058ae3 (Code Files)

```bash
streamlit run app.py
```

<<<<<<< HEAD
Open your browser and visit:

```
http://localhost:8501
```

---

## 📁 Supported File Formats

- CSV (.csv)
- Excel (.xlsx)

---

## ✨ Key Functionalities

- Dataset upload and validation
- Automated Exploratory Data Analysis (EDA)
- Statistical summaries
- Missing value analysis
- Duplicate detection
- AI-generated business insights
- Natural language data querying
- Interactive visualizations
- HTML report export

---

## 🎯 Future Enhancements

- PDF report export
- SQL database connectivity
- Chat history
- Dashboard filters
- User authentication
- Cloud deployment
- Docker support
- Dark mode

---

## 📄 License

This project is licensed under the **MIT License**.

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub!
=======
This opens the app at `http://localhost:8501`.

You can also skip file upload entirely and click **"Or try it with sample data"** — the app ships with a small sample sales dataset in `sample_data/sample_sales.csv`.

## 3. Using AI (optional)

You can configure the AI provider two ways:

1. **`.env` file** — set `AI_PROVIDER`, and `OPENAI_API_KEY` or `GEMINI_API_KEY`.
2. **In the app sidebar** — paste your key directly at runtime (it's stored only for the current session, never written to disk).

Without a key, the app still works:
- "AI Insights" falls back to rule-based summaries (top values, missing data %, correlations, etc.)
- "Ask a Question" falls back to a small keyword matcher (max/min/average of a column, row counts)

## 4. Project Structure

```
ai_data_analyst/
├── app.py                  # Streamlit UI — entry point
├── requirements.txt
├── .env.example
├── src/
│   ├── ai_engine.py         # OpenAI/Gemini wrapper
│   ├── data_loader.py       # File loading + dataset profiling
│   ├── insights.py          # AI + rule-based business insights
│   ├── chart_generator.py   # Automatic Plotly chart selection
│   ├── nl_query.py          # Natural language -> pandas code (sandboxed exec)
│   └── report_exporter.py   # Self-contained HTML report builder
└── sample_data/
    └── sample_sales.csv
```

## 5. How "Ask a Question" works

1. The column names/types of your DataFrame are sent to the LLM along with your question.
2. The LLM returns a small pandas snippet that stores its answer in a variable called `result`.
3. That snippet is executed in a **restricted sandbox** (no imports, no file/network access, whitelisted builtins only) against a **copy** of your DataFrame.
4. The result (number, text, DataFrame, or Series) is displayed, along with the generated code so you can see exactly what ran.

## 6. Deploying

This app deploys as-is to [Streamlit Community Cloud](https://streamlit.io/cloud), Render, or any host that runs a `streamlit run app.py` process. Set your API keys as environment variables/secrets on the host instead of committing a `.env` file.

## 7. Resume / Portfolio Notes

Good talking points for interviews:
- End-to-end data pipeline: ingestion → cleaning/profiling → EDA → AI-generated insights → export
- Practical LLM integration pattern: **text-to-pandas-code with a sandboxed executor**, not just a chatbot wrapper
- Graceful degradation: app remains fully functional with zero API keys configured
- Clean separation of concerns (`src/` modules) instead of one giant script

---

## License

Free to use, modify, and include in your own portfolio.
>>>>>>> 1058ae3 (Code Files)
