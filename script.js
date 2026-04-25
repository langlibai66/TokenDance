const scenes = [
  {
    tag: "AI生成",
    kicker: "春季徒步推荐",
    title: "莫干山清明越野跑攻略",
    destination: "湖州·莫干山",
    days: "2天",
    weather: "15-25°C",
    scenery: "植被丰茂",
    copy: "正值春末夏初，是跑山的好季节。去莫干山吧，感受经典赛道与山野风光。",
    day1: "Day 1",
    day2: "Day 2",
    caption: "春季山野路线与博主攻略卡片的组合展示。",
    detailTitle: "整屏切页让山野攻略更好展示",
    detailCopy: "先讲概念，再放大手机界面，最后补充设计价值。用户不会卡在半屏，也不会在说明和原型之间来回分神。",
    detailFit: "适合想做周末轻户外计划、又希望内容像短视频一样轻松易看的用户。",
    detailRhythm: "第一页收信息，第二页看完整原型，第三页收结论，浏览路径更自然。",
    detailHighlight: "用沉浸式背景和玻璃态卡片承接 AI 攻略内容，兼顾短视频感与信息密度。",
    creators: [
      {
        quote: "“去越野跑吧！钻林子当猴子其乐无穷！”",
        text: "笨蛋哒：去自然里坐坐好舒服呀，庾村好吃很多，有很多条越野跑路线",
        thumbClass: "thumb-a"
      },
      {
        quote: "“莫干山山顶喝咖啡超 nice！”",
        text: "淡人周末：雨天进山，一个人去莫干山顶喝咖啡真是太 nice 了",
        thumbClass: "thumb-b"
      }
    ]
  },
  {
    tag: "AI生成",
    kicker: "周末山野露营",
    title: "安吉竹海两天一夜轻露营",
    destination: "湖州·安吉",
    days: "2天1夜",
    weather: "18-26°C",
    scenery: "竹林云海",
    copy: "适合朋友结伴出发，白天徒步看竹海，傍晚在山顶看日落，晚上围炉聊天。",
    day1: "Camp",
    day2: "Hike",
    caption: "露营与徒步结合的周末路线，更偏氛围感和社交感。",
    detailTitle: "第二个场景偏向放松型周末内容",
    detailCopy: "这一组内容更适合展示短视频里的生活方式气质。路线信息简洁，重点放在氛围、日落、云海和结伴体验。",
    detailFit: "适合情侣、朋友组队、偏爱拍照和慢节奏户外体验的人群。",
    detailRhythm: "先种草氛围，再交代路线和天气，整体更像内容平台里的生活方式推荐。",
    detailHighlight: "画面感更强，适合后续加露营清单、日落时间和拍照机位等补充信息。",
    creators: [
      {
        quote: "“这条线新手也能冲，风景密度很高。”",
        text: "阿卷：中午到达直接进山，沿途机位很多，拍人像和自然景都很出片",
        thumbClass: "thumb-b"
      },
      {
        quote: "“清晨从帐篷拉开拉链就是云海。”",
        text: "木子：如果天气好，第二天早起会很值，整个体验非常松弛",
        thumbClass: "thumb-a"
      }
    ]
  },
  {
    tag: "AI生成",
    kicker: "城市近郊微度假",
    title: "雁荡山一日登高路线",
    destination: "温州·雁荡山",
    days: "1天",
    weather: "17-23°C",
    scenery: "山谷瀑布",
    copy: "适合想要周末短逃离的人群，一天内完成登山、看瀑布和山间咖啡小憩。",
    day1: "AM",
    day2: "PM",
    caption: "更轻决策的一日行程，强调近郊逃离和低门槛出发。",
    detailTitle: "第三个场景更适合快节奏决策",
    detailCopy: "一日路线天然适合短视频信息流。用户能很快理解目的地、时长和体验内容，适合做高转化入口。",
    detailFit: "适合临时起意的周末出行人群，尤其适合想要低成本短逃离的用户。",
    detailRhythm: "信息密度最高，但仍然控制在一屏内完成表达，保留浏览效率。",
    detailHighlight: "突出路线效率和低门槛，让手机屏里的攻略卡片更接近真实产品转化页。",
    creators: [
      {
        quote: "“走到山谷深处会突然安静下来，很治愈。”",
        text: "七七：建议轻装出发，穿防滑鞋，午后光线打在瀑布上特别好看",
        thumbClass: "thumb-a"
      },
      {
        quote: "“景点之间衔接顺，拍照和赶路都不会太累。”",
        text: "阿泽：很适合带家人或者和对象一起走，节奏舒服，不会太赶",
        thumbClass: "thumb-b"
      }
    ]
  }
];

const elements = {
  track: document.getElementById("panel-track"),
  panels: Array.from(document.querySelectorAll("[data-panel]")),
  pageDots: Array.from(document.querySelectorAll(".page-dot")),
  tag: document.getElementById("hero-tag"),
  kicker: document.getElementById("hero-kicker"),
  title: document.getElementById("hero-title"),
  destination: document.getElementById("meta-destination"),
  days: document.getElementById("meta-days"),
  weather: document.getElementById("meta-weather"),
  scenery: document.getElementById("meta-scenery"),
  copy: document.getElementById("card-copy"),
  day1: document.getElementById("route-day-1"),
  day2: document.getElementById("route-day-2"),
  creators: document.getElementById("creator-list"),
  shuffle: document.getElementById("shuffle-btn"),
  sceneCaption: document.getElementById("scene-caption"),
  detailTitle: document.getElementById("detail-title"),
  detailCopy: document.getElementById("detail-copy"),
  detailFit: document.getElementById("detail-fit"),
  detailRhythm: document.getElementById("detail-rhythm"),
  detailHighlight: document.getElementById("detail-highlight"),
  sceneDots: Array.from(document.querySelectorAll(".scene-dot")),
  progressPills: Array.from(document.querySelectorAll(".progress-pill"))
};

