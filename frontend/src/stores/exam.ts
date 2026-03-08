import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Exam {
  exam_id: string
  name: string
  exam_date: string | null
  has_range: boolean
}

export interface ExamCreate {
  name: string
  exam_date: string | null
  has_range: boolean
}

const API_BASE = 'http://localhost:8000'

export const useExamStore = defineStore('exam', () => {
  const exams = ref<Exam[]>([])
  const isLoading = ref(false)
  const errorMessage = ref('')

  // 試験一覧を取得
  async function fetchExams(userId: string) {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(`${API_BASE}/exams/?user_id=${userId}`)
      if (!response.ok) throw new Error('試験一覧の取得に失敗しました')
      exams.value = await response.json()
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
    } finally {
      isLoading.value = false
    }
  }

  // 試験を新規登録
  async function createExam(userId: string, exam: ExamCreate): Promise<Exam | null> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(`${API_BASE}/exams/?user_id=${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(exam),
      })
      if (!response.ok) throw new Error('試験の登録に失敗しました')
      const created: Exam = await response.json()
      exams.value.push(created)
      return created
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
      return null
    } finally {
      isLoading.value = false
    }
  }

// 試験を削除
  async function deleteExam(userId: string, examId: string): Promise<boolean> {
    isLoading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(`${API_BASE}/exams/${examId}?user_id=${userId}`, {
        method: 'DELETE',
      })
      if (!response.ok) throw new Error('試験の削除に失敗しました')
      exams.value = exams.value.filter((e) => e.exam_id !== examId)
      return true
    } catch (e) {
      errorMessage.value = e instanceof Error ? e.message : '不明なエラーが発生しました'
      return false
    } finally {
      isLoading.value = false
    }
  }

  return {
    exams,
    isLoading,
    errorMessage,
    fetchExams,
    createExam,
    deleteExam,
  }
})
