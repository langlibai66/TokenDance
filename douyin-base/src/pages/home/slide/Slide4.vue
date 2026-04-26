<template>
  <SlideItem>
    <SlideList
      uniqueId="home"
      style="background: #000"
      :active="props.active"
      :api="recommendedVideoWithBrushCard"
    />
  </SlideItem>
</template>

<script setup lang="jsx">
import SlideItem from '@/components/slide/SlideItem.vue'
import SlideList from './SlideList.vue'
import { recommendedVideo } from '@/api/videos'
import { _storageGet } from '@/utils'
import { DEFAULT_FEED_PERSONA, FEED_PERSONA, FEED_PERSONA_STORAGE_KEY } from '@/constants/feedPersona'

const BRUSH_COMPARE_CARD = {
  aweme_id: 'brush-compare-card',
  desc: '推荐专题：iPhone 17 / iPhone 17 Air / iPhone 17 Pro 横评对比',
  type: 'brush-compare'
}

const FOOTBALL_PREVIEW_CARD = {
  aweme_id: 'football-preview-card',
  desc: '世界杯前瞻：葡萄牙国家队参赛球队观察',
  type: 'football-preview'
}

const AI_DAILY_CARD = {
  aweme_id: 'ai-daily-card',
  desc: 'AI 日报：DeepSeek、GPT-5.5 与具身智能大单',
  type: 'ai-daily'
}

const props = defineProps({
  active: {
    type: Boolean,
    default: false
  }
})

function isTechFeedPersona() {
  const persona = _storageGet(FEED_PERSONA_STORAGE_KEY, DEFAULT_FEED_PERSONA)
  return persona === FEED_PERSONA.TECH
}

function isSportsFeedPersona() {
  const persona = _storageGet(FEED_PERSONA_STORAGE_KEY, DEFAULT_FEED_PERSONA)
  return persona === FEED_PERSONA.SPORTS
}

function isAiFeedPersona() {
  const persona = _storageGet(FEED_PERSONA_STORAGE_KEY, DEFAULT_FEED_PERSONA)
  return persona === FEED_PERSONA.AI
}

async function recommendedVideoWithBrushCard(params) {
  const res = await recommendedVideo(params)
  if (!res?.success) return res

  const start = params?.start ?? 0
  const list = Array.isArray(res.data?.list) ? [...res.data.list] : []
  let insertedCount = 0

  if (start === 0 && isTechFeedPersona()) {
    if (!list.some((item) => item.type === 'brush-compare')) {
      list.splice(Math.min(3, list.length), 0, BRUSH_COMPARE_CARD)
      insertedCount += 1
    }
  }

  if (start === 0 && isSportsFeedPersona()) {
    if (!list.some((item) => item.type === 'football-preview')) {
      list.splice(Math.min(2, list.length), 0, FOOTBALL_PREVIEW_CARD)
      insertedCount += 1
    }
  }

  if (start === 0 && isAiFeedPersona()) {
    if (!list.some((item) => item.type === 'ai-daily')) {
      list.splice(Math.min(1, list.length), 0, AI_DAILY_CARD)
      insertedCount += 1
    }
  }

  return {
    ...res,
    data: {
      ...res.data,
      total: (res.data?.total ?? list.length) + insertedCount,
      list
    }
  }
}
</script>
