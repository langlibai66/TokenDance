CARD_HTML_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg-start: {bg_start};
      --bg-end: {bg_end};
      --ink: {ink};
      --muted: {muted};
      --accent: {accent};
      --accent-soft: {accent_soft};
      --surface: {surface};
      --surface-strong: {surface_strong};
      --border: {border};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background:
        radial-gradient(circle at top left, rgba(255,255,255,0.65), transparent 36%),
        linear-gradient(160deg, var(--bg-start), var(--bg-end));
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      padding: 24px;
    }}
    .card {{
      width: min(100vw - 32px, 420px);
      aspect-ratio: 9 / 16;
      border-radius: 24px;
      overflow: hidden;
      display: grid;
      grid-template-rows: auto auto 1fr auto auto;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.86), rgba(255,255,255,0.94)),
        linear-gradient(135deg, rgba(255,255,255,0.2), transparent);
      border: 1px solid var(--border);
      box-shadow: 0 28px 72px rgba(20, 28, 45, 0.16);
      position: relative;
    }}
    .glow {{
      position: absolute;
      inset: 0;
      background:
        radial-gradient(circle at 86% 14%, rgba(255,255,255,0.7), transparent 18%),
        radial-gradient(circle at 18% 18%, rgba(255,255,255,0.28), transparent 26%);
      pointer-events: none;
    }}
    .header {{
      padding: 22px 22px 10px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      position: relative;
      z-index: 1;
    }}
    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      color: var(--accent);
      background: var(--accent_soft);
    }}
    .meta {{
      font-size: 12px;
      color: var(--muted);
      text-align: right;
      padding-top: 4px;
    }}
    .hero {{
      padding: 6px 22px 0;
      position: relative;
      z-index: 1;
    }}
    .headline {{
      margin: 0;
      font-size: 34px;
      line-height: 1.03;
      letter-spacing: 0;
      font-weight: 800;
    }}
    .subheadline {{
      margin: 12px 0 0;
      font-size: 15px;
      line-height: 1.5;
      color: var(--muted);
    }}
    .why-now {{
      margin-top: 14px;
      padding: 14px 16px;
      border-radius: 18px;
      background: var(--surface);
      border: 1px solid var(--border);
      font-size: 13px;
      line-height: 1.5;
    }}
    .sections {{
      padding: 18px 22px 0;
      display: grid;
      gap: 12px;
      align-content: start;
      position: relative;
      z-index: 1;
    }}
    .section {{
      padding: 14px 16px;
      border-radius: 18px;
      background: var(--surface);
      border: 1px solid var(--border);
    }}
    .section-title {{
      margin: 0 0 10px;
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--accent);
    }}
    .section ul {{
      margin: 0;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 8px;
    }}
    .section li {{
      font-size: 14px;
      line-height: 1.45;
      display: flex;
      gap: 8px;
      color: var(--ink);
    }}
    .section li::before {{
      content: "";
      width: 6px;
      height: 6px;
      border-radius: 999px;
      margin-top: 7px;
      flex: 0 0 auto;
      background: var(--accent);
    }}
    .actions {{
      padding: 16px 22px 0;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      position: relative;
      z-index: 1;
    }}
    .action {{
      padding: 10px 14px;
      border-radius: 999px;
      border: 1px solid rgba(18, 31, 44, 0.08);
      background: var(--surface-strong);
      font-size: 13px;
      font-weight: 700;
      color: var(--ink);
    }}
    .sources {{
      padding: 16px 22px 22px;
      display: grid;
      gap: 8px;
      align-content: end;
      position: relative;
      z-index: 1;
    }}
    .sources-title {{
      font-size: 11px;
      font-weight: 800;
      color: var(--muted);
      text-transform: uppercase;
    }}
    .source-list {{
      display: grid;
      gap: 8px;
    }}
    .source-item {{
      display: grid;
      gap: 2px;
      padding: 10px 12px;
      border-radius: 14px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.78);
    }}
    .source-item a {{
      color: var(--ink);
      text-decoration: none;
      font-size: 12px;
      font-weight: 700;
      line-height: 1.4;
    }}
    .source-item span {{
      font-size: 11px;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <article class="card">
    <div class="glow"></div>
    <header class="header">
      <div class="eyebrow">{topic}</div>
      <div class="meta">{aspect_ratio}<br>{theme_label}</div>
    </header>
    <section class="hero">
      <h1 class="headline">{headline}</h1>
      <p class="subheadline">{subheadline}</p>
      <div class="why-now">{why_now}</div>
    </section>
    <section class="sections">
      {sections_html}
    </section>
    <section class="actions">
      {actions_html}
    </section>
    <footer class="sources">
      <div class="sources-title">Sources</div>
      <div class="source-list">
        {sources_html}
      </div>
    </footer>
  </article>
</body>
</html>
"""
