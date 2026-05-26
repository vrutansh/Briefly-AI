import streamlit as st
import time
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

st.set_page_config(
    page_title="BrieflyAI · Video Intelligence",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Clash+Display:wght@400;500;600;700&family=Cabinet+Grotesk:wght@300;400;500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Epilogue:wght@300;400;500;700;800;900&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');

:root {
  --ink:        #0d0d12;
  --ink2:       #13131c;
  --ink3:       #1c1c2a;
  --rim:        #252538;
  --rim2:       #32324a;
  --lime:       #c8f135;
  --lime-dim:   rgba(200,241,53,0.12);
  --lime-glow:  rgba(200,241,53,0.25);
  --sky:        #38bdf8;
  --sky-dim:    rgba(56,189,248,0.1);
  --rose:       #fb7185;
  --amber:      #fbbf24;
  --text:       #e8e8f2;
  --muted:      #6b6b8d;
  --radius:     16px;
}

/* ── GLOBAL ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp, [data-testid="stAppViewContainer"] {
  background: var(--ink) !important;
  font-family: 'Instrument Sans', sans-serif;
  color: var(--text);
}

/* subtle noise grain */
.stApp::after {
  content: '';
  position: fixed; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 9999;
  opacity: .5;
}

/* hide chrome */
#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stHeader"] { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--ink2) !important;
  border-right: 1px solid var(--rim) !important;
}
[data-testid="stSidebar"] > div { padding: 1.8rem 1.4rem !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }

.brand {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 0.2rem;
}
.brand-icon {
  width: 36px; height: 36px; border-radius: 10px;
  background: var(--lime);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; flex-shrink: 0;
  box-shadow: 0 0 18px var(--lime-glow);
}
.brand-name {
  font-family: 'Epilogue', sans-serif;
  font-size: 1.35rem; font-weight: 900;
  color: var(--text) !important;
  letter-spacing: -0.03em;
}
.brand-tag {
  font-size: 0.65rem; font-weight: 500;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--muted) !important;
  margin-bottom: 1.6rem;
}

.sidebar-section {
  font-size: 0.6rem; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--muted) !important;
  margin: 1.4rem 0 0.6rem;
  display: flex; align-items: center; gap: 6px;
}
.sidebar-section::after {
  content: ''; flex: 1; height: 1px; background: var(--rim);
}

/* inputs */
[data-testid="stTextInput"] input {
  background: var(--ink3) !important;
  border: 1px solid var(--rim) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: 0.85rem !important;
  padding: 0.65rem 0.9rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--lime) !important;
  box-shadow: 0 0 0 3px var(--lime-dim) !important;
  outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--muted) !important; }
[data-testid="stTextInput"] label { display: none !important; }

[data-testid="stSelectbox"] label { display: none !important; }
[data-testid="stSelectbox"] > div > div {
  background: var(--ink3) !important;
  border: 1px solid var(--rim) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: 0.85rem !important;
}

/* lang pills */
.lang-pill-row { display: flex; gap: 8px; margin: 0.4rem 0 1rem; flex-wrap: wrap; }
.lang-pill {
  padding: 5px 14px; border-radius: 100px;
  font-size: 0.75rem; font-weight: 600;
  border: 1px solid var(--rim2); color: var(--muted);
  cursor: pointer; transition: all 0.18s;
  background: var(--ink3);
}
.lang-pill.selected {
  background: var(--lime); color: var(--ink);
  border-color: var(--lime);
  box-shadow: 0 0 12px var(--lime-glow);
}

