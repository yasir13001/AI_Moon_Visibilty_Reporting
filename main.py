#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from prompt import GenerateReport  # Adjust import based on your file location
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pdf_gene import generate_pdf, load_all_files
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from fastapi import HTTPException



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or list of allowed client URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html") as f:
        return f.read()
   

class ReportRequest(BaseModel):
    date: str
    islamic_month: str
    islamic_year: str

# Load once at startup
DATA_DIR = "Data"
all_data_df = pd.DataFrame()
def load_files(path):
    global all_data_df
    all_data_df = load_all_files(path)
    return(all_data_df)

# Now pass df to MoonCalc
@app.on_event("startup")
def on_startup():
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(load_files(DATA_DIR))
    
@app.post("/generate-moon-parameters/")
def generate_moon_parameters(data: ReportRequest):
    try:
        df = all_data_df
        pdf_path = generate_pdf(df,data.date, data.islamic_month, data.islamic_year)  # Return full path to PDF
        return FileResponse(path=pdf_path, filename=pdf_path.split("\\")[-1], media_type='application/pdf')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.post("/generate-visibility-report/")
def generate_visibility_report(data: ReportRequest):
    df = all_data_df
    report = GenerateReport(df,data.date, data.islamic_month, data.islamic_year)
    pdf_path = report.run_all()  # Return full path to PDF
    return FileResponse(path=pdf_path, filename=pdf_path.split("\\")[-1], media_type='application/pdf')

# @app.post("/generate-report/")
# async def generate_report(data: ReportRequest):
#     report = GenerateReport(data.date, data.islamic_month, data.islamic_year)
#     pdf_path = report.run_all()  # Return full path to PDF
#     print(pdf_path)
#     return FileResponse(path=pdf_path, filename=pdf_path.split("\\")[-1], media_type='application/pdf')

