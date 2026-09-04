from datetime import datetime
from html import escape

import streamlit as st

from translator import LANGUAGES, translate_text


MAX_HISTORY_ITEMS = 8

st.set_page_config(
    page_title="Pinnacle Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --bg: #f6f8f7;
            --card: #ffffff;
            --border: #e6e9ec;
            --text: #1f2933;
            --muted: #6b7280;
            --green: #16a34a;
            --green-dark: #15803d;
            --green-soft: #f0fdf4;
            --green-line: #bbf7d0;
        }
        html, body, [data-testid="stAppViewContainer"] {
            background: var(--bg);
            color: var(--text);
            font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
        }
        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--border);
        }
        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }
        [data-testid="stTextArea"] textarea {
            font-size: 1.02rem;
            line-height: 1.6;
            border-radius: 10px;
        }
        [data-testid="stButton"] button {
            border-radius: 10px;
            font-weight: 600;
        }
        [data-testid="stButton"] button[kind="primary"] {
            background: var(--green);
            border-color: var(--green);
        }
        [data-testid="stButton"] button[kind="primary"]:hover {
            background: var(--green-dark);
            border-color: var(--green-dark);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            padding: 0.2rem 0 1rem;
        }
        .brand-mark {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: var(--green);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            box-shadow: 0 2px 6px rgba(22,163,74,.25);
        }
        .brand-name {
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--muted);
        }
        .brand-app {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text);
            line-height: 1.1;
        }

        .nav-label {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 0.35rem;
        }
        div[data-testid="stRadio"] > div {
            gap: 0.25rem;
        }
        div[data-testid="stRadio"] label {
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.5rem 0.7rem;
            background: #fbfcfc;
            font-weight: 600;
        }
        div[data-testid="stRadio"] label:hover {
            border-color: var(--green-line);
        }

        .status-card {
            margin-top: 1.2rem;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.85rem 1rem;
            background: var(--green-soft);
        }
        .status-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .status-key {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text);
        }
        .status-val {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--green-dark);
        }
        .dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 0 3px rgba(22,163,74,.18);
        }

        .page-head {
            margin-bottom: 1.2rem;
        }
        .page-title {
            font-size: 1.9rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--text);
            margin: 0;
        }
        .page-sub {
            font-size: 1rem;
            color: var(--muted);
            margin: 0.3rem 0 0;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.25rem 1.4rem;
            box-shadow: 0 1px 2px rgba(16,24,40,.04);
            margin-bottom: 1.1rem;
        }
        .card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text);
            margin: 0 0 0.9rem;
        }
        .field-label {
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 0.35rem;
        }
        .count {
            font-size: 0.8rem;
            color: var(--muted);
            margin-top: 0.4rem;
        }
        .swap-btn button {
            font-size: 1.2rem;
        }

        .result-label {
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 0.35rem;
        }
        .result-box {
            border: 1px solid var(--border);
            border-radius: 10px;
            font-size: 1.05rem;
            line-height: 1.6;
            min-height: 3.4rem;
            padding: 0.9rem 1rem;
            white-space: pre-wrap;
            background: #fbfcfc;
            color: var(--text);
        }
        .translated-box {
            border: 1px solid var(--green-line);
            border-radius: 10px;
            font-size: 1.1rem;
            line-height: 1.6;
            min-height: 3.4rem;
            padding: 0.9rem 1rem;
            white-space: pre-wrap;
            background: var(--green-soft);
            color: #14532d;
        }

        .pair-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.7rem;
        }
        .pair-card {
            border: 1px solid var(--border);
            border-radius: 12px;
            background: #fbfcfc;
            padding: 0.7rem 0.85rem;
            text-align: center;
            font-weight: 600;
            color: var(--text);
            font-size: 0.9rem;
        }
        .pair-card small {
            display: block;
            font-weight: 500;
            color: var(--muted);
            font-size: 0.76rem;
            margin-top: 0.15rem;
        }

        .tag {
            display: inline-block;
            background: #f1f5f3;
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.3rem 0.75rem;
            font-size: 0.82rem;
            color: var(--text);
            margin: 0.2rem 0.3rem 0.2rem 0;
            font-weight: 500;
        }

        .metric-num {
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--green-dark);
            line-height: 1;
        }

        .hist-item {
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.85rem 1rem;
            margin-bottom: 0.7rem;
            background: #fff;
        }
        .hist-head {
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.5rem;
        }
        .hist-head .time {
            color: var(--muted);
            font-weight: 600;
            float: right;
        }
        .hist-text {
            font-size: 0.92rem;
            color: var(--text);
            line-height: 1.5;
        }
        .hist-text .lbl {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 600;
        }
        .hist-text .tr {
            color: var(--green-dark);
        }

        .empty-state {
            text-align: center;
            padding: 1.6rem 1rem;
        }
        .empty-state .t {
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text);
        }
        .empty-state .s {
            font-size: 0.95rem;
            color: var(--muted);
            margin-top: 0.3rem;
        }

        @media (max-width: 820px) {
            .pair-grid { grid-template-columns: repeat(2, 1fr); }
            .page-title { font-size: 1.6rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_state() -> None:
    defaults = {
        "source_language": "English",
        "target_language": "Telugu",
        "source_text": "",
        "translation": None,
        "message": None,
        "history": [],
        "nav": "Translate",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def swap_languages() -> None:
    source = st.session_state.source_language
    st.session_state.source_language = st.session_state.target_language
    st.session_state.target_language = source
    st.session_state.translation = None
    st.session_state.message = None


def clear_translation() -> None:
    st.session_state.source_text = ""
    st.session_state.translation = None
    st.session_state.message = None


def run_translation() -> None:
    result = translate_text(
        st.session_state.source_text,
        st.session_state.source_language,
        st.session_state.target_language,
    )
    if not result["success"]:
        st.session_state.translation = None
        st.session_state.message = result["error"]
        return

    st.session_state.translation = result["translated_text"]
    st.session_state.message = None
    history_item = {
        "source": result["source_language"],
        "target": result["target_language"],
        "original": result["original_text"],
        "translated": result["translated_text"],
        "time": datetime.now().strftime("%I:%M %p"),
    }
    st.session_state.history.insert(0, history_item)
    del st.session_state.history[MAX_HISTORY_ITEMS:]


def clear_history() -> None:
    st.session_state.history = []


def set_pair(source: str, target: str) -> None:
    st.session_state.source_language = source
    st.session_state.target_language = target
    st.session_state.translation = None
    st.session_state.message = None


initialize_state()


with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">🌐</div>
            <div>
                <div class="brand-name">Pinnacle Labs</div>
                <div class="brand-app">Translator</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)
    st.session_state.nav = st.radio(
        "Navigation",
        ["Translate", "History", "Languages", "About"],
        index=["Translate", "History", "Languages", "About"].index(st.session_state.nav),
        label_visibility="collapsed",
        key="nav_radio",
    )

    st.markdown(
        """
        <div class="status-card">
            <div class="status-row">
                <span class="status-key">Translation service</span>
                <span class="status-val"><span class="dot"></span>Ready</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_history_section() -> None:
    top, action = st.columns([4, 1], vertical_alignment="center")
    with top:
        st.markdown('<div class="card-title">Recent translations</div>', unsafe_allow_html=True)
    with action:
        if st.session_state.history:
            st.button("Clear history", on_click=clear_history, use_container_width=True)

    if not st.session_state.history:
        st.markdown(
            '<div class="empty-state"><div class="t">No translations yet</div>'
            '<div class="s">Your recent translations will appear here.</div></div>',
            unsafe_allow_html=True,
        )
        return

    for item in st.session_state.history:
        original = escape(item["original"])
        translated = escape(item["translated"])
        st.markdown(
            f"""
            <div class="hist-item">
                <div class="hist-head">{escape(item['source'])} → {escape(item['target'])}
                    <span class="time">{escape(item['time'])}</span>
                </div>
                <div class="hist-text"><span class="lbl">Original</span><br>{original}</div>
                <div class="hist-text" style="margin-top:.4rem;">
                    <span class="lbl">Translated</span><br><span class="tr">{translated}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_language_summary() -> None:
    st.markdown('<div class="card-title">Supported languages</div>', unsafe_allow_html=True)
    top, tags = st.columns([1, 3], vertical_alignment="center")
    with top:
        st.markdown(f'<div class="metric-num">{len(LANGUAGES)}</div>', unsafe_allow_html=True)
    with tags:
        tag_html = "".join(f'<span class="tag">{escape(lang)}</span>' for lang in LANGUAGES)
        st.markdown(tag_html, unsafe_allow_html=True)


POPULAR_PAIRS = [
    ("English", "Telugu"),
    ("English", "Hindi"),
    ("English", "Spanish"),
    ("English", "French"),
]

if st.session_state.nav == "Translate":
    st.markdown(
        """
        <div class="page-head">
            <h1 class="page-title">Translator</h1>
            <p class="page-sub">Translate messages naturally across multiple languages.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        src_col, swap_col, tgt_col = st.columns([5, 1, 5], vertical_alignment="bottom")
        with src_col:
            st.markdown('<div class="field-label">Source language</div>', unsafe_allow_html=True)
            st.selectbox("Source", LANGUAGES, key="source_language", label_visibility="collapsed")
        with swap_col:
            st.markdown('<div class="swap-btn">', unsafe_allow_html=True)
            st.button("⇄", help="Swap languages", on_click=swap_languages, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with tgt_col:
            st.markdown('<div class="field-label">Target language</div>', unsafe_allow_html=True)
            st.selectbox("Target", LANGUAGES, key="target_language", label_visibility="collapsed")

        st.markdown('<div class="field-label">Your text</div>', unsafe_allow_html=True)
        st.text_area(
            "Your text",
            key="source_text",
            height=170,
            max_chars=5000,
            label_visibility="collapsed",
            placeholder="Type or paste the message you want to translate...",
        )
        count = len(st.session_state.source_text or "")
        st.markdown(
            f'<div class="count">{count:,} / 5,000 characters</div>',
            unsafe_allow_html=True,
        )

        tr_col, cl_col = st.columns([3, 1])
        with tr_col:
            st.button("Translate", type="primary", on_click=run_translation, use_container_width=True)
        with cl_col:
            st.button("Clear", on_click=clear_translation, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.message:
        st.error(st.session_state.message)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Translation</div>', unsafe_allow_html=True)
        if st.session_state.translation:
            st.markdown('<div class="result-label">Original</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="result-box">{escape(st.session_state.source_text)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="result-label" style="margin-top:.8rem;">Translated</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="translated-box">{escape(st.session_state.translation)}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="empty-state">
                    <div class="t">Ready to translate</div>
                    <div class="s">Enter your text, choose two languages, and translate.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Popular pairs</div>', unsafe_allow_html=True)
        st.markdown('<div class="pair-grid">', unsafe_allow_html=True)
        for src, tgt in POPULAR_PAIRS:
            st.markdown(
                f'<div class="pair-card">{src} → {tgt}<small>Set languages</small></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
        pair_cols = st.columns(4)
        for i, (src, tgt) in enumerate(POPULAR_PAIRS):
            with pair_cols[i]:
                st.button(
                    f"{src} → {tgt}",
                    key=f"pair_{i}",
                    on_click=set_pair,
                    args=(src, tgt),
                    use_container_width=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_history_section()
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_language_summary()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.nav == "History":
    st.markdown(
        """
        <div class="page-head">
            <h1 class="page-title">History</h1>
            <p class="page-sub">Review the translations from your current session.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_history_section()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.nav == "Languages":
    st.markdown(
        """
        <div class="page-head">
            <h1 class="page-title">Languages</h1>
            <p class="page-sub">Seven widely used languages are available for translation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_language_summary()
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Popular pairs</div>', unsafe_allow_html=True)
        pair_cols = st.columns(4)
        for i, (src, tgt) in enumerate(POPULAR_PAIRS):
            with pair_cols[i]:
                st.button(
                    f"{src} → {tgt}",
                    key=f"pair_lang_{i}",
                    on_click=set_pair,
                    args=(src, tgt),
                    use_container_width=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(
        """
        <div class="page-head">
            <h1 class="page-title">About</h1>
            <p class="page-sub">A simple, reliable translator built by Pinnacle Labs.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            """
            <p style="line-height:1.7;color:#1f2933;">
            The Pinnacle Translator helps you translate everyday messages between seven
            widely used languages. It runs entirely in your browser session, keeps a short
            history of recent translations, and needs no API key to get started.
            </p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_language_summary()
        st.markdown("</div>", unsafe_allow_html=True)
