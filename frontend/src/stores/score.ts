import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface ScoreInput {
  exam_id: string
  category_id: string
  score: number
  max_score: number
  note?: string
}

export interface Score extends ScoreInput {
  score_id: string
  recorded_at: string
}

export interface ScoreComparison {
  category_id: string
  category_name: string
  initial: number | null
  previous: number | null
  latest: number | null
}

const API_BASE = 'http://localhost:8000'

export const useScoreStore = defineStore('score', () => {
  const comparisons = ref<ScoreComparison[]>([])
  const isLoading = ref(false)
  const errorMessage = ref('')

  // スコアを登録
  async function createScore(userId: string, score: ScoreInput): Promise<Score | null> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(`${API_BASE}/scores/?user_id=${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(score),
      })
      if (!response.ok) throw new Error('スコアの登録に失敗しました')
      return await response.json()
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
      return null
    } finally {
      isLoading.value = false
    }
  }

  // 比較データを取得（初回・前回・最新）
  async function fetchComparisons(userId: string, examId: string): Promise<void> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(
        `${API_BASE}/scores/${examId}/comparison?user_id=${userId}`
      )
      if (!response.ok) throw new Error('比較データの取得に失敗しました')
      comparisons.value = await response.json()
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
    } finally {
      isLoading.value = false
    }
  }

  return {
    comparisons,
    isLoading,
    errorMessage,
    createScore,
    fetchComparisons,
  }
})
