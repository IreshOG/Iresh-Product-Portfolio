# Job AI

A polished Python/Streamlit job matching workspace. Paste or upload a job description and CV, then generate:

- Match score with skill, experience, and keyword breakdown
- Skills to lead with and gaps to address
- Tailored cover letter
- Cold email opener

## Run the Python app

From this folder:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown by Streamlit, usually `http://localhost:8501`.

## Original browser version

The original no-build browser version remains available in `index.html`, `styles.css`, and `app.js`.

## Run the browser version

Open `index.html` in a browser. No build step or API key is required.

The Python version reads PDF files locally through `pypdf`. The browser version uses PDF.js from a CDN when available.

## Notes

The analysis is intentionally local and deterministic. For production use, replace `analyze()` in `app.py` with a secure server-side AI integration and keep any API keys in environment variables.
