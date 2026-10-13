"""Job AI — a local Streamlit job/CV matching workspace."""

from __future__ import annotations

import re
from typing import Dict, List

import streamlit as st

try:
    from pypdf import PdfReader
except ImportError:  # PDF upload remains understandable if the optional dependency is absent.
    PdfReader = None


st.set_page_config(page_title="Job AI — Match with clarity", page_icon=":material/auto_awesome:", layout="wide")

SKILLS = [
    "product management", "product strategy", "roadmap", "roadmaps", "payments",
    "fintech", "saas", "apis", "api", "analytics", "sql", "data", "experimentation",
    "experiments", "user research", "discovery", "agile", "stakeholder management",
    "communication", "design", "engineering", "go-to-market", "metrics", "platform",
    "leadership", "javascript", "python", "figma", "a/b testing", "customer insights",
]

SAMPLE_JOB = """Senior Product Manager — Fintech Platform

We are looking for a customer-obsessed product leader to own the next generation of our payments platform. You will define product strategy, work with engineering and design, and turn complex problems into simple experiences.

Responsibilities
• Own the roadmap and product vision for our B2B payments platform
• Partner with engineering, design, data and go-to-market teams
• Use qualitative and quantitative insights to prioritize opportunities
• Define success metrics and communicate progress to senior stakeholders

Requirements
• 5+ years of product management experience in fintech or SaaS
• Experience with payments, APIs, and platform products
• Strong discovery, experimentation and analytical skills
• Excellent written and verbal communication"""

