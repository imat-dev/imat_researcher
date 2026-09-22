EXAMPLES = [
    "Most popular AI Agent frameworks in 2026",
    "Most commercially successful Agentic AI implementations in 2026",
    "Celebrities who don't like cheese",
]

HEADER_HTML = """
<div class="dr-hero">
    <p class="dr-eyebrow">Imat Deep Research</p>
    <h1 class="dr-headline">
        Ask anything.<br><span class="dr-gradient">Get the whole story.</span>
    </h1>
    <p class="dr-subhead">
        Four agents plan the searches, run them in parallel, and write it all up for you.
    </p>
</div>
"""

CSS = """
/* ============================================================
   Palette — Apple's system tokens
   ============================================================ */
.gradio-container {
    --dr-bg: #ffffff;
    --dr-surface: #f5f5f7;
    --dr-card: #ffffff;
    --dr-text: #1d1d1f;
    --dr-muted: #6e6e73;
    --dr-line: #d2d2d7;
    --dr-blue: #0071e3;
    --dr-blue-hover: #0077ed;
    --dr-link: #0066cc;
    --dr-radius: 18px;
    --dr-pill: 980px;

    max-width: 980px !important;
    margin: 0 auto !important;
    padding: 4rem 1.5rem 6rem !important;
    background: var(--dr-bg) !important;
    color: var(--dr-text) !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text",
                 "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    font-size: 17px !important;
    line-height: 1.47059 !important;
    letter-spacing: -0.022em !important;
    -webkit-font-smoothing: antialiased;
}

.gradio-container.dark,
.dark .gradio-container,
body.dark .gradio-container,
html.dark .gradio-container {
    --dr-bg: #000000;
    --dr-surface: #1d1d1f;
    --dr-card: #1d1d1f;
    --dr-text: #f5f5f7;
    --dr-muted: #86868b;
    --dr-line: #424245;
    --dr-blue: #0071e3;
    --dr-blue-hover: #0077ed;
    --dr-link: #2997ff;
}

body { background: var(--dr-bg, #ffffff); }

/* ============================================================
   Hero
   ============================================================ */
.dr-hero {
    text-align: center;
    margin: 0 auto 3.5rem;
    max-width: 720px;
    animation: dr-rise 0.7s cubic-bezier(0.28, 0.11, 0.32, 1) both;
}

@keyframes dr-rise {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}

.dr-eyebrow {
    font-size: 19px;
    line-height: 1.19;
    font-weight: 600;
    letter-spacing: 0.012em;
    color: var(--dr-blue);
    margin: 0 0 0.6rem;
}

.dr-headline {
    font-size: clamp(40px, 6.4vw, 64px);
    line-height: 1.0625;
    font-weight: 600;
    letter-spacing: -0.015em;
    color: var(--dr-text);
    margin: 0;
}

.dr-gradient {
    background: linear-gradient(92deg, #0071e3 0%, #6e5ef5 55%, #bf5af2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
}

.dr-subhead {
    font-size: 21px;
    line-height: 1.381;
    font-weight: 400;
    letter-spacing: 0.011em;
    color: var(--dr-muted);
    margin: 1.2rem auto 0;
    max-width: 34em;
}

/* ============================================================
   Query row
   ============================================================ */
.dr-query-row {
    gap: 12px !important;
    align-items: center !important;
    animation: dr-rise 0.7s cubic-bezier(0.28, 0.11, 0.32, 1) 0.08s both;
}

#dr-query, #dr-query > div, #dr-query .wrap, #dr-query .form, #dr-query .block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
}

#dr-query textarea, #dr-query input {
    background: var(--dr-surface) !important;
    color: var(--dr-text) !important;
    border: 1px solid transparent !important;
    border-radius: var(--dr-pill) !important;
    padding: 0.95rem 1.5rem !important;
    font-size: 17px !important;
    font-family: inherit !important;
    letter-spacing: -0.022em !important;
    box-shadow: none !important;
    line-height: 1.4 !important;
    resize: none !important;
    min-height: 56px !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease !important;
}

#dr-query textarea:focus, #dr-query input:focus {
    outline: none !important;
    background: var(--dr-card) !important;
    border-color: var(--dr-blue) !important;
    box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.18) !important;
}

#dr-query textarea::placeholder, #dr-query input::placeholder {
    color: var(--dr-muted) !important;
    opacity: 1 !important;
}

#dr-run {
    background: var(--dr-blue) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: var(--dr-pill) !important;
    font-weight: 400 !important;
    font-size: 17px !important;
    letter-spacing: -0.022em !important;
    text-transform: none !important;
    box-shadow: none !important;
    min-width: 132px !important;
    min-height: 56px !important;
    padding: 0.95rem 1.6rem !important;
    transition: background 0.25s ease, transform 0.15s ease, opacity 0.25s ease !important;
}

#dr-run:hover { background: var(--dr-blue-hover) !important; }
#dr-run:active { transform: scale(0.975) !important; }
#dr-run:focus-visible {
    outline: none !important;
    box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.35) !important;
}

/* ============================================================
   Clarification panel
   ============================================================ */
#dr-status {
    text-align: center !important;
    color: var(--dr-muted) !important;
    font-size: 15px !important;
    background: transparent !important;
    border: none !important;
    margin-top: 1rem !important;
    min-height: 0 !important;
}

#dr-status:empty { display: none !important; }

#dr-clarify {
    background: var(--dr-surface) !important;
    border: none !important;
    border-radius: var(--dr-radius) !important;
    padding: 1.75rem !important;
    margin-top: 1.5rem !important;
    box-shadow: none !important;
    animation: dr-rise 0.5s cubic-bezier(0.28, 0.11, 0.32, 1) both;
}

.dr-clarify-label {
    font-size: 21px;
    font-weight: 600;
    letter-spacing: -0.011em;
    color: var(--dr-text);
    margin-bottom: 1.25rem;
}

.dr-clarify-label span {
    display: block;
    font-size: 14px;
    font-weight: 400;
    letter-spacing: -0.016em;
    color: var(--dr-muted);
    margin-top: 0.2rem;
}

#dr-clarify .dr-question,
#dr-clarify .dr-question > div,
#dr-clarify .dr-question .block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

#dr-clarify .dr-question { margin-bottom: 1.1rem !important; }

#dr-clarify .dr-question label,
#dr-clarify .dr-question span[data-testid="block-info"] {
    font-size: 15px !important;
    font-weight: 500 !important;
    letter-spacing: -0.016em !important;
    color: var(--dr-text) !important;
}

#dr-clarify .dr-question span[data-testid="block-info"] {
    font-weight: 400 !important;
    color: var(--dr-muted) !important;
    font-size: 13px !important;
}

#dr-clarify .dr-question textarea,
#dr-clarify .dr-question input {
    background: var(--dr-card) !important;
    color: var(--dr-text) !important;
    border: 1px solid var(--dr-line) !important;
    border-radius: 12px !important;
    padding: 0.7rem 1rem !important;
    font-size: 17px !important;
    font-family: inherit !important;
    letter-spacing: -0.022em !important;
    box-shadow: none !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}

#dr-clarify .dr-question textarea:focus,
#dr-clarify .dr-question input:focus {
    outline: none !important;
    border-color: var(--dr-blue) !important;
    box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.18) !important;
}

#dr-go {
    background: var(--dr-blue) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: var(--dr-pill) !important;
    font-weight: 400 !important;
    font-size: 17px !important;
    letter-spacing: -0.022em !important;
    min-height: 48px !important;
    padding: 0.7rem 1.6rem !important;
    margin-top: 0.5rem !important;
    box-shadow: none !important;
    transition: background 0.25s ease, transform 0.15s ease !important;
}

#dr-go:hover { background: var(--dr-blue-hover) !important; }
#dr-go:active { transform: scale(0.985) !important; }

/* ============================================================
   Examples
   ============================================================ */
.dr-examples-label {
    font-size: 14px;
    letter-spacing: -0.016em;
    color: var(--dr-muted);
    text-transform: none;
    margin: 2.5rem 0 0.9rem 0;
    text-align: center;
}

#dr-examples, #dr-examples > div, #dr-examples .wrap, #dr-examples .block {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}

#dr-examples label, #dr-examples .label-wrap, #dr-examples > div > .label-wrap {
    display: none !important;
}

#dr-examples table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    width: 100% !important;
    background: transparent !important;
    border: none !important;
}

#dr-examples thead { display: none !important; }
#dr-examples tbody { background: transparent !important; }

#dr-examples tr {
    background: transparent !important;
    display: flex !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    gap: 10px !important;
    border: none !important;
}

#dr-examples td, #dr-examples button {
    background: var(--dr-surface) !important;
    border: 1px solid transparent !important;
    padding: 0.55rem 1.1rem !important;
    cursor: pointer !important;
    transition: background 0.25s ease, color 0.25s ease, transform 0.15s ease !important;
    font-size: 14px !important;
    letter-spacing: -0.016em !important;
    color: var(--dr-text) !important;
    border-radius: var(--dr-pill) !important;
    margin: 0 !important;
    text-align: center !important;
    box-shadow: none !important;
}

#dr-examples td:hover, #dr-examples button:hover {
    color: var(--dr-blue) !important;
    border-color: var(--dr-line) !important;
    transform: translateY(-1px);
}

/* ============================================================
   Report
   ============================================================ */
#dr-report {
    margin-top: 3rem !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--dr-text) !important;
    min-height: 40px;
}

#dr-report > div, #dr-report .prose {
    background: transparent !important;
    color: var(--dr-text) !important;
}

#dr-report:not(:empty) {
    border-top: 1px solid var(--dr-line) !important;
    padding-top: 2.5rem !important;
}

#dr-report h1 {
    font-size: 40px;
    font-weight: 600;
    line-height: 1.1;
    letter-spacing: -0.015em;
    color: var(--dr-text);
    border: none;
    padding: 0;
    margin: 2rem 0 1rem;
}

#dr-report h2 {
    font-size: 28px;
    font-weight: 600;
    line-height: 1.14;
    letter-spacing: -0.012em;
    color: var(--dr-text);
    margin-top: 2.5rem;
}

#dr-report h3 {
    font-size: 21px;
    font-weight: 600;
    line-height: 1.19;
    letter-spacing: -0.011em;
    color: var(--dr-text);
    margin-top: 2rem;
}

#dr-report p {
    font-size: 17px;
    line-height: 1.6;
    letter-spacing: -0.022em;
    color: var(--dr-text);
}

#dr-report a {
    color: var(--dr-link);
    text-decoration: none;
    transition: text-decoration 0.2s ease;
}

#dr-report a:hover { text-decoration: underline; }

#dr-report code {
    background: var(--dr-surface);
    border: none;
    padding: 0.15rem 0.45rem;
    border-radius: 6px;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
    font-size: 0.9em;
}

#dr-report pre {
    background: var(--dr-surface);
    border: none;
    border-radius: var(--dr-radius);
    padding: 1.25rem 1.5rem;
}

#dr-report blockquote {
    border-left: none !important;
    background: var(--dr-surface);
    border-radius: var(--dr-radius);
    padding: 1.25rem 1.5rem;
    margin: 1.5rem 0;
    color: var(--dr-text);
}

#dr-report ul, #dr-report ol { padding-left: 1.3rem; }
#dr-report li { margin: 0.4rem 0; line-height: 1.6; }

#dr-report table {
    border-collapse: separate;
    border-spacing: 0;
    border: 1px solid var(--dr-line);
    border-radius: 12px;
    overflow: hidden;
    width: 100%;
}

#dr-report th, #dr-report td {
    border: none;
    border-bottom: 1px solid var(--dr-line);
    padding: 0.7rem 1rem;
    text-align: left;
    font-size: 15px;
}

#dr-report tr:last-child td { border-bottom: none; }

#dr-report th {
    background: var(--dr-surface);
    font-weight: 600;
    color: var(--dr-text);
}

footer { display: none !important; }

@media (prefers-reduced-motion: reduce) {
    .dr-hero, .dr-query-row { animation: none !important; }
    * { transition-duration: 0.01ms !important; }
}

@media (max-width: 734px) {
    .gradio-container { padding: 2.5rem 1.25rem 4rem !important; }
    .dr-query-row { flex-direction: column !important; }
    #dr-run { width: 100% !important; }
    .dr-subhead { font-size: 19px; }
}
"""

JS = """
() => {
    const focus = () => {
        const el = document.querySelector("#dr-query textarea, #dr-query input");
        if (el) { el.focus(); return true; }
        return false;
    };
    if (!focus()) {
        let tries = 0;
        const i = setInterval(() => {
            if (focus() || ++tries > 20) clearInterval(i);
        }, 100);
    }
}
"""
