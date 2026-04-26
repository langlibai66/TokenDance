from __future__ import annotations

from html import escape

from src.models.card import CardSection, CardSource, CardSpec
from src.templates.card_template import CARD_HTML_TEMPLATE

THEMES = {
    "default": {
        "bg_start": "#f7f3ea",
        "bg_end": "#dce7f2",
        "ink": "#16202d",
        "muted": "#5d6b7b",
        "accent": "#0c8c78",
        "accent_soft": "rgba(12, 140, 120, 0.14)",
        "surface": "rgba(255, 255, 255, 0.74)",
        "surface_strong": "rgba(255, 255, 255, 0.92)",
        "border": "rgba(22, 32, 45, 0.08)",
        "theme_label": "Moment Card",
    },
    "tech": {
        "bg_start": "#eef6f8",
        "bg_end": "#dfe6f8",
        "ink": "#132032",
        "muted": "#5a6a80",
        "accent": "#007d84",
        "accent_soft": "rgba(0, 125, 132, 0.14)",
        "surface": "rgba(255, 255, 255, 0.76)",
        "surface_strong": "rgba(255, 255, 255, 0.94)",
        "border": "rgba(19, 32, 50, 0.08)",
        "theme_label": "Tech Brief",
    },
    "sports": {
        "bg_start": "#f4f8eb",
        "bg_end": "#e6efe1",
        "ink": "#18251f",
        "muted": "#5f6d66",
        "accent": "#3e8f3e",
        "accent_soft": "rgba(62, 143, 62, 0.14)",
        "surface": "rgba(255, 255, 255, 0.76)",
        "surface_strong": "rgba(255, 255, 255, 0.94)",
        "border": "rgba(24, 37, 31, 0.08)",
        "theme_label": "Match Snapshot",
    },
    "study": {
        "bg_start": "#fff2e8",
        "bg_end": "#f3ead8",
        "ink": "#2c2118",
        "muted": "#776454",
        "accent": "#bf6b2e",
        "accent_soft": "rgba(191, 107, 46, 0.16)",
        "surface": "rgba(255, 255, 255, 0.78)",
        "surface_strong": "rgba(255, 255, 255, 0.94)",
        "border": "rgba(44, 33, 24, 0.08)",
        "theme_label": "Study Brief",
    },
}


def render_card_html(spec: CardSpec) -> str:
    theme = THEMES.get(spec.theme, THEMES["default"])
    theme_vars = {key: value for key, value in theme.items() if key != "theme_label"}
    sections_html = "\n".join(_render_section(section) for section in spec.sections)
    actions_html = "\n".join(
        f'<div class="action">{escape(action)}</div>' for action in spec.quick_actions
    )
    sources_html = "\n".join(_render_source(source) for source in spec.sources[:4])

    return CARD_HTML_TEMPLATE.format(
        title=escape(spec.headline),
        topic=escape(spec.topic),
        headline=escape(spec.headline),
        subheadline=escape(spec.subheadline),
        why_now=escape(spec.why_now),
        sections_html=sections_html,
        actions_html=actions_html,
        sources_html=sources_html,
        aspect_ratio=escape(spec.aspect_ratio),
        theme_label=escape(theme["theme_label"]),
        **theme_vars,
    )


def _render_section(section: CardSection) -> str:
    items = "\n".join(f"<li>{escape(item)}</li>" for item in section.items[:4])
    return (
        '<section class="section">'
        f'<h2 class="section-title">{escape(section.title)}</h2>'
        f"<ul>{items}</ul>"
        "</section>"
    )


def _render_source(source: CardSource) -> str:
    return (
        '<div class="source-item">'
        f'<a href="{escape(source.url)}" target="_blank" rel="noreferrer">{escape(source.title)}</a>'
        f"<span>{escape(source.site)}</span>"
        "</div>"
    )