/* analyse button */
.stButton > button {
  background: var(--lime) !important;
  color: var(--ink) !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Epilogue', sans-serif !important;
  font-size: 0.82rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  padding: 0.65rem 1.4rem !important;
  transition: all 0.2s !important;
  box-shadow: 0 4px 20px var(--lime-glow) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px rgba(200,241,53,0.38) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* secondary / clear */
button[kind="secondary"], .clear-btn > button {
  background: var(--ink3) !important;
  color: var(--muted) !important;
  border: 1px solid var(--rim) !important;
  box-shadow: none !important;
}

/* ── STEP TRACKER (sidebar) ── */
.step-row {
  display: flex; align-items: center; gap: 10px;
  padding: 7px 10px; border-radius: 9px;
  margin: 3px 0; font-size: 0.78rem;
  transition: background 0.2s;
}
.step-row.done   { background: rgba(200,241,53,0.07); }
.step-row.active { background: rgba(200,241,53,0.12); }
.step-row.pending{ opacity: 0.45; }

.step-dot {
  width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
}
.dot-done    { background: var(--lime); box-shadow: 0 0 6px var(--lime); }
.dot-active  { background: var(--amber); box-shadow: 0 0 8px var(--amber); animation: blink 1.2s ease-in-out infinite; }
.dot-pending { background: var(--rim2); }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

.step-check { color: var(--lime); font-size: 0.7rem; flex-shrink:0; }
.step-label { color: var(--text); }
.step-row.done .step-label { color: rgba(200,241,53,0.85); }
.step-row.active .step-label { color: var(--amber); }

/* ── MAIN CANVAS ── */
.main-wrap { padding: 2rem 2.5rem 4rem; max-width: 1200px; margin: 0 auto; }

/* hero */
.page-hero { margin-bottom: 2.5rem; }
.page-eyebrow {
  font-size: 0.65rem; font-weight: 700; letter-spacing: 0.25em;
  text-transform: uppercase; color: var(--lime);
  display: flex; align-items: center; gap: 6px; margin-bottom: 0.5rem;
}
.page-eyebrow::before { content:''; width:18px; height:1px; background:var(--lime); }
.page-h1 {
  font-family: 'Epilogue', sans-serif;
  font-size: clamp(2.2rem,4.5vw,3.8rem);
  font-weight: 900; letter-spacing: -0.04em;
  color: var(--text); line-height: 1.05; margin: 0 0 0.5rem;
}
.page-h1 em { font-style: normal; color: var(--lime); }
.page-sub {
  font-size: 0.9rem; color: var(--muted); max-width: 480px; line-height: 1.65;
}

/* feature pills (landing) */
.feat-row { display:flex; gap:8px; flex-wrap:wrap; margin-top:1.6rem; }
.feat-pill {
  padding: 5px 13px; border-radius: 100px;
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.04em;
  border: 1px solid var(--rim2); color: var(--muted);
  background: var(--ink2);
}

/* ── RESULT CARDS ── */
.r-card {
  background: var(--ink2);
  border: 1px solid var(--rim);
  border-radius: var(--radius);
  padding: 1.4rem 1.5rem;
  margin-bottom: 1.1rem;
  position: relative; overflow: hidden;
  transition: border-color 0.2s, transform 0.2s;
}
.r-card:hover { border-color: var(--rim2); transform: translateY(-1px); }

.r-card-accent {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 2px;
}
.acc-lime  { background: linear-gradient(90deg, var(--lime), transparent 70%); }
.acc-sky   { background: linear-gradient(90deg, var(--sky),  transparent 70%); }
.acc-rose  { background: linear-gradient(90deg, var(--rose), transparent 70%); }
.acc-amber { background: linear-gradient(90deg, var(--amber),transparent 70%); }

.r-card-label {
  font-size: 0.6rem; font-weight: 700;
  letter-spacing: 0.22em; text-transform: uppercase;
  margin-bottom: 0.8rem; display: flex; align-items: center; gap: 7px;
}
.lbl-lime  { color: var(--lime); }
.lbl-sky   { color: var(--sky);  }
.lbl-rose  { color: var(--rose); }
.lbl-amber { color: var(--amber);}
.lbl-muted { color: var(--muted);}

.r-title {
  font-family: 'Epilogue', sans-serif;
  font-size: 1.55rem; font-weight: 800;
  color: var(--text); letter-spacing: -0.025em; line-height: 1.25;
}
.r-body { font-size: 0.88rem; line-height: 1.78; color: rgba(232,232,242,0.82); }

.list-line {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 0.85rem; color: rgba(232,232,242,0.8); line-height: 1.6;
}
.list-line:last-child { border-bottom: none; }
.list-bullet {
  width: 5px; height: 5px; border-radius: 50%;
  margin-top: 0.55rem; flex-shrink: 0;
}

/* transcript */
.tx-box {
  background: rgba(0,0,0,0.25); border-radius: 10px;
  padding: 1.1rem 1.3rem;
  font-size: 0.82rem; line-height: 1.85;
  color: var(--muted); font-style: italic;
  max-height: 260px; overflow-y: auto;
  scrollbar-width: thin; scrollbar-color: var(--rim2) transparent;
}

/* ── CHAT ── */
.chat-wrap {
  background: var(--ink2); border: 1px solid var(--rim);
  border-radius: var(--radius); padding: 1.3rem 1.4rem;
  max-height: 400px; overflow-y: auto; margin-bottom: 1rem;
  scrollbar-width: thin; scrollbar-color: var(--rim2) transparent;
}
.chat-empty {
  text-align:center; padding:2.5rem 1rem;
  color:var(--muted); font-size:0.85rem;
}
.chat-empty-icon { font-size:2.2rem; margin-bottom:0.6rem; }

.cmsg { margin-bottom: 1.1rem; }
.cmsg-label {
  font-size: 0.6rem; font-weight: 700; letter-spacing: 0.16em;
  text-transform: uppercase; margin-bottom: 0.25rem;
}
.cmsg-label.you { color: var(--lime); text-align: right; }
.cmsg-label.bot { color: var(--sky); }

.cbubble {
  display: inline-block; padding: 0.65rem 1.05rem;
  border-radius: 14px; font-size: 0.87rem; line-height: 1.65; max-width: 88%;
}
.cbubble.you {
  background: rgba(200,241,53,0.1); border: 1px solid rgba(200,241,53,0.2);
  float: right; border-radius: 14px 14px 4px 14px;
}
.cbubble.bot {
  background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.18);
  float: left; border-radius: 14px 14px 14px 4px;
}
.cmsg::after { content:''; display:table; clear:both; }

