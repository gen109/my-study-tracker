import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Category {
  category_id: string
  name: string
  exam_id: string
  parent_id: string | null
  children: Category[]
}

const API_BASE = 'http://localhost:8000'

export const useCategoryStore = defineStore('category', () => {
  const categories = ref<Category[]>([])
  const isLoading = ref(false)
  const errorMessage = ref('')

  // カテゴリ一覧を取得（階層構造）
  async function fetchCategories(userId: string, examId: string): Promise<void> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(
        `${API_BASE}/categories/${examId}?user_id=${userId}`
      )
      if (!response.ok) throw new Error('カテゴリの取得に失敗しました')
      categories.value = await response.json()
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
    } finally {
      isLoading.value = false
    }
  }

  return {
    categories,
    isLoading,
    errorMessage,
    fetchCategories,
  }
})
