<template>
  <div class="brush-compare" :style="themeStyle">
    <div class="compare-screen">
      <div class="feed-glow"></div>

      <div class="feed-content">
        <div class="story-head">
          <span class="story-badge">牙刷对比</span>
          <p>轻滑切换机型，雷达图同步变化</p>
        </div>

        <div class="swipe-card-shell">
          <article class="product-card" :class="{ 'is-dragging': isDragging }" :style="productCardStyle" @pointerdown="onPointerDown">
            <div class="hero-row">
              <div class="product-visual">
                <div class="visual-aura"></div>
                <div class="brush-figure">
                  <span class="brush-head"></span>
                  <span class="brush-neck"></span>
                  <span class="brush-handle"></span>
                  <span class="brush-accent"></span>
                </div>
              </div>

              <div class="product-main">
                <div class="product-card__top">
                  <div>
                    <span class="product-chip">{{ currentProduct.chip }}</span>
                    <h2>{{ currentProduct.name }}</h2>
                  </div>
                  <div class="overall-box">
                    <strong>{{ averageScore(currentProduct.axes) }}</strong>
                  </div>
                </div>

                <p class="product-summary">{{ currentProduct.compareNote }}</p>

                <div class="product-meta">
                  <div class="meta-item">
                    <span>价位</span>
                    <strong>{{ currentProduct.price }}</strong>
                  </div>
                  <div class="meta-item">
                    <span>续航</span>
                    <strong>{{ currentProduct.battery }}</strong>
                  </div>
                  <div class="meta-item">
                    <span>噪音</span>
                    <strong>{{ currentProduct.noise }}</strong>
                  </div>
                </div>
              </div>
            </div>
          </article>
        </div>

        <section class="radar-panel">
          <div class="radar-panel__head">
            <div>
              <span class="panel-kicker">六维雷达图</span>
              <h3>{{ currentProduct.name }}</h3>
            </div>
            <p class="radar-copy">{{ currentProduct.summary }}</p>
          </div>

          <div class="radar-stage">
            <svg class="radar-chart" viewBox="0 0 320 320" aria-hidden="true">
              <g class="radar-grid">
                <polygon points="160,38 265.65,99 265.65,221 160,282 54.35,221 54.35,99"></polygon>
                <polygon points="160,62 244.78,111 244.78,209 160,258 75.22,209 75.22,111"></polygon>
                <polygon points="160,86 223.91,123 223.91,197 160,234 96.09,197 96.09,123"></polygon>
                <polygon points="160,110 203.04,135 203.04,185 160,210 116.96,185 116.96,135"></polygon>
                <polygon points="160,134 182.17,147 182.17,173 160,186 137.83,173 137.83,147"></polygon>
                <line x1="160" y1="160" x2="160" y2="28"></line>
                <line x1="160" y1="160" x2="274.32" y2="94"></line>
                <line x1="160" y1="160" x2="274.32" y2="226"></line>
                <line x1="160" y1="160" x2="160" y2="292"></line>
                <line x1="160" y1="160" x2="45.68" y2="226"></line>
                <line x1="160" y1="160" x2="45.68" y2="94"></line>
              </g>
              <polygon class="radar-area" :points="radarPolygonPoints"></polygon>
              <g>
                <circle
                  v-for="(point, index) in radarPointList"
                  :key="index"
                  class="radar-point"
                  :cx="point.x"
                  :cy="point.y"
                  r="5"
                ></circle>
              </g>
            </svg>

            <div
              v-for="(axis, index) in axes"
              :key="axis"
              class="radar-label"
              :class="labelClasses[index]"
            >
              <span>{{ axis }}</span>
              <strong>{{ displayAxes[index].toFixed(1) }}</strong>
            </div>
          </div>
        </section>

        <div class="product-dots">
          <button
            v-for="(product, index) in products"
            :key="product.id"
            class="dot-card"
            :class="{ 'is-active': index === currentIndex }"
            type="button"
            @click="setProduct(index)"
          >
            <span class="dot-color" :style="{ background: product.colors.accent }"></span>
            <span class="dot-name">{{ product.name }}</span>
            <strong>{{ averageScore(product.axes) }}</strong>
          </button>
        </div>

        <button class="caption-link" type="button" @click="goToReferenceVideo">
          <span>看参考测评视频</span>
          <strong>{{ currentProduct.name }}</strong>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import bus, { EVENT_KEY } from '@/utils/bus'
import { useNav } from '@/utils/hooks/useNav'
import { recommendedVideo } from '@/api/videos'

