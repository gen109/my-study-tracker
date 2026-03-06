<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="title">my-study-tracker</h1>
      <p class="subtitle">学習成績管理システム</p>

      <form @submit.prevent="handleLogin">
        <!-- ユーザーID -->
        <div class="form-group">
          <label for="userId">ユーザーID</label>
          <input
            id="userId"
            v-model="userId"
            type="text"
            placeholder="ユーザーIDを入力"
            required
          />
        </div>

        <!-- パスワード -->
        <div class="form-group">
          <label for="password">パスワード</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="パスワードを入力"
            required
          />
        </div>

        <!-- 対象試験 -->
        <div class="form-group">
          <label for="examId">対象試験</label>
          <select id="examId" v-model="selectedExamId">
            <option value="">試験を選択してください</option>
            <option v-for="exam in exams" :key="exam.exam_id" :value="exam.exam_id">
              {{ exam.name }}
            </option>
          </select>
        </div>

        <button type="submit" class="login-btn">ログイン</button>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const userId = ref('')
const password = ref('')
const selectedExamId = ref('')
const errorMessage = ref('')

// 試験一覧（暫定：後でAPIから取得）
const exams = ref<{ exam_id: string; name: string }[]>([])

onMounted(async () => {
  // TODO: APIから試験一覧を取得する
  // const response = await fetch(`http://localhost:8000/exams/?user_id=${userId.value}`)
  // exams.value = await response.json()
})

function handleLogin() {
  // 暫定：ユーザーIDとパスワードの簡易チェック
  if (!userId.value || !password.value) {
    errorMessage.value = 'ユーザーIDとパスワードを入力してください'
    return
  }

  authStore.login(userId.value)

  if (selectedExamId.value) {
    authStore.selectExam(selectedExamId.value)
  }

  router.push('/dashboard')
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
}

.subtitle {
  color: #7f8c8d;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-size: 0.9rem;
  color: #34495e;
  font-weight: 500;
}

input,
select {
  width: 100%;
  padding: 0.65rem 0.75rem;
  border: 1px solid #dce1e7;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input:focus,
select:focus {
  outline: none;
  border-color: #3498db;
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
  margin-top: 0.5rem;
  transition: background-color 0.2s;
}

.login-btn:hover {
  background-color: #2980b9;
}

.error {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.75rem;
  text-align: center;
}
</style>
