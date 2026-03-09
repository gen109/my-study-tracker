<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="title">my-study-tracker</h1>
      <p class="subtitle">学習成績管理システム</p>

      <div class="form-group">
        <label for="userId">ユーザーID</label>
        <input
          id="userId"
          v-model="userId"
          type="text"
          placeholder="ユーザーIDを入力"
          @keydown.enter="handleLogin"
          autofocus
        />
      </div>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <button class="login-btn" :disabled="isLoading" @click="handleLogin">
        {{ isLoading ? 'ログイン中...' : 'ログイン' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const userId = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

async function handleLogin() {
  if (!userId.value.trim()) {
    errorMessage.value = 'ユーザーIDを入力してください'
    return
  }
  isLoading.value = true
  errorMessage.value = ''
  authStore.login(userId.value.trim())
  router.push('/dashboard')
  isLoading.value = false
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f4f8;
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.25rem;
  text-align: center;
}

.subtitle {
  color: #7f8c8d;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-size: 0.9rem;
  color: #34495e;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #dce1e7;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #3498db;
}

.error {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.login-btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}
</style>
