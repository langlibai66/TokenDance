<template>
  <div class="football-preview" :style="themeStyle">
    <div class="preview-screen">
      <div class="hero-glow"></div>

      <div class="preview-content">
        <header class="match-head">
          <div>
            <span class="section-chip">赛前看点</span>
            <h2>国家德比</h2>
            <p>皇马 vs 巴萨</p>
          </div>
          <div class="match-meta">
            <strong>伯纳乌</strong>
            <span>西甲焦点战</span>
          </div>
        </header>

        <section class="match-banner">
          <div class="club club-real">
            <span class="club-badge">RMA</span>
            <strong>皇家马德里</strong>
            <p>主场冲冠窗口</p>
          </div>
          <div class="vs-box">
            <span>04 / 26</span>
            <strong>VS</strong>
            <p>国家德比夜</p>
          </div>
          <div class="club club-barca">
            <span class="club-badge">FCB</span>
            <strong>巴塞罗那</strong>
            <p>年轻锋线提速</p>
          </div>
        </section>

        <section class="focus-panel">
          <div class="panel-head">
            <span>三大看点</span>
            <strong>赛前速读</strong>
          </div>

          <article v-for="focus in focusList" :key="focus.title" class="focus-card">
            <span class="focus-tag">{{ focus.tag }}</span>
            <strong>{{ focus.title }}</strong>
            <p>{{ focus.text }}</p>
          </article>
        </section>

        <section class="duel-panel">
          <div class="panel-head">
            <span>关键对位</span>
            <strong>比赛节奏</strong>
          </div>

          <div v-for="meter in meterList" :key="meter.label" class="meter-row">
            <div class="meter-labels">
              <span>{{ meter.left }}</span>
              <strong>{{ meter.label }}</strong>
              <span>{{ meter.right }}</span>
            </div>
            <div class="meter-track">
              <div class="meter-fill meter-fill-left" :style="{ width: animatedMeters[meter.key].left + '%' }"></div>
              <div class="meter-fill meter-fill-right" :style="{ width: animatedMeters[meter.key].right + '%' }"></div>
            </div>
          </div>
        </section>

        <footer class="prediction-card">
          <span>比赛倾向</span>
          <strong>皇马更稳，巴萨更快</strong>
          <p>如果皇马先把中场站住，德比赛事很可能会进入强度与转换拉满的对攻节奏。</p>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps({
  active: {
    type: Boolean,
    default: false
  }
})

const focusList = [
  {
    tag: '看点 01',
    title: '贝林厄姆与京多安谁能先拿住中场第二点',
    text: '皇马擅长把二点球变成推进起点，巴萨则更依赖控球落位后的二次组织。'
  },
  {
    tag: '看点 02',
    title: '维尼修斯冲击边路，巴萨年轻防线能否持续回追',
    text: '一旦巴萨高位压迫没能形成反抢，皇马的纵向推进会直接考验边后卫身后保护。'
  },
  {
    tag: '看点 03',
    title: '亚马尔和莱万的终结效率，决定巴萨反扑上限',
    text: '巴萨的机会质量未必少，关键是能不能在高压客场里把有限射门打成进球。'
  }
]

const meterList = [
  { key: 'transition', label: '转换冲击', left: '皇马', right: '巴萨', value: { left: 86, right: 75 } },
  { key: 'control', label: '阵地控制', left: '皇马', right: '巴萨', value: { left: 74, right: 88 } },
  { key: 'finishing', label: '门前效率', left: '皇马', right: '巴萨', value: { left: 84, right: 80 } }
]

const animatedMeters = ref(
  meterList.reduce(
    (acc, meter) => {
      acc[meter.key] = { left: 0, right: 0 }
      return acc
    },
    {} as Record<string, { left: number; right: number }>
  )
)

const themeStyle = computed(() => ({
  '--real-main': '#f4d68f',
  '--real-deep': '#5f4a20',
  '--barca-main': '#7aa7ff',
  '--barca-deep': '#102d6a'
}))

let frameId = 0

function replayMeters() {
  if (frameId) {
    cancelAnimationFrame(frameId)
  }

  animatedMeters.value = meterList.reduce(
    (acc, meter) => {
      acc[meter.key] = { left: 0, right: 0 }
      return acc
    },
    {} as Record<string, { left: number; right: number }>
  )

  const start = performance.now()
  const duration = 680

  const step = (now: number) => {
    const progress = Math.min((now - start) / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)
    animatedMeters.value = meterList.reduce(
      (acc, meter) => {
        acc[meter.key] = {
          left: meter.value.left * eased,
          right: meter.value.right * eased
        }
        return acc
      },
      {} as Record<string, { left: number; right: number }>
    )

    if (progress < 1) {
      frameId = requestAnimationFrame(step)
    }
  }

  frameId = requestAnimationFrame(step)
}

watch(
  () => props.active,
  (active) => {
    if (active) {
      replayMeters()
    }
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  if (frameId) {
    cancelAnimationFrame(frameId)
  }
})
</script>

