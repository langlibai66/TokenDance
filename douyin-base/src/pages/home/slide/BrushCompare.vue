<template>
  <div class="brush-compare" :style="themeStyle">
    <div class="compare-screen">
      <div class="feed-glow"></div>

      <div class="feed-content">
        <div class="story-head">
          <span class="story-badge">iPhone 横评</span>
          <p>点按切换三款 iPhone，3D 模型自动转动</p>
        </div>

        <div class="swipe-card-shell">
          <article class="product-card">
            <div class="hero-row">
              <div class="product-visual">
                <div class="visual-aura"></div>
                <GlbPhoneViewer
                  v-if="!modelErrors[currentProduct.id]"
                  :key="currentProduct.id"
                  class="phone-model"
                  :src="currentProduct.modelSrc"
                  :active="props.active"
                  @error="markModelError(currentProduct.id)"
                />
                <div v-else class="phone-figure" :class="currentProduct.visualClass">
                  <span class="phone-body"></span>
                  <span class="phone-island"></span>
                  <span class="phone-camera main"></span>
                  <span class="phone-camera top"></span>
                  <span class="phone-camera bottom"></span>
                  <span class="phone-flash"></span>
                  <span class="phone-shine"></span>
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
                    <span>定位</span>
                    <strong>{{ currentProduct.price }}</strong>
                  </div>
                  <div class="meta-item">
                    <span>芯片</span>
                    <strong>{{ currentProduct.chipSpec }}</strong>
                  </div>
                  <div class="meta-item">
                    <span>影像</span>
                    <strong>{{ currentProduct.camera }}</strong>
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
          <span>看 iPhone 17 横评视频</span>
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
import GlbPhoneViewer from './GlbPhoneViewer.vue'
import iphone17Glb from '@/assets/3d_data/glb/iphone-17.glb?url'
import iphone17AirGlb from '@/assets/3d_data/glb/iphone-17-air.glb?url'
import iphone17ProGlb from '@/assets/3d_data/glb/iphone-17-pro.glb?url'

type Product = {
  id: string
  name: string
  chip: string
  price: string
  chipSpec: string
  camera: string
  summary: string
  tags: string[]
  radarTitle: string
  radarCopy: string
  compareNote: string
  visualClass: string
  modelSrc: string
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

const axes = ['性能', '影像', '续航', '手感', '屏幕', '性价比']
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
    id: 'iphone17',
    name: 'iPhone 17',
    chip: '标准旗舰',
    price: '主流首选',
    chipSpec: 'A 系列',
    camera: '双摄',
    summary: 'iPhone 17 在性能、屏幕、手感和价格之间最均衡，是大多数人换机时最稳的选择。',
    tags: ['均衡体验', '价格更稳', '日常够用'],
    radarTitle: 'iPhone 17 评分轮廓',
    radarCopy: '整体表现没有明显短板，性价比和手感更突出，适合日常使用。',
    compareNote: '适合大多数日常使用、希望预算更稳的人。',
    visualClass: 'phone-standard',
    modelSrc: iphone17Glb,
    colors: {
      main: '#d9efff',
      accent: '#84c7ff',
      deep: '#23405f'
    },
    axes: [8.7, 8.2, 8.6, 9.1, 8.8, 9.0]
  },
  {
    id: 'iphone17-air',
    name: 'iPhone 17 Air',
    chip: '轻薄优先',
    price: '轻薄新档',
    chipSpec: 'A 系列',
    camera: '轻量影像',
    summary: 'iPhone 17 Air 的重点是更薄更轻，手感和便携性更强，适合不想拿重机身的人。',
    tags: ['轻薄机身', '手感最佳', '便携优先'],
    radarTitle: 'iPhone 17 Air 评分轮廓',
    radarCopy: '手感优势最明显，性能和屏幕保持旗舰水准，但影像和续航会为轻薄取舍。',
    compareNote: '适合看重轻薄、单手握持和随身携带体验的人。',
    visualClass: 'phone-air',
    modelSrc: iphone17AirGlb,
    colors: {
      main: '#f0f7ff',
      accent: '#bfd7ff',
      deep: '#30405c'
    },
    axes: [8.8, 8.0, 8.1, 9.8, 9.0, 7.8]
  },
  {
    id: 'iphone17-pro',
    name: 'iPhone 17 Pro',
    chip: '专业性能',
    price: '专业旗舰',
    chipSpec: 'A Pro',
    camera: '三摄',
    summary: 'iPhone 17 Pro 在性能释放、影像系统和屏幕表现上更强，适合重度拍摄和创作用户。',
    tags: ['性能更强', '三摄更全能', '屏幕更专业'],
    radarTitle: 'iPhone 17 Pro 评分轮廓',
    radarCopy: '性能、影像和屏幕维度明显领先，但价格和手感会比标准版更有负担。',
    compareNote: '适合经常拍摄、剪辑，或想要更完整旗舰能力的人。',
    visualClass: 'phone-pro',
    modelSrc: iphone17ProGlb,
    colors: {
      main: '#ece4ff',
      accent: '#b692ff',
      deep: '#39275e'
    },
    axes: [9.6, 9.5, 9.0, 8.2, 9.6, 7.2]
  }
]

