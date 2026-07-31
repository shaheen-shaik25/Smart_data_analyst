# 📊 AI Data Analyst

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

```bash
streamlit run app.py
```

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

## 👨‍💻 Author

**Shaheen Shaik**

- GitHub: https://github.com/your-username
- LinkedIn: https://linkedin.com/in/your-profile

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub!
