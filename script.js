const axes = ["清洁力", "续航", "护龈", "噪音", "颜值", "价格"];

const products = [
  {
    id: "laifen",
    name: "Laifen Wave",
    chip: "旗舰刷感",
    price: "799 元",
    battery: "30 天",
    motor: "摆动 + 声波",
    noise: "58 dB",
    summary: "适合想从基础电动牙刷升级到更完整刷感的人，优点集中在清洁结构、做工和视觉质感。",
    tags: ["清洁轮廓最饱满", "刷感偏进阶", "设计感突出"],
    radarTitle: "Laifen Wave 评分轮廓",
    radarCopy: "清洁力和颜值最强，价格维度偏保守，因此整体像高完成度升级款。",
    compareNote: "适合预算更高、明显在意刷感与外观的人。",
    colors: {
      main: "#d8f0c0",
      accent: "#8fda69",
      deep: "#1f4530"
    },
    axes: [9.2, 8.5, 8.3, 6.8, 9.5, 6.4],
    reasons: [
      "双动力结构带来更强包裹感，清洁轮廓最完整。",
      "出差通勤够用，但不是三款里最长。",
      "刷毛和力度过渡比较柔和，适合敏感牙龈。",
      "高频感更明显，安静程度不算最优。",
      "机身做工和配色最有家电质感。",
      "主机价格更高，性价比不是它的主卖点。"
    ]
  },
  {
    id: "oclean",
    name: "Oclean X Pro Elite",
    chip: "均衡全能",
    price: "599 元",
    battery: "35 天",
    motor: "84,000 次/分声波",
    noise: "45 dB",
    summary: "六个维度最均衡的一款，静音、续航和价格更讨好大多数用户，属于容易买对的主流选项。",
    tags: ["综合分最高", "静音最强", "价格更稳"],
    radarTitle: "Oclean X Pro Elite 评分轮廓",
    radarCopy: "轮廓整体更圆，说明没有明显短板，适合作为主流用户的一步到位方案。",
    compareNote: "适合大多数第一次认真买电动牙刷的人。",
    colors: {
      main: "#d7eff7",
      accent: "#74d2e7",
      deep: "#1d4050"
    },
    axes: [8.7, 9.4, 8.8, 9.1, 8.4, 8.8],
    reasons: [
      "清洁力稳定，属于日常使用很好理解的主流强度。",
      "续航最长，减少频繁充电打断。",
      "护龈模式更均衡，适合长期通用。",
      "低噪音优势最明显，夜刷也更友好。",
      "科技感强，但设计表达不是最张扬。",
      "在三款里价格压力最容易接受。"
    ]
  },
  {
    id: "oralb",
    name: "Oral-B iO 3",
    chip: "圆头易上手",
    price: "499 元",
    battery: "14 天",
    motor: "微震 + 小圆头",
    noise: "52 dB",
    summary: "更适合看重上手门槛低、刷头路径好理解的人，小圆头和品牌认知会让体验更熟悉。",
    tags: ["入门更友好", "圆头路径直观", "品牌认知高"],
    radarTitle: "Oral-B iO 3 评分轮廓",
    radarCopy: "清洁力依旧不错，但续航短一些，整体更像稳妥入门款而不是全能王。",
    compareNote: "适合想要圆头路线、希望容易适应的人。",
    colors: {
      main: "#f7dfe8",
      accent: "#f190b1",
      deep: "#53253a"
    },
    axes: [8.8, 6.5, 8.2, 7.1, 8.1, 8.4],
    reasons: [
      "小圆头路径直观，清洁力仍然在线。",
      "续航最短，需要更频繁充电。",
      "压力控制思路成熟，对新手更友好。",
      "噪音表现中规中矩，不算最安静。",
      "外观偏经典路线，辨识度稳定。",
      "主机价格可接受，入门压力较小。"
    ]
  }
];

const productSwitcher = document.getElementById("product-switcher");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");
const productCard = document.getElementById("product-card");
const productVisual = document.getElementById("product-visual");
const productChip = document.getElementById("product-chip");
const productName = document.getElementById("product-name");
const overallScore = document.getElementById("overall-score");
const productPrice = document.getElementById("product-price");
const productBattery = document.getElementById("product-battery");
const productMotor = document.getElementById("product-motor");
const productNoise = document.getElementById("product-noise");
const productSummary = document.getElementById("product-summary");
const tagRow = document.getElementById("tag-row");
const radarTitle = document.getElementById("radar-title");
const radarCopy = document.getElementById("radar-copy");
const radarArea = document.getElementById("radar-area");
const radarPoints = document.getElementById("radar-points");
const dimensionTable = document.getElementById("dimension-table");
const summaryRow = document.getElementById("summary-row");
const axisValueLabels = Array.from({ length: 6 }, (_, index) => document.getElementById(`label-${index}`));

let currentIndex = 0;
let currentRadarValues = new Array(6).fill(0);
let radarFrame = null;
let dragStartX = 0;
let dragCurrentX = 0;
let dragActive = false;

function averageScore(values) {
  return (values.reduce((sum, value) => sum + value, 0) / values.length).toFixed(1);
}

function pointForAxis(index, value) {
  const center = 160;
  const radius = 118;
  const angle = -Math.PI / 2 + (Math.PI * 2 * index) / axes.length;
  const length = (value / 10) * radius;
  const x = center + Math.cos(angle) * length;
  const y = center + Math.sin(angle) * length;
  return `${x.toFixed(2)},${y.toFixed(2)}`;
}

function renderRadar(values) {
  const points = values.map((value, index) => pointForAxis(index, value));
  radarArea.setAttribute("points", points.join(" "));
  radarPoints.innerHTML = values
    .map((value, index) => {
      const [x, y] = pointForAxis(index, value).split(",");
      return `<circle class="radar-point" cx="${x}" cy="${y}" r="5"></circle>`;
    })
    .join("");
}

