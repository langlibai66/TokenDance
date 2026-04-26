export const FEED_PERSONA_STORAGE_KEY = 'home-feed-persona'

export const FEED_PERSONA = {
  TECH: 'tech',
  SPORTS: 'sports',
  AI: 'ai'
} as const

export type FeedPersona = (typeof FEED_PERSONA)[keyof typeof FEED_PERSONA]

export const DEFAULT_FEED_PERSONA: FeedPersona = FEED_PERSONA.TECH