/* quick Qs */
.quick-row { display:flex; gap:8px; flex-wrap:wrap; margin-top:0.8rem; }
.quick-pill {
  padding: 5px 13px; border-radius: 100px;
  font-size: 0.73rem; font-weight: 500;
  background: var(--ink3); border: 1px solid var(--rim2);
  color: var(--muted); cursor: pointer; transition: all 0.16s;
}
.quick-pill:hover { border-color: var(--lime); color: var(--lime); }

/* section heading */
.section-head {
  font-family: 'Epilogue', sans-serif;
  font-size: 1.05rem; font-weight: 800;
  color: var(--text); letter-spacing: -0.02em;
  margin: 2rem 0 0.9rem;
  display: flex; align-items: center; gap: 10px;
}
.section-head::after {
  content:''; flex:1; height:1px; background:var(--rim); margin-left:4px;
}

/* divider */
.ff-hr { border:none; border-top:1px solid var(--rim); margin:2rem 0; }

/* processing overlay */
.proc-card {
  background: var(--ink2); border: 1px solid var(--rim);
  border-radius: var(--radius); padding: 2rem 2rem 1.8rem;
  margin-bottom:1rem; text-align:center;
}
.proc-title {
  font-family:'Epilogue',sans-serif;
  font-size:1.1rem; font-weight:800; color:var(--text);
  margin-bottom:0.4rem;
}
.proc-sub { font-size:0.8rem; color:var(--muted); }