function animateRadar(nextValues) {
  const startValues = [...currentRadarValues];
  const startTime = performance.now();
  const duration = 620;

  if (radarFrame) {
    cancelAnimationFrame(radarFrame);
  }

  function step(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const frameValues = nextValues.map((value, index) => startValues[index] + (value - startValues[index]) * eased);
    renderRadar(frameValues);

    if (progress < 1) {
      radarFrame = requestAnimationFrame(step);
      return;
    }

    currentRadarValues = [...nextValues];
  }

  radarFrame = requestAnimationFrame(step);
}

function renderSwitcher() {
  productSwitcher.innerHTML = products
    .map((product, index) => `<button class="switch-chip ${index === currentIndex ? "is-active" : ""}" type="button" data-index="${index}">${product.name}</button>`)
    .join("");
}

function renderComparisonTable() {
  dimensionTable.innerHTML = axes
    .map((axis, axisIndex) => {
      const productBars = products
        .map((product, productIndex) => {
          const activeClass = productIndex === currentIndex ? "is-active" : "";
          const value = product.axes[axisIndex].toFixed(1);
          return `
            <div class="dimension-product ${activeClass}" style="--product-main:${product.colors.main}; --product-accent:${product.colors.accent};">
              <div>
                <span>${product.name}</span>
                <strong>${value}</strong>
              </div>
              <div class="bar-track"><div class="bar-fill" style="width:${product.axes[axisIndex] * 10}%"></div></div>
            </div>
          `;
        })
        .join("");

      return `
        <article class="dimension-row">
          <div class="dimension-name">${axis}</div>
          <div class="dimension-products">${productBars}</div>
        </article>
      `;
    })
    .join("");
}

function renderSummaryCards() {
  summaryRow.innerHTML = products
    .map((product, index) => {
      const activeClass = index === currentIndex ? "is-active" : "";
      return `
        <article class="summary-card ${activeClass}" data-summary-index="${index}">
          <div class="summary-card__head">
            <div>
              <span>${product.chip}</span>
              <strong>${product.name}</strong>
            </div>
            <strong class="summary-score">${averageScore(product.axes)}</strong>
          </div>
          <p>${product.compareNote}</p>
        </article>
      `;
    })
    .join("");
}

function renderProduct(index) {
  currentIndex = (index + products.length) % products.length;
  const product = products[currentIndex];
  const overall = averageScore(product.axes);

  productCard.style.transform = "translateX(0px) rotate(0deg)";
  productCard.style.opacity = "1";
  productCard.classList.remove("is-dragging");

  productVisual.style.setProperty("--product-main", product.colors.main);
  productVisual.style.setProperty("--product-accent", product.colors.accent);
  productVisual.style.setProperty("--product-deep", product.colors.deep);

  productChip.textContent = product.chip;
  productName.textContent = product.name;
  overallScore.textContent = overall;
  productPrice.textContent = product.price;
  productBattery.textContent = product.battery;
  productMotor.textContent = product.motor;
  productNoise.textContent = product.noise;
  productSummary.textContent = product.summary;
  radarTitle.textContent = product.radarTitle;
  radarCopy.textContent = product.radarCopy;

  tagRow.innerHTML = product.tags.map((tag) => `<span class="tag-pill">${tag}</span>`).join("");
  axisValueLabels.forEach((label, idx) => {
    label.textContent = product.axes[idx].toFixed(1);
  });

  renderSwitcher();
  renderComparisonTable();
  renderSummaryCards();
  animateRadar(product.axes);
}

function changeProduct(step) {
  renderProduct(currentIndex + step);
}

function resetDrag() {
  dragActive = false;
  productCard.classList.remove("is-dragging");
  productCard.style.transform = "translateX(0px) rotate(0deg)";
  productCard.style.opacity = "1";
}

function onPointerDown(event) {
  dragActive = true;
  dragStartX = event.clientX;
  dragCurrentX = event.clientX;
  productCard.classList.add("is-dragging");
}

function onPointerMove(event) {
  if (!dragActive) {
    return;
  }

  dragCurrentX = event.clientX;
  const deltaX = dragCurrentX - dragStartX;
  const rotate = deltaX / 18;
  const opacity = Math.max(0.72, 1 - Math.abs(deltaX) / 320);
  productCard.style.transform = `translateX(${deltaX}px) rotate(${rotate}deg)`;
  productCard.style.opacity = opacity.toString();
}

function onPointerUp() {
  if (!dragActive) {
    return;
  }

  const deltaX = dragCurrentX - dragStartX;
  if (deltaX > 70) {
    resetDrag();
    changeProduct(-1);
    return;
  }

  if (deltaX < -70) {
    resetDrag();
    changeProduct(1);
    return;
  }

  resetDrag();
}

prevBtn.addEventListener("click", () => changeProduct(-1));
nextBtn.addEventListener("click", () => changeProduct(1));

productSwitcher.addEventListener("click", (event) => {
  const button = event.target.closest("[data-index]");
  if (!button) {
    return;
  }
  renderProduct(Number(button.dataset.index));
});

summaryRow.addEventListener("click", (event) => {
  const card = event.target.closest("[data-summary-index]");
  if (!card) {
    return;
  }
  renderProduct(Number(card.dataset.summaryIndex));
});

productCard.addEventListener("pointerdown", onPointerDown);
window.addEventListener("pointermove", onPointerMove);
window.addEventListener("pointerup", onPointerUp);
window.addEventListener("pointercancel", onPointerUp);

window.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight") {
    changeProduct(1);
  }

  if (event.key === "ArrowLeft") {
    changeProduct(-1);
  }
});

renderProduct(0);