let currentSceneIndex = 0;
let currentPanelIndex = 0;
let isPanelAnimating = false;
let touchStartY = 0;
let panelUnlockTimer = null;

function renderCreators(creators) {
  elements.creators.innerHTML = "";

  creators.forEach((creator) => {
    const card = document.createElement("article");
    card.className = "creator-card";
    card.innerHTML = `
      <blockquote>${creator.quote}</blockquote>
      <p>${creator.text}</p>
      <div class="creator-thumb ${creator.thumbClass}"></div>
    `;
    elements.creators.appendChild(card);
  });
}

function renderScene(index) {
  const scene = scenes[index];
  if (!scene) {
    return;
  }

  elements.tag.textContent = scene.tag;
  elements.kicker.textContent = scene.kicker;
  elements.title.textContent = scene.title;
  elements.destination.textContent = scene.destination;
  elements.days.textContent = scene.days;
  elements.weather.textContent = scene.weather;
  elements.scenery.textContent = scene.scenery;
  elements.copy.textContent = scene.copy;
  elements.day1.textContent = scene.day1;
  elements.day2.textContent = scene.day2;
  elements.sceneCaption.textContent = scene.caption;
  elements.detailTitle.textContent = scene.detailTitle;
  elements.detailCopy.textContent = scene.detailCopy;
  elements.detailFit.textContent = scene.detailFit;
  elements.detailRhythm.textContent = scene.detailRhythm;
  elements.detailHighlight.textContent = scene.detailHighlight;

  renderCreators(scene.creators);

  elements.sceneDots.forEach((dot, dotIndex) => {
    dot.classList.toggle("is-active", dotIndex === index);
  });

  elements.progressPills.forEach((pill, pillIndex) => {
    pill.classList.toggle("is-active", pillIndex === index);
  });

  currentSceneIndex = index;
}

function unlockPanelScrollLater() {
  window.clearTimeout(panelUnlockTimer);
  panelUnlockTimer = window.setTimeout(() => {
    isPanelAnimating = false;
  }, 860);
}

function updatePanelPosition() {
  const panelOffset = currentPanelIndex * window.innerHeight;
  elements.track.style.transform = `translate3d(0, -${panelOffset}px, 0)`;

  elements.pageDots.forEach((dot, dotIndex) => {
    dot.classList.toggle("is-active", dotIndex === currentPanelIndex);
  });
}

function goToPanel(index) {
  const nextIndex = Math.max(0, Math.min(index, elements.panels.length - 1));
  if (nextIndex === currentPanelIndex) {
    return;
  }

  currentPanelIndex = nextIndex;
  isPanelAnimating = true;
  updatePanelPosition();
  unlockPanelScrollLater();
}

function goToAdjacentPanel(direction) {
  if (isPanelAnimating) {
    return;
  }

  goToPanel(currentPanelIndex + direction);
}

function showNextScene() {
  renderScene((currentSceneIndex + 1) % scenes.length);
}

function handleWheel(event) {
  if (Math.abs(event.deltaY) < 24) {
    return;
  }

  event.preventDefault();
  goToAdjacentPanel(event.deltaY > 0 ? 1 : -1);
}

function handleKeydown(event) {
  if (event.defaultPrevented) {
    return;
  }

  if (["ArrowDown", "PageDown", " "].includes(event.key)) {
    event.preventDefault();
    goToAdjacentPanel(1);
  }

  if (["ArrowUp", "PageUp"].includes(event.key)) {
    event.preventDefault();
    goToAdjacentPanel(-1);
  }

  if (event.key === "Home") {
    event.preventDefault();
    goToPanel(0);
  }

  if (event.key === "End") {
    event.preventDefault();
    goToPanel(elements.panels.length - 1);
  }
}

function handleTouchStart(event) {
  touchStartY = event.touches[0].clientY;
}

function handleTouchEnd(event) {
  const touchEndY = event.changedTouches[0].clientY;
  const deltaY = touchStartY - touchEndY;

  if (Math.abs(deltaY) < 50) {
    return;
  }

  goToAdjacentPanel(deltaY > 0 ? 1 : -1);
}

elements.shuffle.addEventListener("click", showNextScene);

elements.sceneDots.forEach((dot) => {
  dot.addEventListener("click", () => {
    renderScene(Number(dot.dataset.index));
  });
});

elements.pageDots.forEach((dot) => {
  dot.addEventListener("click", () => {
    goToPanel(Number(dot.dataset.panelIndex));
  });
});

window.addEventListener("wheel", handleWheel, { passive: false });
window.addEventListener("keydown", handleKeydown);
window.addEventListener("touchstart", handleTouchStart, { passive: true });
window.addEventListener("touchend", handleTouchEnd, { passive: true });
window.addEventListener("resize", updatePanelPosition);

renderScene(currentSceneIndex);
updatePanelPosition();
