# 🌙 Moon Visibility Report Generator

An AI-powered Python tool for generating **lunar visibility reports** using **LLMs (Large Language Models)** such as **Gemini**, **Groq**, and **LLaMA3** (via **Ollama**). Designed for astronomers, developers, and researchers interested in **moon sighting**, **Hilal reports**, and **Islamic calendar computations**.

## 🚀 Features

* 🧠 **AI-Powered Reporting** – Uses advanced language models to generate descriptive moon visibility reports.
* ⚡ **Parallel Processing** – Boosted performance via `ThreadPoolExecutor` for concurrent prompt generation.
* 🗃️ **Dataset Integration** – Works with structured data using `pandas`, with real-time progress updates using `tqdm`.
* 💻 **Local + Cloud Models** – Supports local models via [Ollama](https://ollama.com) and cloud APIs like **Groq**, **Gemini**, etc.
* 🛰️ **Astronomical Accuracy** – Compatible with moon phase datasets and visibility criteria for precise reports.

## 🛠️ Tech Stack

* Python (3.9+)
* `pandas`, `tqdm`, `concurrent.futures`
* Gemini / Groq API (or any chat-completion LLM)
* Ollama (for local LLaMA3 or other open models)
* FastAPI (optional, for web API interface)

## 🌐 Use Cases

* Moon visibility reporting for Islamic calendar (Hilal sighting)
* Astronomical event tracking and reporting
* Educational tools for lunar phases
* Integration into observatory or planetarium dashboards

## 🔍 Keywords

```
moon report generator, lunar visibility, hilal sighting, ai moon report, llama3 moon, gemini groq, ollama moon visibility, moon phase api, astronomy ai, moon python, islamic calendar ai, llm moon sighting, moon visibility generator
```

## 📦 Example Usage

```python
generator = MoonReportGenerator()
prompts = generator.make_prompt(row)
responses = generator.generate_all(prompts)
```