<style scoped lang="less">
.football-preview {
  height: 100%;
  padding-top: var(--home-header-height);
  box-sizing: border-box;
  color: #f7f9fc;
  background:
    radial-gradient(circle at 20% 18%, rgba(252, 206, 84, 0.18), transparent 24%),
    radial-gradient(circle at 80% 16%, rgba(85, 128, 255, 0.2), transparent 24%),
    linear-gradient(180deg, #07101f, #04070d 60%, #020306);
  overflow: hidden;
  font-size: 14rem;

  .preview-screen {
    position: relative;
    height: calc(100% - var(--home-header-height));
    overflow: hidden;
  }

  .hero-glow {
    position: absolute;
    inset: 8% 12% auto;
    height: 170rem;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.12), transparent 70%);
    filter: blur(30rem);
    pointer-events: none;
  }

  .preview-content {
    position: relative;
    z-index: 1;
    height: 100%;
    padding: 14rem 16rem 16rem;
    display: grid;
    grid-template-rows: auto auto auto 1fr auto;
    gap: 12rem;
  }

  .match-head,
  .match-banner,
  .focus-panel,
  .duel-panel,
  .prediction-card {
    border: 1rem solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(18rem);
  }

  .match-head {
    border-radius: 24rem;
    padding: 16rem;
    display: flex;
    justify-content: space-between;
    gap: 14rem;
  }

  .section-chip,
  .panel-head span,
  .prediction-card span {
    font-size: 10rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(237, 242, 248, 0.72);
  }

  .match-head h2 {
    margin: 6rem 0 4rem;
    font-size: 26rem;
    line-height: 1;
  }

  .match-head p,
  .match-meta span,
  .focus-card p,
  .prediction-card p {
    margin: 0;
    color: rgba(237, 242, 248, 0.76);
    line-height: 1.45;
  }

  .match-meta {
    text-align: right;
    display: grid;
    align-content: start;
    gap: 4rem;
  }

  .match-meta strong {
    font-size: 16rem;
  }

  .match-banner {
    border-radius: 22rem;
    padding: 16rem 14rem;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 10rem;
  }

  .club,
  .vs-box {
    min-height: 96rem;
    border-radius: 18rem;
    padding: 12rem;
    display: grid;
    align-content: center;
    gap: 4rem;
  }

  .club {
    background: rgba(255, 255, 255, 0.04);
  }

  .club-real {
    box-shadow: inset 0 0 0 1rem rgba(244, 214, 143, 0.18);
  }

  .club-barca {
    box-shadow: inset 0 0 0 1rem rgba(122, 167, 255, 0.22);
    text-align: right;
  }

  .club-badge {
    display: inline-flex;
    width: fit-content;
    padding: 4rem 8rem;
    border-radius: 999rem;
    background: rgba(255, 255, 255, 0.08);
    font-size: 10rem;
  }

  .club-barca .club-badge {
    margin-left: auto;
  }

  .club strong,
  .vs-box strong,
  .focus-card strong,
  .prediction-card strong {
    font-size: 15rem;
  }

  .club p,
  .vs-box p {
    margin: 0;
    color: rgba(237, 242, 248, 0.72);
    font-size: 11rem;
  }

  .vs-box {
    text-align: center;
    min-width: 76rem;
  }

  .vs-box span {
    font-size: 11rem;
    color: rgba(237, 242, 248, 0.7);
  }

  .panel-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8rem;
    margin-bottom: 12rem;
  }

  .focus-panel,
  .duel-panel {
    border-radius: 22rem;
    padding: 14rem;
  }

  .focus-panel {
    display: grid;
    gap: 10rem;
  }

  .focus-card {
    border-radius: 16rem;
    padding: 12rem;
    background: rgba(255, 255, 255, 0.04);
    display: grid;
    gap: 6rem;
  }

  .focus-tag {
    width: fit-content;
    padding: 3rem 7rem;
    border-radius: 999rem;
    background: rgba(255, 255, 255, 0.06);
    font-size: 10rem;
    color: rgba(237, 242, 248, 0.7);
  }

  .duel-panel {
    display: grid;
    gap: 12rem;
  }

  .meter-row {
    display: grid;
    gap: 8rem;
  }

  .meter-labels {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 8rem;
    font-size: 11rem;
    color: rgba(237, 242, 248, 0.76);
  }

  .meter-labels strong {
    font-size: 12rem;
    color: #fff;
  }

  .meter-labels span:last-child {
    text-align: right;
  }

  .meter-track {
    position: relative;
    height: 10rem;
    border-radius: 999rem;
    background: rgba(255, 255, 255, 0.07);
    overflow: hidden;
  }

  .meter-fill {
    position: absolute;
    top: 0;
    height: 100%;
  }

  .meter-fill-left {
    left: 0;
    background: linear-gradient(90deg, rgba(244, 214, 143, 0.45), var(--real-main));
  }

  .meter-fill-right {
    right: 0;
    background: linear-gradient(270deg, rgba(122, 167, 255, 0.45), var(--barca-main));
  }

  .prediction-card {
    border-radius: 20rem;
    padding: 14rem 16rem;
    display: grid;
    gap: 6rem;
  }
}
</style>
