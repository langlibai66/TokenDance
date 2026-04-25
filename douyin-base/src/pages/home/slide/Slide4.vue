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

const BRUSH_COMPARE_CARD = {
  aweme_id: 'brush-compare-card',
  desc: '推荐专题：电动牙刷横向对比',
  type: 'brush-compare'
}

const FOOTBALL_PREVIEW_CARD = {
  aweme_id: 'football-preview-card',
  desc: '赛前看点：国家德比 皇马 vs 巴萨',
  type: 'football-preview'
}

const props = defineProps({
  active: {
    type: Boolean,
    default: false
  }
})

async function recommendedVideoWithBrushCard(params) {
  const res = await recommendedVideo(params)
  if (!res?.success) return res

  const start = params?.start ?? 0
  const list = Array.isArray(res.data?.list) ? [...res.data.list] : []
  let insertedCount = 0

  if (start === 0) {
    if (!list.some((item) => item.type === 'brush-compare')) {
      list.splice(Math.min(1, list.length), 0, BRUSH_COMPARE_CARD)
      insertedCount += 1
    }

    if (!list.some((item) => item.type === 'football-preview')) {
      list.splice(Math.min(3, list.length), 0, FOOTBALL_PREVIEW_CARD)
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
