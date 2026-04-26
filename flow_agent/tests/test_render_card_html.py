from src.models.card import CardSection, CardSource, CardSpec
from src.services.html_renderer import render_card_html


def test_render_card_html_contains_expected_blocks() -> None:
    spec = CardSpec(
        card_id="iphone17-upgrade",
        user_id="u-1",
        topic="iPhone17 换机",
        headline="iPhone17 这次该怎么选",
        subheadline="如果你在 Air、Pro 和 Pro Max 之间纠结，先看使用场景。",
        why_now="平台里的横评和新机内容都在升温，这时候最需要一个直接结论。",
        sections=[
            CardSection(
                kind="comparison",
                title="型号差异",
                items=["Air 更轻薄", "Pro 更均衡", "Pro Max 续航更强"],
            )
        ],
        quick_actions=["只看 Air", "加入安卓备选"],
        sources=[
            CardSource(
                title="iPhone17 系列对比",
                url="https://example.com/iphone17",
                site="example.com",
            )
        ],
        theme="tech",
        aspect_ratio="9:16",
    )

    html = render_card_html(spec)

    assert "aspect-ratio: 9 / 16" in html
    assert "iPhone17 这次该怎么选" in html
    assert "Sources" in html
    assert "Tech Brief" in html
