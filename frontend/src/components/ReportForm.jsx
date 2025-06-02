import './ReportForm.css';
import { useState } from 'react';
import InputWithLabel from './InputWithLabel';
import SelectMonth from './SelectMonth';
import ButtonGroup from './ButtonGroup';
import ResponseMessage from './ResponseMessage';

const backendURL = "https://moonai-backend.onrender.com"; // رابط الـ backend الخاص بك
//const backendURL = "http://127.0.0.1:8000";


function ReportForm() {
  const [date, setDate] = useState("28-05-2025");
  const [month, setMonth] = useState("");
  const [year, setYear] = useState(1446);
  const [responseMessage, setResponseMessage] = useState("");
  const [isError, setIsError] = useState(false);

  function generateReport(type) {

  if (!date || !month || !year) {
    setResponseMessage("Please fill in all fields before generating the report.");
    setIsError(true);
    return;
  }

    const formData = {
      date: date,   
      islamic_month: month,
      islamic_year: year.toString(),
    };

    let endpoint = type === "moon-parameters" 
      ? "/generate-moon-parameters/" 
      : "/generate-visibility-report/";

    fetch(`${backendURL}${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to generate report.");
        return response.blob();
      })
      .then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${type.replace("-", "_")}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setResponseMessage("Download started.");
        setIsError(false);
      })
      .catch(error => {
        setResponseMessage("Error: " + error.message);
        setIsError(true);
      });
  }

  return (
    <form id="reportForm" className="report-form">
      <h2>Moon Report Generator</h2>
      <InputWithLabel
        label="Date (DD-MM-YYYY):"
        id="date"
        value={date}
        onChange={e => setDate(e.target.value)}
      />
      <SelectMonth
        value={month}
        onChange={e => setMonth(e.target.value)}
      />
      <InputWithLabel
        label="Islamic Year:"
        id="year"
        type="number"
        value={year}
        onChange={e => setYear(Number(e.target.value))}
      />
      <ButtonGroup
        onGenerateMoonParameters={() => generateReport("moon-parameters")}
        onGenerateVisibilityReport={() => generateReport("visibility-report")}
      />
      <ResponseMessage message={responseMessage} isError={isError} />
    </form>
  );
}

export default ReportForm;
