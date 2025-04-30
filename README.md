Sure! Here's an **enhanced `README.md`** that includes everything you've asked for — usage, dependencies, project structure, scheduling, and even `cURL` testing instructions.

---

### ✅ Full `README.md`

```markdown
# 🌙 Moon Visibility Report Generator API

A FastAPI-based application that calculates moon visibility across regions based on astronomical data, analyzes it using Google Gemini AI, and generates a PDF report. This tool is designed for Islamic calendar observations and supports scheduled or manual report generation.

---

## 📦 Features

- 🧮 Calculates moon visibility metrics using astronomical data
- 🤖 Uses Gemini AI (Google Generative AI) to interpret data
- 📄 Generates a summarized PDF report
- 🕓 Supports background tasks and scheduling (daily/interval)
- ⚙️ API endpoint to manually trigger report generation

---

## 🛠 Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```
fastapi
uvicorn
pydantic
tqdm
pandas
python-dotenv
markdown-pdf
apscheduler
google-generativeai
```

> Note: You also need a local module `pdf_gene` and a valid Gemini API key.

---

## 🔐 Environment Variables

Create a `.env` file in your root directory and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

---

## 🚀 Running the FastAPI Server

```bash
uvicorn main:app --reload
```

---

## 📍 API Endpoint

### `POST /generate-report/`

Trigger report generation manually via POST request.

#### Example Request Body

```json
{
  "date": "28-05-2025",
  "islamic_month": "ZUL-HAJJAH",
  "islamic_year": "1446"
}
```

#### Example Response

```json
{
  "message": "Report generation started in background."
}
```

---

## 🧪 Testing the API

You can test it using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/generate-report/ \
     -H "Content-Type: application/json" \
     -d '{"date": "28-05-2025", "islamic_month": "ZUL-HAJJAH", "islamic_year": "1446"}'
```

Or use tools like Postman, Thunder Client, or Insomnia.

---

## ⏰ Automatic Scheduling (Optional)

This app includes `APScheduler` for daily automated report generation.

In `main.py`:

```python
from apscheduler.schedulers.background import BackgroundScheduler

def scheduled_job():
    report = GenerateReport("28-05-2025", "ZUL-HAJJAH", "1446")
    report.run_all()

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'interval', days=1)
scheduler.start()
```

You can customize the schedule using [cron expressions](https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html) or other intervals.

---

## 🗂 Project Structure

```
.
├── main.py               # FastAPI app entry point
├── generate_report.py    # Contains the GenerateReport class logic
├── pdf_gene/             # Your custom moon calculation logic
├── .env                  # Environment file with API keys
├── requirements.txt
└── README.md
```

---

## 📄 Output

Upon successful execution, a report like this will be generated:

```
Visibility_report(28-05-2025).pdf
```

This PDF includes:
- A summary paragraph
- Structured findings
- Key visibility factors
- A final conclusion

---

## 📝 License

MIT License © 2025 Your Name
```

---

Let me know if you'd like a **GitHub Actions CI setup**, **Dockerfile**, or a sample `.env` and test client script included too!