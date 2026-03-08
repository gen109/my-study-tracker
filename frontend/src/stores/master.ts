import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface MasterCategory {
  master_id: string
  name: string
  parent_id: string | null
  children: MasterCategory[]
}

export interface MasterCategoryCreate {
  name: string
  parent_id: string | null
}

const API_BASE = 'http://localhost:8000'

export const useMasterStore = defineStore('master', () => {
  const categories = ref<MasterCategory[]>([])
  const isLoading = ref(false)
  const errorMessage = ref('')

  // マスタカテゴリ一覧を取得
  async function fetchCategories(userId: string): Promise<void> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(`${API_BASE}/masters/?user_id=${userId}`)
      if (!response.ok) throw new Error('マスタの取得に失敗しました')
      categories.value = await response.json()
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
    } finally {
      isLoading.value = false
    }
  }

  // マスタカテゴリを登録
  async function createCategory(userId: string, category: MasterCategoryCreate): Promise<MasterCategory | null> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(`${API_BASE}/masters/?user_id=${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(category),
      })
      if (!response.ok) throw new Error('マスタの登録に失敗しました')
      return await response.json()
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
      return null
    } finally {
      isLoading.value = false
    }
  }

  // マスタカテゴリを削除
  async function deleteCategory(userId: string, masterId: string): Promise<boolean> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(`${API_BASE}/masters/${masterId}?user_id=${userId}`, {
        method: 'DELETE',
      })
      if (!response.ok) throw new Error('マスタの削除に失敗しました')
      await fetchCategories(userId)
      return true
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
      return false
    } finally {
      isLoading.value = false
    }
  }

  // CSVからインポート
  async function importCsv(userId: string, file: File): Promise<string | null> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await fetch(`${API_BASE}/masters/import-csv?user_id=${userId}`, {
        method: 'POST',
        body: formData,
      })
      if (!response.ok) throw new Error('CSVのインポートに失敗しました')
      const data = await response.json()
      await fetchCategories(userId)
      return data.message
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
      return null
    } finally {
      isLoading.value = false
    }
  }

  return {
    categories,
    isLoading,
    errorMessage,
    fetchCategories,
    createCategory,
    deleteCategory,
    importCsv,
  }
})
