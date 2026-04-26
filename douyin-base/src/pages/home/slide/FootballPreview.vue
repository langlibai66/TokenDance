<template>
  <div class="football-preview" :style="themeStyle">
    <div class="preview-screen">
      <div class="hero-glow"></div>

      <div class="preview-content">
        <header class="match-head">
          <div>
            <span class="section-chip">赛前看点</span>
            <h2>世界杯前瞻</h2>
            <p>葡萄牙国家队参赛球队观察</p>
          </div>
          <div class="match-meta">
            <strong>Portugal</strong>
            <span>阵容厚度与淘汰赛上限</span>
          </div>
        </header>

        <section class="match-banner">
          <div class="club club-real">
            <span class="club-badge">POR</span>
            <strong>葡萄牙</strong>
            <p>边路爆点 + 中场组织双线在线</p>
          </div>
          <div class="vs-box">
            <span>2026</span>
            <strong>WC</strong>
            <p>冲击四强的热门候选</p>
          </div>
          <div class="club club-barca">
            <span class="club-badge">11</span>
            <strong>核心轴线</strong>
            <p>B 费调度，B 席串联，莱奥提速，C 罗终结</p>
          </div>
        </section>

        <section class="focus-panel">
          <div class="panel-head">
            <span>三大看点</span>
            <strong>赛前速读</strong>
          </div>

          <article
            v-for="focus in focusList"
            :key="focus.title"
            class="focus-card"
            @click="handleFocusCardClick"
          >
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
          <span>球队倾向</span>
          <strong>葡萄牙上限够高，关键在防线抗压与锋线效率</strong>
          <p>如果中场先把比赛节奏接住，再把边锋单挑能力转化成禁区产出，葡萄牙具备连续过关的硬实力。</p>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { _showNoticeDialog } from '@/utils'

const props = defineProps({
  active: {
    type: Boolean,
    default: false
  }
})

const focusList = [
  {
    tag: '看点 01',
    title: '中场控制力决定葡萄牙能否把天赋稳定兑现',
    text: 'B 费、维蒂尼亚和 B 席的拿球与推进质量，将直接决定球队能不能持续把球送到危险区域。'
  },
  {
    tag: '看点 02',
    title: '莱奥与边路群的单点爆破，是打开僵局的最快方式',
    text: '当淘汰赛进入低容错节奏，葡萄牙最需要的是边锋把一对一优势转化成真实射门和制造犯规。'
  },
  {
    tag: '看点 03',
    title: '后场保护与高空防守，是冲击更深轮次的最后门槛',
    text: '葡萄牙进攻资源足够亮眼，但遇到冲吊和转换强队时，双中卫与门将的处理稳定性会成为关键变量。'
  }
]

const meterList = [
  { key: 'transition', label: '边路爆点', left: '葡萄牙', right: '世界杯强队均值', value: { left: 90, right: 78 } },
  { key: 'control', label: '中场控制', left: '葡萄牙', right: '世界杯强队均值', value: { left: 86, right: 80 } },
  { key: 'finishing', label: '禁区终结', left: '葡萄牙', right: '世界杯强队均值', value: { left: 82, right: 79 } }
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
  '--real-main': '#f56b6b',
  '--real-deep': '#6a1018',
  '--barca-main': '#55d3a4',
  '--barca-deep': '#0d4f3f'
}))

let frameId = 0

function handleFocusCardClick() {
  _showNoticeDialog(
    '搜索功能开发中',
    '即将跳转搜索界面，请等待后续开发。',
    '#cfd8e8',
    () => {},
    '知道了'
  )
}

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
    cursor: pointer;
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
