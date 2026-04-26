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
