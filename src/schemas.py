from pydantic import BaseModel


class ReportRequest(BaseModel):
    date: str
    islamic_month: str
    islamic_year: str
