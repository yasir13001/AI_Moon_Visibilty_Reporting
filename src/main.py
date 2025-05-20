from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
import pandas as pd
from src.pdf_gene import load_all_files, generate_pdf
from src.schemas import ReportRequest
from src.prompt import GenerateReport
from src.config import Settings
from fastapi.staticfiles import StaticFiles


all_data_df = pd.DataFrame()

ISLAMIC_MONTHS: list[str] = [
    "MUHARRAM",
    "SAFAR",
    "RABI-UL-AWWAL",
    "RABI-US-SANI",
    "JAMADI-UL-AWWAL",
    "JAMADI-US-SANI",
    "RAJAB",
    "SHABAN",
    "RAMADAN",
    "SHAWWAL",
    "ZUL-QADAH",
    "ZUL-HIJJAH",
]


def load_files(path):
    global all_data_df
    all_data_df = load_all_files(path)
    return all_data_df


@asynccontextmanager
async def startup(app: FastAPI):
    executor = ThreadPoolExecutor(max_workers=1)
    try:
        executor.submit(load_files, Settings.DATA_DIR)
        yield
    finally:
        executor.shutdown(wait=True)


templates = Jinja2Templates(directory=".")


app = FastAPI(lifespan=startup)
app.mount("/static", StaticFiles(directory="."), name="static")

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"islamic_months": ISLAMIC_MONTHS}
    )


@app.post("/generate-moon-parameters/")
def generate_moon_parameters(data: ReportRequest):
    try:
        df = all_data_df
        pdf_path = generate_pdf(
            df, data.date, data.islamic_month, data.islamic_year
        )  # Return full path to PDF
        return FileResponse(
            path=pdf_path,
            filename=pdf_path.split("\\")[-1],
            media_type="application/pdf",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@app.post("/generate-visibility-report/")
def generate_visibility_report(data: ReportRequest):
    df = all_data_df
    report = GenerateReport(df, data.date, data.islamic_month, data.islamic_year)
    pdf_path = report.run_all()
    return FileResponse(
        path=pdf_path, filename=pdf_path.split("\\")[-1], media_type="application/pdf"
    )


# @app.post("/generate-report/")
# async def generate_report(data: ReportRequest):
#     report = GenerateReport(data.date, data.islamic_month, data.islamic_year)
#     pdf_path = report.run_all()  # Return full path to PDF
#     print(pdf_path)
#     return FileResponse(path=pdf_path, filename=pdf_path.split("\\")[-1], media_type='application/pdf')