type Product = {
  id: string
  name: string
  chip: string
  price: string
  battery: string
  motor: string
  noise: string
  summary: string
  tags: string[]
  radarTitle: string
  radarCopy: string
  compareNote: string
  colors: {
    main: string
    accent: string
    deep: string
  }
  axes: number[]
}

const props = defineProps({
  active: {
    type: Boolean,
    default: false
  },
  item: {
    type: Object,
    default: () => ({})
  }
})

const nav = useNav()

const axes = ['清洁力', '续航', '护龈', '噪音', '颜值', '价格']
const labelClasses = [
  'radar-label-top',
  'radar-label-top-right',
  'radar-label-bottom-right',
  'radar-label-bottom',
  'radar-label-bottom-left',
  'radar-label-top-left'
]

const products: Product[] = [
  {
    id: 'laifen',
    name: 'Laifen Wave',
    chip: '旗舰刷感',
    price: '799 元',
    battery: '30 天',
    motor: '摆动 + 声波',
    noise: '58 dB',
    summary: '适合想从基础电动牙刷升级到更完整刷感的人，优点集中在清洁结构、做工和视觉质感。',
    tags: ['清洁轮廓最饱满', '刷感偏进阶', '设计感突出'],
    radarTitle: 'Laifen Wave 评分轮廓',
    radarCopy: '清洁力和颜值最强，价格维度偏保守，因此整体像高完成度升级款。',
    compareNote: '适合预算更高、明显在意刷感与外观的人。',
    colors: {
      main: '#d8f0c0',
      accent: '#8fda69',
      deep: '#1f4530'
    },
    axes: [9.2, 8.5, 8.3, 6.8, 9.5, 6.4]
  },
  {
    id: 'oclean',
    name: 'Oclean X Pro Elite',
    chip: '均衡全能',
    price: '599 元',
    battery: '35 天',
    motor: '84,000 次/分声波',
    noise: '45 dB',
    summary: '六个维度最均衡的一款，静音、续航和价格更讨好大多数用户，属于容易买对的主流选项。',
    tags: ['综合分最高', '静音最强', '价格更稳'],
    radarTitle: 'Oclean X Pro Elite 评分轮廓',
    radarCopy: '轮廓整体更圆，说明没有明显短板，适合作为主流用户的一步到位方案。',
    compareNote: '适合大多数第一次认真买电动牙刷的人。',
    colors: {
      main: '#d7eff7',
      accent: '#74d2e7',
      deep: '#1d4050'
    },
    axes: [8.7, 9.4, 8.8, 9.1, 8.4, 8.8]
  },
  {
    id: 'oralb',
    name: 'Oral-B iO 3',
    chip: '圆头易上手',
    price: '499 元',
    battery: '14 天',
    motor: '微震 + 小圆头',
    noise: '52 dB',
    summary: '更适合看重上手门槛低、刷头路径好理解的人，小圆头和品牌认知会让体验更熟悉。',
    tags: ['入门更友好', '圆头路径直观', '品牌认知高'],
    radarTitle: 'Oral-B iO 3 评分轮廓',
    radarCopy: '清洁力依旧不错，但续航短一些，整体更像稳妥入门款而不是全能王。',
    compareNote: '适合想要圆头路线、希望容易适应的人。',
    colors: {
      main: '#f7dfe8',
      accent: '#f190b1',
      deep: '#53253a'
    },
    axes: [8.8, 6.5, 8.2, 7.1, 8.1, 8.4]
  }
]

const currentIndex = ref(0)
const displayAxes = ref<number[]>(new Array(6).fill(0))
const isDragging = ref(false)
const dragOffset = ref(0)
const dragRotation = ref(0)
const dragOpacity = ref(1)

const currentProduct = computed(() => products[currentIndex.value])
const themeStyle = computed(() => ({
  '--product-main': currentProduct.value.colors.main,
  '--product-accent': currentProduct.value.colors.accent,
  '--product-deep': currentProduct.value.colors.deep
}))

const productCardStyle = computed(() => ({
  transform: `translateX(${dragOffset.value}px) rotate(${dragRotation.value}deg)`,
  opacity: String(dragOpacity.value)
}))

function averageScore(values: number[]) {
  return (values.reduce((sum, value) => sum + value, 0) / values.length).toFixed(1)
}

function pointForAxis(index: number, value: number) {
  const center = 160
  const radius = 118
  const angle = -Math.PI / 2 + (Math.PI * 2 * index) / axes.length
  const length = (value / 10) * radius
  return {
    x: Number((center + Math.cos(angle) * length).toFixed(2)),
    y: Number((center + Math.sin(angle) * length).toFixed(2))
  }
}

