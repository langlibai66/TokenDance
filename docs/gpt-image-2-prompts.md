# GPT-Image-2 Prompt Pack

本文件整理了 `MomentCard` 项目用于生成技术方案图、架构图和案例运行图的 `GPT-Image-2` prompt。

默认约束：

- 画幅：`16:9`
- 风格：企业架构蓝白风，白底，蓝灰主色，少量青蓝强调
- 形态：扁平化矢量信息图，适合 PPT 和答辩展示
- 文字：中高密度中文标签，不要大段小字
- 目标：结构清晰、箭头明确、模块分层强、后期可在 Figma / PPT 中继续补字

## 使用建议

- 先用 prompt 生成结构图，再人工替换或加粗关键中文标签。
- 如果中文小字发糊，优先减少标签数量，不要先改深色风格。
- 同一套图保持统一视觉语言，避免有的像产品海报、有的像论文图。
- 答辩优先展示第 2 张和第 4 张，方法论和运行闭环最容易说服评委。

## 1. 核心方法论图

```text
Create a clean flat vector architecture infographic, 16:9, white background, enterprise blue-white style, dark gray text, blue and cyan accents, presentation-slide quality, high readability, not sketchy, not 3D, not realistic.

Main title in Chinese: “用户画像 × 当前事件 × 即时意图”
Subtitle in Chinese: “在交叉点上生成用户此刻最需要的信息流卡片”

Layout:
On the left, show three strong signal sources as three large labeled blocks:
1. “搜索行为：高意图锚点”
   small labels: “主动搜索”, “明确问题”, “高置信度”
2. “刷视频行为：偏好佐证”
   small labels: “停留”, “收藏”, “跳出”, “偏好补全”
3. “实时事件：需求触发器”
   small labels: “天气”, “节气”, “时间”, “地点”, “热点”

All three arrows converge into a large center block:
“决策交叉点”
inside small labels:
“用户画像”
“当前事件”
“即时意图”

From the center, output to the right into a highlighted block:
“AI 信息流卡片”
small labels:
“刷到即成立”
“直接给结果”
“轻量互动”

At the bottom, add a comparison strip:
left small box: “传统推荐：猜你喜欢”
right small box: “MomentCard：此刻需要”

Use large Chinese labels, minimal small text, 8-12 readable Chinese labels total, clean spacing, clear arrows, strong hierarchy.
```

## 2. 端到端技术链路图

```text
Create a polished system architecture diagram for an AI-native short-video feed card pipeline, 16:9, white background, blue-gray enterprise style, flat vector, high information density, readable Chinese labels, no clutter, no decorative icons.

Main title in Chinese: “MomentCard 端到端技术链路”

Show a left-to-right pipeline with 6 large layers:
1. “原始搜索与交互数据”
   small labels: “搜索词”, “搜索结果点击”, “停留/跳出”, “收藏反馈”
2. “LLM 意图抽取”
   small labels: “意图识别”, “偏好提炼”, “规避项抽取”
3. “Profile Skill Store”
   small labels: “长期画像”, “可触发 Skill”, “证据引用”
4. “实时事件引擎”
   small labels: “天气”, “节气”, “时间”, “地点”, “平台热点”
5. “AI 卡片生成引擎”
   small labels: “事件匹配”, “LLM 推理”, “卡片组装”
6. “抖音信息流卡片”
   small labels: “推荐流展示”, “轻交互”, “反馈写回”

Add two small system labels:
above layer 1-5: “flow_agent”
above layer 6: “douyin-base”

Add a feedback arrow from the final card back to the first layer, labeled:
“点击 / 跳过 / 收藏 / 换一个”

Use bold Chinese titles, simple arrows, editable text areas, keep text legible and avoid tiny paragraphs.
```

## 3. Profile Skill Store 结构图

```text
Create a clean data-model infographic, 16:9, flat vector, white background, enterprise architecture style, blue-white palette, strong hierarchy, readable Chinese labels.

Main title in Chinese: “Profile Skill Store 结构图”

Center a large modular block:
“Profile Skill Store”

Inside show one highlighted example card:
“Skill 对象”
with readable field labels:
“skill_id”
“intent_type”
“activation_events”
“keywords”
“negative_keywords”
“confidence”
“evidence_refs”
“preferred_card_style”
“interaction_preferences”

On the left show three evidence source groups:
1. “搜索证据”
   labels: “query”, “高意图问题”
2. “搜索结果探索证据”
   labels: “点击顺序”, “停留时长”, “收藏/跳出”
3. “自然刷视频证据”
   labels: “偏好佐证”, “长期兴趣”

On the right show downstream usage groups:
1. “事件匹配”
2. “LLM 推理”
3. “AI 卡片生成”

At the bottom add one Chinese note strip:
“画像不是静态标签，而是可被事件触发调用的技能单元”

Use box-and-arrow architecture style, medium-high information density, keep all labels short and readable.
```

## 4. 单次卡片生成运行图

```text
Create a scenario-based runtime flow infographic for a personalized AI card in a TikTok-style feed, 16:9, white background, enterprise blue-white style, flat vector, presentation-ready, readable Chinese text.

Main title in Chinese: “单次卡片生成运行图”
Subtitle in Chinese: “案例：低年级技术奖学生的换机决策卡”

Show a left-to-right runtime sequence with 5 steps:
1. “平台热点升温”
   labels: “iPhone17 系列”, “安卓旗舰横评”, “发布窗口”
2. “用户高意图搜索”
   labels: “iPhone17 系列怎么选”, “Air / Pro / Pro Max”, “跨品牌对比”
3. “命中 Profile Skill”
   labels: “数码发烧友”, “近期换机需求”, “苹果生态偏好”
4. “事件 + 画像 + 即时意图融合”
   labels: “型号纠结”, “价格敏感”, “长期主力机”
5. “生成 AI 信息流卡片”

On the far right, include a mobile feed mockup with one highlighted card.
Card title in Chinese:
“你更适合 iPhone17 Pro”
Card body labels:
“比 Air 更稳”
“比 Pro Max 更轻”
“开发 + 日常更均衡”
Buttons:
“看安卓备选”
“换成续航优先”

Add one feedback arrow back from the card:
“用户点击后继续修正画像”

Keep the mobile card visually prominent, use large Chinese text, avoid tiny captions.
```

## 5. 数据结构与字段关系图

```text
Create a technical schema relationship diagram, 16:9, flat vector, white background, blue-gray enterprise style, clean and dense, suitable for technical documentation, readable Chinese labels.

Main title in Chinese: “数据结构与字段关系图”

Show three major data layers stacked or left-to-right:

Layer 1:
“原始行为日志”
file label: “event_search_log.json”
fields:
“session_id”
“trigger_event”
“search_chain”
“result_impressions”
“interaction_summary”
“derived_evidence”

Layer 2:
“画像 Skill 文档”
file label: “profile_skill.md”
fields:
“长期兴趣”
“核心目标”
“核心焦虑”
“Skills”
“evidence_refs”
“preferred_card_style”

Layer 3:
“卡片输出层”
fields:
“卡片标题”
“推荐理由”
“轻交互按钮”
“反馈写回”

Add relationship arrows:
“session_id -> evidence_refs”
“搜索证据 -> Skill”
“Skill + Event -> Card”
“Card feedback -> 行为日志”

Add one side note block:
“前端展示不承载复杂分析逻辑，只消费结构化结果”

Use short Chinese field labels, strong alignment, architecture-diagram style, no unnecessary decoration.
```
