<template>
  <div class="ai-daily-card">
    <div class="daily-screen">
      <div class="hero-glow"></div>

      <div class="daily-content">
        <header class="daily-head">
          <div>
            <span class="section-chip">AI 日报</span>
            <h2>模型竞速 + 具身落地</h2>
            <p>今日 3 条高优先级动态速览</p>
          </div>
          <div class="daily-meta">
            <strong>04 / 24</strong>
            <span>Agent / 大模型 / 机器人</span>
          </div>
        </header>

        <section class="headline-card headline-deepseek" @click="handleHeadlineClick">
          <div class="headline-top">
            <span class="headline-rank">01</span>
            <div>
              <strong>DeepSeek V4 正式开源发布</strong>
              <p>1.6 万亿参数 MoE，100 万 Token，上线 V4-Pro + V4-Flash 双版本</p>
            </div>
          </div>
          <div class="headline-metrics">
            <span>DSA 稀疏注意力</span>
            <span>Agent 能力拉满</span>
            <span>国产算力适配存疑</span>
          </div>
          <p class="headline-focus">
            值得关注：你一直跟进的 DeepSeek V4 已经正式落地，Agent 框架对具身任务链有直接参考价值，建议尽快补一轮 baseline。
          </p>
        </section>

        <section class="headline-grid">
          <article class="headline-card" @click="handleHeadlineClick">
            <div class="headline-top">
              <span class="headline-rank">02</span>
              <div>
                <strong>GPT-5.5 发布</strong>
                <p>7 周一大版本，定位真实工作 Agent</p>
              </div>
            </div>
            <div class="headline-metrics">
              <span>Terminal-Bench 82.7%</span>
              <span>SWE-Bench Pro 58.6%</span>
            </div>
            <p class="headline-focus">
              值得关注：几乎与 DeepSeek V4 同时上线，OpenAI 正在用高频版本节奏压缩窗口期，Agent 编码场景可直接用于实验室脚本自动化。
            </p>
          </article>

          <article class="headline-card" @click="handleHeadlineClick">
            <div class="headline-top">
              <span class="headline-rank">03</span>
              <div>
                <strong>国家电网 68 亿采购 8500 台具身机器人</strong>
                <p>电力巡检、带电作业、应急救援、仓储物流同步推进</p>
              </div>
            </div>
            <div class="headline-metrics">
              <span>2026 重点渗透</span>
              <span>总投资 68 亿元</span>
            </div>
            <p class="headline-focus">
              值得关注：这是具身智能走向大规模工业部署的强信号，电力巡检的点云和视觉感知场景与你的研究方向高度相关。
            </p>
          </article>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { _showNoticeDialog } from '@/utils'

function handleHeadlineClick() {
  _showNoticeDialog(
    '搜索功能开发中',
    '即将跳转搜索界面，请等待后续开发。',
    '#cfd8e8',
    () => {},
    '知道了'
  )
}
</script>

<style scoped lang="less">
.ai-daily-card {
  height: 100%;
  padding-top: var(--home-header-height);
  box-sizing: border-box;
  color: #eef5ff;
  background:
    radial-gradient(circle at 18% 12%, rgba(85, 190, 255, 0.18), transparent 24%),
    radial-gradient(circle at 86% 14%, rgba(151, 107, 255, 0.22), transparent 26%),
    linear-gradient(180deg, #07111f, #060913 58%, #02040a);
  overflow: hidden;
  font-size: 14rem;

  .daily-screen {
    position: relative;
    height: calc(100% - var(--home-header-height));
    overflow: hidden;
  }

  .hero-glow {
    position: absolute;
    inset: 7% 10% auto;
    height: 180rem;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.14), transparent 70%);
    filter: blur(34rem);
    pointer-events: none;
  }

  .daily-content {
    position: relative;
    z-index: 1;
    height: 100%;
    padding: 14rem 16rem 16rem;
    display: grid;
    grid-template-rows: auto auto 1fr;
    gap: 12rem;
    box-sizing: border-box;
  }

  .daily-head,
  .headline-card {
    border: 1rem solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(18rem);
  }

  .daily-head {
    border-radius: 24rem;
    padding: 16rem;
    display: flex;
    justify-content: space-between;
    gap: 12rem;
  }

  .section-chip {
    display: inline-block;
    font-size: 10rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(237, 242, 248, 0.74);
  }

  .daily-head h2 {
    margin: 6rem 0 4rem;
    font-size: 26rem;
    line-height: 1.05;
  }

  .daily-head p,
  .daily-meta span,
  .headline-top p,
  .headline-focus {
    margin: 0;
    color: rgba(237, 242, 248, 0.74);
    line-height: 1.45;
  }

  .daily-meta {
    text-align: right;
    display: flex;
    flex-direction: column;
    gap: 4rem;
    min-width: 104rem;

    strong {
      font-size: 18rem;
    }

    span {
      font-size: 12rem;
    }
  }

  .headline-grid {
    min-height: 0;
    display: grid;
    gap: 12rem;
    grid-template-rows: 1fr 1fr;
  }

  .headline-card {
    border-radius: 22rem;
    padding: 16rem;
    display: flex;
    flex-direction: column;
    gap: 12rem;
    cursor: pointer;
  }

  .headline-deepseek {
    background:
      linear-gradient(135deg, rgba(48, 131, 255, 0.2), rgba(145, 91, 255, 0.14)),
      rgba(255, 255, 255, 0.05);
  }

  .headline-top {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 12rem;
    align-items: start;

    strong {
      display: block;
      margin-bottom: 6rem;
      font-size: 18rem;
      line-height: 1.25;
    }

    p {
      font-size: 13rem;
    }
  }

  .headline-rank {
    width: 34rem;
    height: 34rem;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 13rem;
    font-weight: 700;
    background: rgba(255, 255, 255, 0.14);
    color: white;
    flex-shrink: 0;
  }

  .headline-metrics {
    display: flex;
    flex-wrap: wrap;
    gap: 8rem;

    span {
      padding: 6rem 10rem;
      border-radius: 999rem;
      background: rgba(255, 255, 255, 0.08);
      font-size: 12rem;
      color: #f2f7ff;
    }
  }

  .headline-focus {
    font-size: 13rem;
  }
}
</style>