const radarPointList = computed(() =>
  displayAxes.value.map((value, index) => {
    return pointForAxis(index, value)
  })
)

const radarPolygonPoints = computed(() =>
  radarPointList.value.map((point) => `${point.x},${point.y}`).join(' ')
)

let radarFrame = 0
let dragStartX = 0
let dragCurrentX = 0
let radarReplayTimer = 0

function replayRadar() {
  if (radarReplayTimer) {
    window.clearTimeout(radarReplayTimer)
  }
  displayAxes.value = new Array(axes.length).fill(0)
  radarReplayTimer = window.setTimeout(() => {
    animateRadar(currentProduct.value.axes)
  }, 80)
}

function animateRadar(nextValues: number[]) {
  const startValues = [...displayAxes.value]
  const startTime = performance.now()
  const duration = 620

  if (radarFrame) {
    cancelAnimationFrame(radarFrame)
  }

  const step = (now: number) => {
    const progress = Math.min((now - startTime) / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)
    displayAxes.value = nextValues.map((value, index) => {
      return startValues[index] + (value - startValues[index]) * eased
    })

    if (progress < 1) {
      radarFrame = requestAnimationFrame(step)
      return
    }

    displayAxes.value = [...nextValues]
  }

  radarFrame = requestAnimationFrame(step)
}

function resetDrag() {
  isDragging.value = false
  dragOffset.value = 0
  dragRotation.value = 0
  dragOpacity.value = 1
}

function setProduct(index: number) {
  currentIndex.value = (index + products.length) % products.length
  resetDrag()
  animateRadar(currentProduct.value.axes)
}

function changeProduct(step: number) {
  setProduct(currentIndex.value + step)
}

function onPointerDown(event: PointerEvent) {
  if (!props.active) return
  isDragging.value = true
  dragStartX = event.clientX
  dragCurrentX = event.clientX
}

function onPointerMove(event: PointerEvent) {
  if (!isDragging.value) return

  dragCurrentX = event.clientX
  const deltaX = dragCurrentX - dragStartX
  dragOffset.value = deltaX
  dragRotation.value = deltaX / 18
  dragOpacity.value = Math.max(0.72, 1 - Math.abs(deltaX) / 320)
}

function onPointerUp() {
  if (!isDragging.value) return

  const deltaX = dragCurrentX - dragStartX
  if (deltaX > 70) {
    changeProduct(-1)
    return
  }

  if (deltaX < -70) {
    changeProduct(1)
    return
  }

  resetDrag()
}

watch(
  () => props.active,
  (active) => {
    if (active) {
      replayRadar()
    }
  },
  { immediate: true }
)

function handleCurrentItem(item) {
  if (item?.aweme_id === props.item?.aweme_id) {
    replayRadar()
  }
}

async function goToReferenceVideo() {
  const res = await recommendedVideo({ start: 0, pageSize: 8 })
  if (!res?.success || !Array.isArray(res.data?.list) || !res.data.list.length) return
  nav('/video-detail', {}, { list: res.data.list, index: 0 })
}

onMounted(() => {
  window.addEventListener('pointermove', onPointerMove)
  window.addEventListener('pointerup', onPointerUp)
  window.addEventListener('pointercancel', onPointerUp)
  bus.on(EVENT_KEY.CURRENT_ITEM, handleCurrentItem)
})

onBeforeUnmount(() => {
  if (radarFrame) {
    cancelAnimationFrame(radarFrame)
  }
  if (radarReplayTimer) {
    window.clearTimeout(radarReplayTimer)
  }
  window.removeEventListener('pointermove', onPointerMove)
  window.removeEventListener('pointerup', onPointerUp)
  window.removeEventListener('pointercancel', onPointerUp)
  bus.off(EVENT_KEY.CURRENT_ITEM, handleCurrentItem)
})
</script>

