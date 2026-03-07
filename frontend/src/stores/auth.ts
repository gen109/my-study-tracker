import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const userId = ref<string | null>(null)
  const isLoggedIn = ref(false)
  const selectedExamId = ref<string | null>(null)

  function login(id: string) {
    userId.value = id
    isLoggedIn.value = true
  }

  function logout() {
    userId.value = null
    isLoggedIn.value = false
    selectedExamId.value = null
  }

  function selectExam(examId: string) {
    selectedExamId.value = examId
  }

  return {
    userId,
    isLoggedIn,
    selectedExamId,
    login,
    logout,
    selectExam,
  }
}, {
  persist: true
})