const currentIndex = ref(0)
const displayAxes = ref<number[]>(new Array(6).fill(0))
const modelErrors = ref<Record<string, boolean>>({})

const currentProduct = computed(() => products[currentIndex.value])
const themeStyle = computed(() => ({
  '--product-main': currentProduct.value.colors.main,
  '--product-accent': currentProduct.value.colors.accent,
  '--product-deep': currentProduct.value.colors.deep
}))

function markModelError(id: string) {
  modelErrors.value = {
    ...modelErrors.value,
    [id]: true
  }
}

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

function setProduct(index: number) {
  const nextIndex = ((index % products.length) + products.length) % products.length
  if (nextIndex === currentIndex.value) {
    return
  }
  currentIndex.value = nextIndex
  animateRadar(currentProduct.value.axes)
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
  bus.on(EVENT_KEY.CURRENT_ITEM, handleCurrentItem)
})

onBeforeUnmount(() => {
  if (radarFrame) {
    cancelAnimationFrame(radarFrame)
  }
  if (radarReplayTimer) {
    window.clearTimeout(radarReplayTimer)
  }
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
    height: 100%;
    padding: 12rem;
    overflow: hidden;
    box-shadow: 0 18rem 36rem rgba(0, 0, 0, 0.26);
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

  .phone-model {
    position: absolute;
    inset: 8rem 7rem 12rem;
    width: calc(100% - 14rem);
    height: calc(100% - 20rem);
    filter: drop-shadow(0 15rem 20rem rgba(0, 0, 0, 0.26));
    pointer-events: none;
  }

  .phone-figure {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 68rem;
    height: 136rem;
    transform: translate(-50%, -50%) rotate(-7deg);
  }

  .phone-body {
    position: absolute;
    inset: 0;
    border-radius: 18rem;
    background:
      linear-gradient(135deg, rgba(255, 255, 255, 0.42), transparent 32%),
      linear-gradient(180deg, var(--product-main), var(--product-deep));
    border: 2rem solid rgba(255, 255, 255, 0.64);
    box-shadow:
      inset 0 8rem 14rem rgba(255, 255, 255, 0.22),
      inset 0 -14rem 18rem rgba(0, 0, 0, 0.18),
      0 18rem 28rem rgba(0, 0, 0, 0.3);
  }

  .phone-island,
  .phone-camera,
  .phone-flash,
  .phone-shine {
    position: absolute;
  }

  .phone-island {
    top: 10rem;
    left: 50%;
    width: 28rem;
    height: 8rem;
    transform: translateX(-50%);
    border-radius: 999rem;
    background: rgba(4, 8, 14, 0.8);
  }

  .phone-camera {
    width: 16rem;
    height: 16rem;
    border-radius: 50%;
    background:
      radial-gradient(circle at 42% 38%, rgba(255, 255, 255, 0.9) 0 2rem, transparent 3rem),
      radial-gradient(circle, #182131 0 38%, #05070b 42% 100%);
    border: 2rem solid rgba(255, 255, 255, 0.72);
    box-shadow: 0 2rem 6rem rgba(0, 0, 0, 0.25);
  }

  .phone-camera.main {
    top: 34rem;
    left: 13rem;
  }

  .phone-camera.top {
    top: 34rem;
    right: 13rem;
  }

  .phone-camera.bottom {
    top: 58rem;
    left: 13rem;
  }

  .phone-flash {
    top: 61rem;
    right: 17rem;
    width: 8rem;
    height: 8rem;
    border-radius: 50%;
    background: #fff6cf;
  }

  .phone-shine {
    inset: 10rem auto auto 10rem;
    width: 18rem;
    height: 80rem;
    border-radius: 999rem;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.34), transparent);
    transform: rotate(14deg);
  }

  .phone-air {
    width: 56rem;
    height: 136rem;
  }

  .phone-air .phone-body {
    border-radius: 16rem;
  }

  .phone-air .phone-camera.top,
  .phone-air .phone-camera.bottom,
  .phone-air .phone-flash {
    display: none;
  }

  .phone-air .phone-camera.main {
    left: 50%;
    transform: translateX(-50%);
  }

  .phone-pro {
    width: 72rem;
    height: 138rem;
  }

  .phone-pro .phone-body {
    border-color: rgba(255, 255, 255, 0.74);
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
