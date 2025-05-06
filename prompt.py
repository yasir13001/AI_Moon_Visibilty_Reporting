from pdf_gene import MoonCalc, generate_pdf
from datetime import datetime
import requests
from tqdm import tqdm
import pandas as pd
from google import genai
import os
from dotenv import load_dotenv
import json
from markdown_pdf import MarkdownPdf, Section
from collections import Counter
import re
import webbrowser


class GenerateReport:
    def __init__(self, date: str, islamic_month: str, islamic_year: str):
        load_dotenv(dotenv_path='../.env')
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.date = date
        self.month = islamic_month
        self.year = islamic_year
        self.path = "Data"
        self.dst = "Output"
        self.df = None
        self.responses = []

    def prepare_dataframe(self):
        date_obj = datetime.strptime(self.date, "%d-%m-%Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")

        moon = MoonCalc(self.path, formatted_date, self.month, self.year + " AH", self.dst)
        df = moon.calculate()

        df[['Station', 'SunsetTime']] = df['STATION(Sunset)'].str.extract(r'^(.*?)\s*\((.*?)\)$')
        df.drop(columns=['STATION(Sunset)'], inplace=True)

        df = df[['Station', 'SunsetTime', 'LAG TIME(Minutes)', 'MOON ALTITUDE(Degrees)',
                 'SUN_AZIMUTH(Degrees)', 'DAZ(Degrees)', 'ELONGATION(Degrees)',
                 'ILLUMINATION(%)', 'CRITERION']]

        df.columns = ['Station', 'SunsetTime', 'LagTime', 'MoonAltitude', 'SunAzimuth',
                      'DAZ', 'Elongation', 'Illumination', 'Criterion']

        self.df = df

    def make_prompt(self, row):
        visibility_mapping = {
            'A': 'Easily visible',
            'B': 'Visible under perfect conditions',
            'C': 'May need optical aid to find the crescent Moon',
            'D': 'Will need optical aid to find the crescent Moon',
            'E': 'Not visible with a telescope',
            'F': 'Not visible, below the Danjon limit'
        }

        visibility_description = visibility_mapping.get(row['Criterion'], 'Unknown visibility criterion')
        illumination = float(row['Illumination'])
        moon_altitude = float(row['MoonAltitude'])

        illumination_description = (
            "The illumination is high, indicating good visibility."
            if illumination > 0.8 else
            "The illumination is low, which might make the Moon harder to see."
        )

        altitude_description = (
            "The Moon is high above the horizon, aiding visibility."
            if moon_altitude > 8 else
            "The Moon is low on the horizon, which may limit visibility."
        )

        return (
            "Here is the required format:\n"
            "{\n"
            "  \"Station\": \"...\",\n"
            "  \"visibility criterion\": \"...\",\n"
            "  \"Time\": \"...\",\n"
            "  \"Date\": \"...\",\n"
            "  \"Conclusion\": \"...\"\n"
            "}\n"
            "Answer based on the following data:\n"
            f"On {self.date}, at station {row['Station']}, at the time of Sunset {row['SunsetTime']}, "
            f"moon altitude {moon_altitude}°, illumination {illumination}%, "
            f"and visibility criterion '{row['Criterion']}': {visibility_description}. "
            f"{illumination_description} {altitude_description}. "
            f"Based on this data, explain whether the moon is likely to be visible and why."
        )

    def query_gemini(self, prompt):
        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text

    def get_ai_responses(self):
        tqdm.pandas()
        self.df['llama_response'] = self.df.progress_apply(
            lambda row: self.query_gemini(self.make_prompt(row)), axis=1
        )

    def sanitize_and_parse_json(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    return None
            return None

    def parse_responses(self):
        for content in self.df["llama_response"]:
            parsed = self.sanitize_and_parse_json(content)
            if parsed:
                self.responses.append(parsed)
            else:
                print("Invalid JSON after cleaning")

    def summarize_visibility_report(self, country="Pakistan"):
        conclusions = [entry['Conclusion'] for entry in self.responses]
        times = [entry['Time'] for entry in self.responses]
        dates = [entry['Date'] for entry in self.responses]

        most_common_conclusion, _ = Counter(conclusions).most_common(1)[0]
        most_common_time, _ = Counter(times).most_common(1)[0]
        most_common_date, _ = Counter(dates).most_common(1)[0]

        report = f"Moon Visibility Summary Report for {country}\n"
        report += f"Date: {most_common_date}\n"
        report += f"Typical Observation Time: Around {most_common_time}\n\n"
        report += "General Observation:\n"
        report += f"In most cities of {country}, the Moon is reported as:\n"
        report += f"{most_common_conclusion}\n\n"
        report += "Notable Differences:\n"
        differences_found = False

        for entry in self.responses:
            if entry['Conclusion'] != most_common_conclusion:
                differences_found = True
                report += (
                    f"- {entry['Station']} (on {entry['Date']} at {entry['Time']}):\n"
                    f"  {entry['Conclusion']}\n"
                )

        if not differences_found:
            report += "No significant differences observed across cities.\n"

        return report

    def generate_pdf_report(self):
        summary = self.summarize_visibility_report()
        prompt = f"""
You are provided with specific data about the moon's visibility, including altitude, illumination, and visibility criterion.
{summary}
Task:
- Write no introduction
- Summarize all text in one paragraph.
- Write structured report of findings
- Key Factors affecting moon visibilty
- Write Conclusion that says if moon visibility is high or low.
"""

        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
            content = response.text
        except Exception as e:
            # Optional: Log the full error
            print(f"Gemini API error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

        pdf = MarkdownPdf(toc_level=1, optimize=True)
        pdf.add_section(Section(content))
        pdf.meta["title"] = "Moon Visibility Report"
        pdf.meta["author"] = "Artificial Intelligence"
        # Ensure Output directory exists
        output_dir = os.path.join(os.path.dirname(__file__), "Output")
        os.makedirs(output_dir, exist_ok=True)  # Creates the directory if it doesn't exist

        # Save PDF to Output directory
        pdf_file = f"Visibility_report({self.date}).pdf"
        pdf_path = os.path.join(output_dir, pdf_file)
        pdf.save(pdf_path)

        # Open PDF in default browser
        #webbrowser.open_new(f"file://{os.path.abspath(pdf_path)}")
        return pdf_path
    
    def generate_params(self):
        return(generate_pdf(self.date,self.month,self.year))



    def run_all(self):
        self.prepare_dataframe()
        self.get_ai_responses()
        self.parse_responses()
        path = self.generate_pdf_report()
        return(path)