/* streamlit overrides */
.stProgress > div > div > div { background: var(--lime) !important; }
.stSpinner > div { border-top-color: var(--lime) !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
label { color: var(--muted) !important; font-size:0.78rem !important; }
[data-testid="stExpander"] {
  background: var(--ink2) !important;
  border: 1px solid var(--rim) !important;
  border-radius: 12px !important;
}

::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--rim2); border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:var(--lime); }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in {
    "result": None,
    "chat_history": [],
    "pipeline_done": False,
    "pipeline_steps": {},
    "language": "english",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-icon">🔥</div>
      <span class="brand-name">BrieflyAI</span>
    </div>
    <div class="brand-tag">Video Intelligence</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Source</div>', unsafe_allow_html=True)
    source = st.text_input("url", label_visibility="collapsed",
        placeholder="YouTube URL or /path/to/file.mp4")

    st.markdown('<div class="sidebar-section">Language</div>', unsafe_allow_html=True)

    l1, l2, l3 = st.columns(3)
    with l1:
        if st.button("EN", use_container_width=True, key="l_en"):
            st.session_state.language = "english"
    # with l2:
    #     if st.button("HI", use_container_width=True, key="l_hi"):
    #         st.session_state.language = "hindi"
    with l3:
        if st.button("MIX", use_container_width=True, key="l_hg"):
            st.session_state.language = "hinglish"

    st.markdown(
        f"<p style='font-size:0.72rem;color:rgba(200,241,53,0.7);margin:0.3rem 0 1rem;'>"
        f"● {st.session_state.language.title()}</p>",
        unsafe_allow_html=True
    )

    run_btn = st.button("⚡  Analyse Video", use_container_width=True)

    # Pipeline steps
    if st.session_state.pipeline_done or st.session_state.pipeline_steps:
        st.markdown('<div class="sidebar-section" style="margin-top:1.6rem">Pipeline</div>', unsafe_allow_html=True)

        STEPS = [
            ("audio",      "🔊", "Audio"),
            ("transcript", "✍️",  "Transcription"),
            ("title",      "🏷️",  "Title"),
            ("summary",    "📋", "Summary"),
            ("extract",    "🔍", "Extraction"),
            ("rag",        "🧠", "RAG Engine"),
        ]
        for key, icon, label in STEPS:
            s = st.session_state.pipeline_steps.get(key, "pending")
            dot_cls   = f"dot-{s}"
            row_cls   = s
            check     = "✓" if s == "done" else ""
            st.markdown(f"""
            <div class="step-row {row_cls}">
              <div class="step-dot {dot_cls}"></div>
              <span class="step-label">{icon} {label}</span>
              <span class="step-check" style="margin-left:auto">{check}</span>
            </div>""", unsafe_allow_html=True)

    if st.session_state.result:
        st.markdown('<div class="ff-hr"></div>', unsafe_allow_html=True)
        if st.button("↩ New Video", use_container_width=True, key="reset"):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.session_state.pipeline_done = False
            st.session_state.pipeline_steps = {}
            st.rerun()

# ── Main ───────────────────────────────────────────────────────────────────────
with st.container():

    # ── Landing / empty state ────────────────────────────────────────────────
    if not st.session_state.result and not st.session_state.pipeline_steps:
        st.markdown("""
        <div class="page-hero">
          <div class="page-eyebrow">AI Video Intelligence</div>
          <h1 class="page-h1">Understand any video<br><em>in seconds.</em></h1>
          <p class="page-sub">
            Drop a YouTube link or local file. Firefly transcribes, summarises,
            extracts decisions & actions — then lets you chat with the content.
          </p>
          <div class="feat-row">
            <span class="feat-pill">🎙 Transcription</span>
            <span class="feat-pill">📋 Summary</span>
            <span class="feat-pill">✅ Action Items</span>
            <span class="feat-pill">🔑 Decisions</span>
            <span class="feat-pill">❓ Open Questions</span>
            <span class="feat-pill">💬 RAG Chat</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:var(--ink2);border:1px dashed var(--rim2);
             border-radius:var(--radius);padding:3rem 2rem;text-align:center;margin-top:1rem">
          <div style="font-size:3rem;margin-bottom:0.75rem">🔥</div>
          <div style="font-family:'Epilogue',sans-serif;font-size:1rem;font-weight:800;
               color:var(--text);margin-bottom:0.4rem">Ready when you are</div>
          <div style="font-size:0.82rem;color:var(--muted)">
            Paste a URL in the sidebar and hit <strong style="color:var(--lime)">Analyse Video</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Run pipeline ─────────────────────────────────────────────────────────
    if run_btn:
        if not source.strip():
            st.error("Please enter a YouTube URL or file path.")
        else:
            st.session_state.pipeline_done = False
            st.session_state.result = None
            st.session_state.chat_history = []
            st.session_state.pipeline_steps = {}

            prog_ph = st.empty()

            def upd(key, state):
                st.session_state.pipeline_steps[key] = state

            try:
                prog_ph.markdown("""
                <div class="proc-card">
                  <div class="proc-title">🔥 Firefly is working…</div>
                  <div class="proc-sub">Check the pipeline tracker in the sidebar</div>
                </div>""", unsafe_allow_html=True)

                upd("audio", "active")
                chunks = process_input(source)
                upd("audio", "done")

                upd("transcript", "active")
                transcript = transcribe_all(chunks, st.session_state.language)
                upd("transcript", "done")

                upd("title", "active")
                title = generate_title(transcript)
                upd("title", "done")

                upd("summary", "active")
                summary = summarize(transcript)
                upd("summary", "done")

                upd("extract", "active")
                action_items = extract_action_items(transcript)
                decisions    = extract_key_decisions(transcript)
                questions    = extract_questions(transcript)
                upd("extract", "done")

                upd("rag", "active")
                rag_chain = build_rag_chain(transcript)
                upd("rag", "done")

                st.session_state.result = {
                    "title": title, "transcript": transcript,
                    "summary": summary, "action_items": action_items,
                    "key_decisions": decisions, "open_questions": questions,
                    "rag_chain": rag_chain,
                }
                st.session_state.pipeline_done = True
                prog_ph.empty()
                st.rerun()

            except Exception as e:
                for k in ["audio","transcript","title","summary","extract","rag"]:
                    if st.session_state.pipeline_steps.get(k) == "active":
                        st.session_state.pipeline_steps[k] = "pending"
                prog_ph.error(f"❌ {e}")

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.result:
        r = st.session_state.result

        # Title
        st.markdown(f"""
        <div class="r-card">
          <div class="r-card-accent acc-lime"></div>
          <div class="r-card-label lbl-lime">📌 Detected Title</div>
          <div class="r-title">{r['title']}</div>
        </div>""", unsafe_allow_html=True)

        # Summary + Transcript
        sc1, sc2 = st.columns([3, 2], gap="medium")
        with sc1:
            st.markdown(f"""
            <div class="r-card" style="height:100%">
              <div class="r-card-accent acc-sky"></div>
              <div class="r-card-label lbl-sky">📋 Summary</div>
              <div class="r-body">{r['summary']}</div>
            </div>""", unsafe_allow_html=True)
        with sc2:
            with st.expander("📄 Full Transcript", expanded=False):
                st.markdown(f'<div class="tx-box">{r["transcript"]}</div>',
                            unsafe_allow_html=True)

        # Insights row
        st.markdown('<div class="section-head">Extracted Insights</div>',
                    unsafe_allow_html=True)

        ic1, ic2, ic3 = st.columns(3, gap="medium")

        def insight_card(text, label, icon, acc_cls, lbl_cls, dot_color):
            lines = [l.strip("•-–* ").strip()
                     for l in str(text).split("\n") if l.strip("•-–* ").strip()]
            rows = "".join(
                f'<div class="list-line">'
                f'<div class="list-bullet" style="background:{dot_color}"></div>'
                f'<span>{ln}</span></div>'
                for ln in lines
            ) or '<span style="color:var(--muted);font-size:0.82rem">None identified</span>'
            return f"""
            <div class="r-card" style="height:100%">
              <div class="r-card-accent {acc_cls}"></div>
              <div class="r-card-label {lbl_cls}">{icon} {label}</div>
              <div>{rows}</div>
            </div>"""

        with ic1:
            st.markdown(insight_card(r["action_items"], "Action Items",
                "✅", "acc-lime", "lbl-lime", "var(--lime)"), unsafe_allow_html=True)
        with ic2:
            st.markdown(insight_card(r["key_decisions"], "Key Decisions",
                "🔑", "acc-amber", "lbl-amber", "var(--amber)"), unsafe_allow_html=True)
        with ic3:
            st.markdown(insight_card(r["open_questions"], "Open Questions",
                "❓", "acc-rose", "lbl-rose", "var(--rose)"), unsafe_allow_html=True)

        # ── RAG Chat ─────────────────────────────────────────────────────────
        st.markdown('<div class="section-head">Chat with the Video</div>',
                    unsafe_allow_html=True)

        # History
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        if not st.session_state.chat_history:
            st.markdown("""
            <div class="chat-empty">
              <div class="chat-empty-icon">💬</div>
              Ask anything — Firefly has read every word of the video.
            </div>""", unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="cmsg">
                      <div class="cmsg-label you">You</div>
                      <div class="cbubble you">{msg['content']}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="cmsg">
                      <div class="cmsg-label bot">🔥 Firefly</div>
                      <div class="cbubble bot">{msg['content']}</div>
                    </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Input row
        qi1, qi2 = st.columns([5, 1], gap="small")
        with qi1:
            user_q = st.text_input("q", label_visibility="collapsed",
                placeholder="What were the main decisions? Who owns what action?",
                key="chat_q")
        with qi2:
            send = st.button("Send ➤", use_container_width=True, key="send")

        if send and user_q.strip():
            with st.spinner(""):
                ans = ask_question(r["rag_chain"], user_q.strip())
            st.session_state.chat_history += [
                {"role": "user",      "content": user_q.strip()},
                {"role": "assistant", "content": ans},
            ]
            st.rerun()

        # Quick prompts
        st.markdown('<p style="font-size:0.65rem;color:var(--muted);letter-spacing:0.14em;text-transform:uppercase;margin:0.8rem 0 0.3rem">Quick asks →</p>', unsafe_allow_html=True)
        qp1, qp2, qp3, qp4 = st.columns(4)
        QUICK = [
            ("Top 3 takeaways?",      qp1),
            ("Who owns what?",        qp2),
            ("What problems came up?", qp3),
            ("Any deadlines set?",    qp4),
        ]
        for qlabel, qcol in QUICK:
            with qcol:
                if st.button(qlabel, use_container_width=True, key=f"qp_{qlabel[:6]}"):
                    with st.spinner(""):
                        ans = ask_question(r["rag_chain"], qlabel)
                    st.session_state.chat_history += [
                        {"role": "user",      "content": qlabel},
                        {"role": "assistant", "content": ans},
                    ]
                    st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑 Clear chat", key="clr"):
                st.session_state.chat_history = []
                st.rerun()