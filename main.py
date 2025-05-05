#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from prompt import GenerateReport  # Adjust import based on your file location
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html") as f:
        return f.read()
   

class ReportRequest(BaseModel):
    date: str
    islamic_month: str
    islamic_year: str

@app.post("/generate-report/")
async def generate_report(data: ReportRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(GenerateReport(data.date, data.islamic_month, data.islamic_year).run_all)
    return {"message": "Report generation started in background."}


