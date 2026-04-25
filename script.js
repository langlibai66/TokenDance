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
  dots: Array.from(document.querySelectorAll(".scene-dot")),
  progressPills: Array.from(document.querySelectorAll(".progress-pill"))
};

let currentIndex = 0;

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

  renderCreators(scene.creators);

  elements.dots.forEach((dot, dotIndex) => {
    dot.classList.toggle("is-active", dotIndex === index);
  });

  elements.progressPills.forEach((pill, pillIndex) => {
    pill.classList.toggle("is-active", pillIndex === index);
  });

  currentIndex = index;
}

function showNextScene() {
  renderScene((currentIndex + 1) % scenes.length);
}

elements.shuffle.addEventListener("click", showNextScene);

elements.dots.forEach((dot) => {
  dot.addEventListener("click", () => {
    renderScene(Number(dot.dataset.index));
  });
});

renderScene(currentIndex);
