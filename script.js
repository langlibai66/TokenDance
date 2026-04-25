const scenes = [
  {
    kicker: "18:30 晚饭时段",
    title: "今晚适合来一份热汤面",
    summary: "下雨、降温、刚下班，AI 推荐一张更适合此刻的轻决策卡片。",
    tag: "吃什么",
    highlight: "推荐方案：番茄肥牛汤面 + 溏心蛋",
    reason: "热量适中、饱腹感强，适合忙碌后的快速恢复，也更适合阴雨天气的胃口。",
    time: "22 分钟",
    budget: "25-35 元",
    style: "暖胃优先",
    actions: ["想要同款", "更省钱", "不想吃面"]
  },
  {
    kicker: "周六 10:00 周末状态",
    title: "今天适合一场轻出逃",
    summary: "天气晴、路程短、拍照友好，AI 生成一个半日微出行方案。",
    tag: "去哪儿",
    highlight: "推荐路线：滨江步道 + 咖啡店 + 日落观景点",
    reason: "动线轻松、节奏舒服，不需要复杂准备，适合临时出门和朋友小聚。",
    time: "4 小时",
    budget: "60-120 元",
    style: "轻松出片",
    actions: ["换成省钱版", "我想拍照", "适合约会吗"]
  },
  {
    kicker: "赛前 30 分钟",
    title: "你关注的比赛快开始了",
    summary: "AI 把阵容、看点和悬念压缩成一张赛前卡，适合在信息流中快速消费。",
    tag: "看比赛",
    highlight: "核心看点：双核对位，节奏与三分命中率决定走势",
    reason: "不用打开资讯 App，就能在一眼之内知道这场比赛为什么值得看。",
    time: "30 秒读完",
    budget: "信息即得",
    style: "赛前速览",
    actions: ["展开阵容", "看关键球员", "提醒我开赛"]
  }
];

const elements = {
  kicker: document.getElementById("story-kicker"),
  title: document.getElementById("story-title"),
  summary: document.getElementById("story-summary"),
  tag: document.getElementById("card-tag"),
  highlight: document.getElementById("highlight-line"),
  reason: document.getElementById("card-reason"),
  time: document.getElementById("meta-time"),
  budget: document.getElementById("meta-budget"),
  style: document.getElementById("meta-style"),
  actions: document.getElementById("card-actions"),
  progress: document.getElementById("progress-fill"),
  shuffle: document.getElementById("shuffle-btn"),
  dots: Array.from(document.querySelectorAll(".scene-dot"))
};

let currentIndex = 0;

function renderScene(index) {
  const scene = scenes[index];
  if (!scene) {
    return;
  }

  elements.kicker.textContent = scene.kicker;
  elements.title.textContent = scene.title;
  elements.summary.textContent = scene.summary;
  elements.tag.textContent = scene.tag;
  elements.highlight.textContent = scene.highlight;
  elements.reason.textContent = scene.reason;
  elements.time.textContent = scene.time;
  elements.budget.textContent = scene.budget;
  elements.style.textContent = scene.style;
  elements.progress.style.width = `${((index + 1) / scenes.length) * 100}%`;

  elements.actions.innerHTML = "";
  scene.actions.forEach((label) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    elements.actions.appendChild(button);
  });

  elements.dots.forEach((dot, dotIndex) => {
    dot.classList.toggle("is-active", dotIndex === index);
  });

  currentIndex = index;
}

function showNextScene() {
  const nextIndex = (currentIndex + 1) % scenes.length;
  renderScene(nextIndex);
}

elements.shuffle.addEventListener("click", showNextScene);

elements.dots.forEach((dot) => {
  dot.addEventListener("click", () => {
    const targetIndex = Number(dot.dataset.index);
    renderScene(targetIndex);
  });
});

renderScene(currentIndex);