<style scoped lang="less">
.brush-compare {
  height: 100%;
  padding-top: var(--home-header-height);
  box-sizing: border-box;
  color: #f7f9fc;
  background:
    radial-gradient(circle at 20% 18%, rgba(244, 78, 119, 0.12), transparent 22%),
    radial-gradient(circle at 80% 20%, rgba(63, 189, 255, 0.11), transparent 20%),
    radial-gradient(circle at 50% 100%, rgba(189, 247, 129, 0.08), transparent 28%),
    linear-gradient(180deg, #0b1119, #05070b);
  overflow: hidden;
  font-size: 14rem;

  .compare-screen {
    position: relative;
    height: calc(100% - var(--home-header-height));
    overflow: hidden;
  }

  .feed-glow {
    position: absolute;
    inset: 8% 16% auto;
    height: 180rem;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1), transparent 70%);
    filter: blur(28rem);
    pointer-events: none;
  }

  .feed-content {
    position: relative;
    z-index: 1;
    height: 100%;
    padding: 12rem 16rem 12rem 14rem;
    display: grid;
    grid-template-rows: auto 186rem 1fr auto auto;
    gap: 10rem;
  }

  .story-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12rem;
    padding-top: 4rem;
  }

  .story-badge {
    display: inline-flex;
    align-items: center;
    padding: 6rem 10rem;
    border-radius: 999rem;
    background: rgba(255, 255, 255, 0.07);
    border: 1rem solid rgba(255, 255, 255, 0.08);
    color: #fff;
    font-size: 11rem;
    letter-spacing: 0.06em;
  }

  .story-head p {
    margin: 0;
    color: rgba(237, 242, 248, 0.78);
    font-size: 10rem;
    white-space: nowrap;
  }

  .panel-kicker,
  .caption-link span {
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .panel-kicker {
    font-size: 10rem;
    color: #d8efc7;
  }

  .swipe-card-shell {
    position: relative;
    min-height: 186rem;
  }

  .product-card,
  .radar-panel,
  .dot-card {
    border-radius: 20rem;
    background: rgba(255, 255, 255, 0.06);
    border: 1rem solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(16rem);
  }

  .product-card {
    position: relative;
    z-index: 1;
    height: 100%;
    padding: 12rem;
    touch-action: pan-y;
    user-select: none;
    transition: transform 0.24s ease, box-shadow 0.24s ease, opacity 0.24s ease;
    overflow: hidden;
  }

  .product-card.is-dragging {
    transition: none;
    box-shadow: 0 18rem 36rem rgba(0, 0, 0, 0.3);
  }

  .hero-row {
    display: grid;
    grid-template-columns: 124rem minmax(0, 1fr);
    gap: 12rem;
    height: 100%;
    align-items: center;
  }

  .product-visual {
    position: relative;
    border-radius: 18rem;
    overflow: hidden;
    background:
      radial-gradient(circle at 50% 22%, rgba(255, 255, 255, 0.18), transparent 28%),
      linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02));
    min-height: 162rem;
  }

  .visual-aura {
    position: absolute;
    inset: 48% auto auto 50%;
    width: 110rem;
    height: 110rem;
    border-radius: 50%;
    background: radial-gradient(circle, var(--product-main) 0, transparent 68%);
    transform: translate(-50%, -50%);
    filter: blur(8rem);
    opacity: 0.38;
  }

  .brush-figure {
    position: absolute;
    inset: 0;
  }

  .brush-head,
  .brush-neck,
  .brush-handle,
  .brush-accent {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }

  .brush-head {
    top: 16rem;
    width: 38rem;
    height: 44rem;
    border-radius: 18rem 18rem 14rem 14rem;
    background: linear-gradient(180deg, #fff, #dfe7df 72%);
  }

  .brush-head::before,
  .brush-head::after {
    content: '';
    position: absolute;
    top: 8rem;
    width: 7rem;
    height: 16rem;
    border-radius: 999rem;
    background: linear-gradient(180deg, var(--product-accent), #f8fff3);
  }

  .brush-head::before {
    left: 9rem;
  }

  .brush-head::after {
    right: 9rem;
  }

  .brush-neck {
    top: 50rem;
    width: 10rem;
    height: 34rem;
    border-radius: 999rem;
    background: linear-gradient(180deg, #dfe8df, #a5b2a7);
  }

  .brush-handle {
    top: 78rem;
    width: 56rem;
    height: 106rem;
    border-radius: 28rem;
    background: linear-gradient(180deg, var(--product-main), var(--product-deep));
    box-shadow:
      inset 0 8rem 12rem rgba(255, 255, 255, 0.18),
      inset 0 -12rem 16rem rgba(0, 0, 0, 0.14),
      0 12rem 18rem rgba(0, 0, 0, 0.2);
  }

  .brush-accent {
    top: 112rem;
    width: 16rem;
    height: 34rem;
    border-radius: 999rem;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.2));
  }

  .product-main {
    min-width: 0;
    display: grid;
    align-content: center;
    gap: 10rem;
  }

  .product-card__top,
  .radar-panel__head {
    display: flex;
    justify-content: space-between;
    gap: 10rem;
  }

  .product-card__top {
    align-items: flex-start;
  }

  .product-chip {
    display: inline-flex;
    padding: 4rem 8rem;
    border-radius: 999rem;
    background: rgba(189, 247, 129, 0.16);
    color: #e7f8d9;
    font-size: 10rem;
  }

  h2,
  h3 {
    margin: 6rem 0 0;
    font-size: 19rem;
    line-height: 1.05;
  }

  .overall-box {
    min-width: 52rem;
    height: 52rem;
    display: grid;
    place-items: center;
    padding: 0;
    border-radius: 16rem;
    background: rgba(255, 255, 255, 0.08);
    text-align: right;
  }

  .meta-item span,
  .radar-label span,
  .dot-card span {
    display: block;
    color: rgba(237, 242, 248, 0.74);
    font-size: 10rem;
  }

  .overall-box strong {
    font-size: 18rem;
  }

  .product-meta {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8rem;
  }

  .meta-item {
    padding: 9rem 8rem;
    border-radius: 16rem;
    background: rgba(255, 255, 255, 0.05);
  }

  .meta-item strong,
  .radar-label strong,
  .dot-card strong {
    display: block;
    margin-top: 4rem;
  }

  .meta-item strong {
    font-size: 12rem;
  }

  .product-summary {
    margin: 0;
    color: rgba(237, 242, 248, 0.74);
    font-size: 11rem;
    line-height: 1.45;
  }

  .radar-panel {
    padding: 14rem 12rem 10rem;
    display: grid;
    grid-template-rows: auto 1fr;
  }

  .radar-panel__head {
    align-items: start;
  }

  .radar-copy {
    margin: 0;
    max-width: 144rem;
    color: rgba(237, 242, 248, 0.74);
    font-size: 10rem;
    line-height: 1.45;
    text-align: right;
  }

  .radar-stage {
    position: relative;
    min-height: 228rem;
  }

  .radar-chart {
    display: block;
    width: 230rem;
    margin: 6rem auto 0;
  }

  .radar-grid polygon,
  .radar-grid line {
    fill: none;
    stroke: rgba(255, 255, 255, 0.14);
    stroke-width: 1;
  }

  .radar-area {
    fill: rgba(189, 247, 129, 0.25);
    stroke: rgba(214, 255, 177, 0.92);
    stroke-width: 3;
    filter: drop-shadow(0 0 12rem rgba(189, 247, 129, 0.22));
  }

  .radar-point {
    fill: #f8fff3;
    stroke: rgba(189, 247, 129, 0.96);
    stroke-width: 3;
  }

  .radar-label {
    position: absolute;
    min-width: 48rem;
    text-align: center;

    strong {
      font-size: 11rem;
    }
  }

  .radar-label-top {
    top: 0;
    left: 50%;
    transform: translateX(-50%);
  }

  .radar-label-top-right {
    top: 48rem;
    right: 2rem;
  }

  .radar-label-bottom-right {
    right: 8rem;
    bottom: 52rem;
  }

  .radar-label-bottom {
    left: 50%;
    bottom: 6rem;
    transform: translateX(-50%);
  }

  .radar-label-bottom-left {
    left: 8rem;
    bottom: 52rem;
  }

  .radar-label-top-left {
    top: 48rem;
    left: 2rem;
  }

  .product-dots {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8rem;
  }

  .dot-card {
    min-width: 0;
    display: grid;
    justify-items: center;
    gap: 4rem;
    padding: 8rem 6rem;
    cursor: pointer;
    transition: border-color 0.2s ease, transform 0.2s ease, background-color 0.2s ease;
    color: #fff;
  }

  .dot-card.is-active {
    border-color: rgba(189, 247, 129, 0.45);
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2rem);
  }

  .dot-color {
    width: 10rem;
    height: 10rem;
    border-radius: 50%;
    box-shadow: 0 0 12rem rgba(255, 255, 255, 0.22);
  }

  .dot-name {
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    text-align: center;
  }

  .caption-link {
    width: 100%;
    padding: 10rem 12rem;
    border: 1rem solid rgba(255, 255, 255, 0.08);
    border-radius: 16rem;
    background: rgba(255, 255, 255, 0.05);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12rem;
    text-align: left;
    cursor: pointer;
  }

  .caption-link span {
    font-size: 10rem;
    color: rgba(237, 242, 248, 0.72);
  }

  .caption-link strong {
    margin: 0;
    font-size: 12rem;
    font-weight: 600;
  }
}
</style>