SAMPLE_CV = """Iresh Kumar
Product Manager | Fintech & SaaS

Product manager with 7 years of experience building B2B platforms and consumer fintech products. I turn customer insight and data into focused roadmaps that ship.

EXPERIENCE
Senior Product Manager, AcmePay — 2021–Present
• Owned roadmap for a payments API used by 2,000+ businesses; increased activation 32%.
• Partnered with engineering, design, sales and data across 3 squads.
• Shipped experimentation program that improved checkout conversion by 18%.
• Presented product strategy and metrics to executive leadership.

Product Manager, LaunchDesk — 2018–2021
• Led discovery, interviews and analytics for a B2B SaaS workflow product.
• Launched MVP in 12 weeks and grew weekly active users 40%.

SKILLS
Product strategy, roadmap planning, payments, APIs, SQL, analytics, experimentation, user research, stakeholder management, Agile

EDUCATION
BBA, University of Delhi"""


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
        :root { --navy:#16443a; --ink:#19342f; --muted:#6e817b; --line:#e4eee9; --lav:#7665d8; --mint:#c5f6d8; --green:#238c62; }
        .stApp { background:#f7fbf9; color:var(--ink); font-family:Manrope,sans-serif; }
        [data-testid="stSidebar"] { background:var(--navy); }
        [data-testid="stSidebar"] * { color:#d9e1ed; }
        [data-testid="stSidebar"] .stMarkdown h1 { color:#fff; letter-spacing:-1.5px; }
        .block-container { max-width:1180px; padding-top:2rem; padding-bottom:4rem; }
        h1,h2,h3 { font-family:Manrope,sans-serif; color:var(--ink); }
        h1 { font-size:3.1rem !important; letter-spacing:-2.5px; }
        h2 { letter-spacing:-1px; }
        .eyebrow { color:#8792a3; font:500 10px 'DM Mono',monospace; letter-spacing:1.4px; text-transform:uppercase; }
        .hero-copy { color:#637a72; max-width:560px; font-size:14px; line-height:1.8; }
        .hero-orbit { width:125px; height:125px; border:1px solid #bfe5d2; border-radius:50%; background:#ecfaf2; display:flex; align-items:center; justify-content:center; color:#2b9b6b; text-align:center; font-weight:800; box-shadow:0 12px 30px rgba(35,140,98,.10); }
        .card { background:#fff; border:1px solid var(--line); border-radius:15px; padding:22px; box-shadow:0 16px 50px rgba(24,76,59,.06); min-height:300px; }
        .card-title { font-size:17px; font-weight:800; margin-bottom:5px; }
        .card-helper { color:#8691a1; font-size:11px; margin-bottom:14px; }
        .step { color:#7d6bce; background:#f1efff; border-radius:5px; padding:6px; font:500 10px 'DM Mono',monospace; margin-right:9px; }
        .status { float:right; color:#138a58; font:500 9px 'DM Mono',monospace; }
        .stTextArea textarea { min-height:180px; font-family:Manrope,sans-serif; font-size:12px; line-height:1.65; }
        .stTextArea textarea, .stTextInput input { background:#fff !important; color:var(--ink) !important; border:1px solid #d6e7df !important; border-radius:8px !important; color-scheme:light; }
        .stTextArea textarea:focus, .stTextInput input:focus { border-color:#62b88b !important; box-shadow:0 0 0 3px rgba(98,184,139,.14) !important; }
        .stButton button, .stDownloadButton button { background:#fff; color:#277e5c; border-radius:8px; font-family:Manrope,sans-serif; font-weight:700; border-color:#d6e7df; }
        .stButton button:hover, .stDownloadButton button:hover { border-color:#8acdad; color:#16734d; }
        .stButton button[kind="primary"], .stButton button[data-testid="baseButton-primary"] { background:var(--green) !important; color:#fff !important; border-color:var(--green) !important; }
        .metric-card { background:#fff; border:1px solid var(--line); border-radius:10px; padding:16px; }
        .metric-label { display:block; color:#9ba5b2; font:500 9px 'DM Mono',monospace; margin-bottom:8px; }
        .metric-value { font-size:25px; font-weight:800; letter-spacing:-1px; }
        .pill { display:inline-block; background:#edf9f2; color:#23845b; border-radius:4px; padding:7px 8px; margin:3px; font-size:10px; }
        .pill.missing { background:#fff1e9; color:#c07552; }
        .report-box { background:#fff; border:1px solid var(--line); border-radius:14px; padding:22px; margin-bottom:16px; }
        .score { color:var(--green); font-size:48px; font-weight:800; letter-spacing:-3px; }
        .small-muted { color:#8792a2; font-size:11px; line-height:1.7; }
        footer { border-top:1px solid var(--line); padding-top:18px; margin-top:70px; color:#a3acb9; font:9px 'DM Mono',monospace; letter-spacing:.5px; }
        @media (max-width:700px) { h1 { font-size:2.4rem !important; } .hero-orbit { display:none; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def clean(text: str) -> str:
    return re.sub(r"[^a-z0-9+/#.\s-]", " ", text.lower())


def meaningful(text: str) -> bool:
    return len(re.findall(r"[a-z]", text, re.I)) >= 20


def extract_skills(text: str) -> List[str]:
    haystack = clean(text)
    return list(dict.fromkeys(
        skill for skill in SKILLS
        if re.search(rf"(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])", haystack, re.I)
    ))


def experience_years(text: str) -> int:
    match = re.search(r"(\d+)\s*\+?\s*years?", text, re.I)
    if match:
        return int(match.group(1))
    dates = re.findall(r"20\d\s?[-–]\s?(?:20\d|Present)", text, re.I)
    return min(15, len(dates) * 2)


def title_case(value: str) -> str:
    return value.replace("a/b testing", "A/B testing").title()


def analyze(job: str, cv: str) -> Dict:
    job_skills = extract_skills(job)
    cv_skills = extract_skills(cv)
    matched = [skill for skill in job_skills if skill in cv_skills]
    missing = [skill for skill in job_skills if skill not in cv_skills]
    skill_score = round(len(matched) / max(len(job_skills), 1) * 100)
    cv_years = experience_years(cv)
    required = re.search(r"(\d+)\s*\+?\s*years?", job, re.I)
    required_years = int(required.group(1)) if required else 0
    experience_score = min(100, round(cv_years / required_years * 100)) if required_years else 75
    keyword_score = min(100, 55 + round(len(matched) / max(len(job_skills), 1) * 45))
    score = round(skill_score * .5 + experience_score * .25 + keyword_score * .25)
    role_match = re.search(r"(?:looking for|role of|position of|seeking)\s+(?:a\s+)?([^\n,.]+)", job, re.I)
    role = role_match.group(1).strip() if role_match else "this role"
    name_match = re.search(r"^([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){1,3})", cv, re.M)
    name = name_match.group(1).strip() if name_match else "Your Name"
    return {"job_skills":job_skills, "cv_skills":cv_skills, "matched":matched, "missing":missing,
            "skill_score":skill_score, "experience_score":experience_score, "keyword_score":keyword_score,
            "score":score, "years":cv_years, "role":role, "name":name}


def writing(report: Dict) -> Dict[str, str]:
    lead_skills = ", ".join(title_case(x) for x in report["matched"][:3]) or "your transferable product experience"
    gaps = " and ".join(title_case(x) for x in report["missing"][:2]) or "the team’s product goals"
    role = title_case(report["role"])
    name = report["name"]
    letter = f"""Dear Hiring Manager,

I’m excited to apply for the {role} role. With {report['years'] or 'several'} years of experience across {lead_skills}, I’ve built a track record of turning customer problems into measurable product outcomes.

In my recent work, I owned product decisions from discovery through delivery, partnered closely with cross-functional teams, and used evidence to focus roadmaps. That maps closely to what your team needs as it scales {gaps}.

I’d welcome the chance to bring that mix of product judgment, execution, and customer empathy to your team. Thank you for your consideration.

Best,
{name}"""
    email = f"""Subject: Product perspective for {role}

Hi [Hiring Manager],

I came across the {role} opening and noticed the focus on {lead_skills}. In my recent role, I used a similar approach to turn a complex customer problem into a clearer product experience and a measurable result.

I’d love to share a little more context on how I could help with {gaps}. Would a 15-minute conversation next week be useful?

Best,
{name}"""
    return {"letter":letter, "email":email}


def uploaded_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    if uploaded_file.name.lower().endswith(".txt"):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    if uploaded_file.name.lower().endswith(".pdf"):
        if PdfReader is None:
            st.warning("Install pypdf to read PDFs: pip install pypdf")
            return ""
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return ""


def use_sample_job() -> None:
    st.session_state["job_input"] = SAMPLE_JOB
    st.session_state["job_text"] = SAMPLE_JOB


def use_sample_cv() -> None:
    st.session_state["cv_input"] = SAMPLE_CV
    st.session_state["cv_text"] = SAMPLE_CV


def pills(values: List[str], missing: bool = False) -> str:
    css = " pill missing" if missing else " pill"
    return "".join(f'<span class="{css.strip()}">{title_case(value)}</span>' for value in values) or '<span class="small-muted">No major keyword gaps found</span>'


inject_styles()

with st.sidebar:
    st.markdown("# ✦ job<span style='color:#c5f6d8'>ai</span>", unsafe_allow_html=True)
    st.caption("CAREER INTELLIGENCE")
    st.markdown("### ◒ Match analysis")
    st.markdown("### ⌁ Your report")
    st.markdown("### ✎ Writing studio")
    st.divider()
    st.markdown("**◉ Private by design**")
    st.caption("Your documents are processed locally in this app.")

st.markdown('<div class="eyebrow">A SHARPER WAY TO APPLY</div>', unsafe_allow_html=True)
hero_left, hero_right = st.columns([4, 1])
with hero_left:
    st.title("Find the clearest path to yes.")
    st.markdown('<p class="hero-copy">Add a role and your CV. Job AI turns the overlap into a calm, practical plan for your next application.</p>', unsafe_allow_html=True)
with hero_right:
    st.markdown('<div class="hero-orbit">✦<br><small>AI career co-pilot</small></div>', unsafe_allow_html=True)
st.markdown('<p class="small-muted">✦ Private by design &nbsp;&nbsp; ◌ Practical insights &nbsp;&nbsp; ↗ Ready-to-use writing</p>', unsafe_allow_html=True)

st.markdown("## 01 / Start with two simple inputs")
st.markdown('<p class="small-muted">No perfect formatting needed — paste what you have and we’ll help you make sense of it.</p>', unsafe_allow_html=True)
job_col, cv_col = st.columns(2, gap="medium")
with job_col:
    st.markdown('<div class="card-title"><span class="step">01</span>Job description <span class="status">TEXT / PDF</span></div><div class="card-helper">Paste the role or upload a .txt / .pdf file.</div>', unsafe_allow_html=True)
    job_file = st.file_uploader("Upload job description", type=["txt", "pdf"], key="job_upload", label_visibility="collapsed")
    if job_file:
        st.session_state["job_input"] = uploaded_text(job_file)
        st.session_state["job_text"] = st.session_state["job_input"]
    job_text = st.text_area("Paste the job description here", value=st.session_state.get("job_text", ""), height=220, key="job_input", placeholder="Include responsibilities, requirements, and skills.")
    st.button("Use sample role", key="sample_job", on_click=use_sample_job)
with cv_col:
    st.markdown('<div class="card-title"><span class="step">02</span>Your CV <span class="status">TEXT / PDF</span></div><div class="card-helper">Give us the context behind your experience.</div>', unsafe_allow_html=True)
    cv_file = st.file_uploader("Upload CV", type=["txt", "pdf"], key="cv_upload", label_visibility="collapsed")
    if cv_file:
        st.session_state["cv_input"] = uploaded_text(cv_file)
        st.session_state["cv_text"] = st.session_state["cv_input"]
    cv_text = st.text_area("Paste your CV content here", value=st.session_state.get("cv_text", ""), height=220, key="cv_input", placeholder="Include experience, projects, education, and skills.")
    st.button("Use sample CV", key="sample_cv", on_click=use_sample_cv)

st.session_state["job_text"] = job_text
st.session_state["cv_text"] = cv_text
st.markdown('<p class="small-muted">✦ Private, practical, and processed locally in this browser session.</p>', unsafe_allow_html=True)
if st.button("Analyze match  →", type="primary"):
    if not job_text.strip() or not cv_text.strip():
        st.session_state.pop("report", None)
        st.session_state.pop("writing", None)
        st.warning("Add both a job description and CV to continue.")
    elif not meaningful(job_text) or not meaningful(cv_text):
        st.session_state.pop("report", None)
        st.session_state.pop("writing", None)
        st.warning("Please provide more meaningful job and CV content.")
    else:
        st.session_state["report"] = analyze(job_text, cv_text)
        st.session_state["writing"] = writing(st.session_state["report"])
        st.success("Your report is ready.")

st.markdown("## 03 / Your match report")
if "report" not in st.session_state:
    st.info("You’re only two inputs away from a clearer application. We’ll highlight what already works, what to strengthen, and what to say next.")
else:
    report = st.session_state["report"]
    score = report["score"]
    top_left, top_right = st.columns([1.15, 1], gap="medium")
    with top_left:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="score">{score}<small style="font-size:14px;color:#8792a2"> / 100</small></div>', unsafe_allow_html=True)
        st.subheader("Strong match with a clear story." if score >= 80 else "Promising match — sharpen the story.")
        st.markdown('<p class="small-muted">Based on the overlap between the role requirements and the evidence in your CV. Your best opportunity is to make the relevant wins impossible to miss.</p>', unsafe_allow_html=True)
        st.markdown("<span class='pill'>HIGH CONFIDENCE</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with top_right:
        st.markdown('<div class="report-box"><h3>What stands out</h3>', unsafe_allow_html=True)
        for skill in report["matched"][:3] or ["transferable product experience"]:
            st.markdown(f"✦ Your CV shows credible evidence of **{title_case(skill)}** — keep this near the top of your application.")
        st.markdown('</div>', unsafe_allow_html=True)

    metric_cols = st.columns(4)
    metrics = [("SKILL OVERLAP", report["skill_score"], "%"), ("EXPERIENCE FIT", report["experience_score"], "%"), ("KEYWORD SIGNAL", report["keyword_score"], "%"), ("CV EXPERIENCE", report["years"] or "—", "yrs" if report["years"] else "n/a")]
    for col, (label, value, suffix) in zip(metric_cols, metrics):
        with col:
            st.markdown(f'<div class="metric-card"><span class="metric-label">{label}</span><span class="metric-value">{value}<small style="font-size:10px;color:#8994a2"> {suffix}</small></span></div>', unsafe_allow_html=True)

    detail_left, detail_right = st.columns(2, gap="medium")
    with detail_left:
        st.markdown(f'<div class="report-box"><h3>Skills to lead with</h3>{pills(report["matched"])}</div>', unsafe_allow_html=True)
    with detail_right:
        st.markdown(f'<div class="report-box"><h3>Gaps to address</h3>{pills(report["missing"][:7], True)}</div>', unsafe_allow_html=True)
    gap_text = " and ".join(title_case(x) for x in report["missing"][:2]) or "the company’s product challenge"
    st.markdown(f'<div class="report-box"><h3>Recommended next move</h3><p class="small-muted">→ Add a short “Relevant experience” line or bullet that addresses <strong>{gap_text}</strong>. Quantify the outcome wherever possible.</p></div>', unsafe_allow_html=True)

    st.markdown("## 04 / Writing studio")
    write_left, write_right = st.columns(2, gap="medium")
    for col, title, key in [(write_left, "Tailored cover letter", "letter"), (write_right, "Cold email opener", "email")]:
        with col:
            st.markdown(f'<div class="report-box"><h3>{title}</h3>', unsafe_allow_html=True)
            st.text_area(title, st.session_state["writing"][key], height=350, key=f"output_{key}", label_visibility="collapsed")
            st.download_button(f"Download {key}", st.session_state["writing"][key], file_name=f"job_ai_{key}.txt", key=f"download_{key}")
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<footer>JOB AI / PYTHON EDITION <span style="float:right">BUILT FOR BETTER APPLICATIONS ✦</span></footer>', unsafe_allow_html=True)
