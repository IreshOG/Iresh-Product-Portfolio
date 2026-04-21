# Recruit AI

This folder contains the full Recruit AI project package, including the n8n workflow definition and supporting project documentation.

## Folder Contents

- `Final Project Iresh.docx` - Final project deliverable (Word document).
- `Final Project Iresh.pdf` - Final project deliverable (PDF export).
- `n8n_json_new.json` - n8n workflow definition for the Recruit AI automation.
- `PM Project Recuite AI.docx` - Project planning / documentation file.
- `Recruit-AI Metrics and Roadmap.docx` - Metrics, roadmap, and planning details.
- `Recruit-ai Problem Framing Document.docx` - Problem framing and user/recruitment context.
- `Recruit-AI_ Process & Decision Log.docx` - Project process notes and decision log.
- `RecuitAI PPT.pptx` - Presentation deck for the Recruit AI project.

## n8n Workflow Summary (`n8n_json_new.json`)

The workflow file is an n8n JSON export that defines the Recruit AI automation flow. Key nodes and actions include:

- `Extract Resume Text`: Extracts text from uploaded PDF resumes.
- `Resume Analysis AI Agent`: Uses an AI agent to analyze resumes and generate candidate insights.
- `Candidate Info Extractor`: Parses candidate information from AI output.
- `Normalize Candidate Info`: Standardizes candidate fields like name, email, phone, and city.
- `Parse Merged Output`: Converts AI output and scoring data into structured fields.
- `Store Analysis Results`: Writes candidate score, status, email, and name into a data table.
- `Send Rejection Email Draft`: Sends a draft rejection email using Gmail.
- `Send Interview Email Draft`: Sends a draft interview invitation email using Gmail.
- `Create Interview Event`: Schedules an interview event in Google Calendar.
- `Google Gemini Chat Model` nodes: Connect to Google Gemini / PaLM API for AI language model operations.

## Workflow Notes

- The JSON file includes credential references for Gmail, Google Calendar, and Google Palm API connections.
- The workflow uses custom JavaScript nodes to parse and normalize AI responses.
- Status logic is applied to decide interview vs reject recommendations.

## How to use

1. Open `n8n_json_new.json` in n8n by importing the workflow JSON.
2. Open the Word/PDF files with Microsoft Word or a compatible viewer.
3. Open `RecuitAI PPT.pptx` in PowerPoint or an equivalent presentation app.

## Notes

- This `README.md` documents all files currently present in the `Recruit AI` folder.
- The binary documents (`.docx`, `.pdf`, `.pptx`) are included in the folder and can be opened with standard office tools.
- For the full workflow definition and all node settings, refer to `n8n_json_new.json`.
