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

export interface ScoreUpdate {
  score: number
  max_score: number
  note?: string
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
  const histories = ref<Record<string, Score[]>>({}) // category_id → Score[]
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

  // スコアを編集
  async function updateScore(
    userId: string,
    examId: string,
    scoreId: string,
    body: ScoreUpdate
  ): Promise<Score | null> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(
        `${API_BASE}/scores/${examId}/${scoreId}?user_id=${userId}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        }
      )
      if (!response.ok) throw new Error('スコアの編集に失敗しました')
      return await response.json()
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
      return null
    } finally {
      isLoading.value = false
    }
  }

  // スコアを削除
  async function deleteScore(
    userId: string,
    examId: string,
    scoreId: string,
    categoryId: string
  ): Promise<boolean> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(
        `${API_BASE}/scores/${examId}/${scoreId}?user_id=${userId}`,
        { method: 'DELETE' }
      )
      if (!response.ok) throw new Error('スコアの削除に失敗しました')
      // ローカルの履歴からも削除
      if (histories.value[categoryId]) {
        histories.value[categoryId] = histories.value[categoryId].filter(
          (s) => s.score_id !== scoreId
        )
      }
      return true
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
      return false
    } finally {
      isLoading.value = false
    }
  }

  // カテゴリ別スコア全履歴を取得
  async function fetchHistory(
    userId: string,
    examId: string,
    categoryId: string
  ): Promise<void> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(
        `${API_BASE}/scores/${examId}/history?user_id=${userId}&category_id=${categoryId}`
      )
      if (!response.ok) throw new Error('履歴の取得に失敗しました')
      histories.value[categoryId] = await response.json()
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
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
    histories,
    isLoading,
    errorMessage,
    createScore,
    updateScore,
    deleteScore,
    fetchHistory,
    fetchComparisons,
  }
})
