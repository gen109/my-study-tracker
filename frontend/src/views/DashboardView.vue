<template>
  <div class="dashboard">

    <!-- ヘッダー -->
    <header class="header">
      <h1 class="logo">my-study-tracker</h1>
      <div class="header-right">
        <span class="user-id">👤 {{ authStore.userId }}</span>
        <button class="logout-btn" @click="handleLogout">ログアウト</button>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="main">

      <!-- タイトルエリア -->
      <div class="section-header">
        <h2 class="section-title">試験一覧</h2>
        <button class="add-btn" @click="router.push('/registry')">
          ＋ 試験を追加
        </button>
      </div>

      <!-- ローディング -->
      <div v-if="examStore.isLoading" class="state-message">
        読み込み中...
      </div>

      <!-- 試験なし -->
      <div v-else-if="examStore.exams.length === 0" class="state-message">
        <p>登録された試験がありません。</p>
        <button class="add-btn" @click="router.push('/registry')">
          ＋ 最初の試験を登録する
        </button>
      </div>

      <!-- 試験カード一覧 -->
      <div v-else class="exam-grid">
        <ExamCard
          v-for="exam in examStore.exams"
          :key="exam.exam_id"
          :exam="exam"
          @go-score="handleGoScore"
          @go-analysis="handleGoAnalysis"
        />
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useExamStore } from '@/stores/exam'
import ExamCard from '@/components/ExamCard.vue'

const router = useRouter()
const authStore = useAuthStore()
const examStore = useExamStore()

// 試験一覧を取得
onMounted(async () => {
  if (authStore.userId) {
    await examStore.fetchExams(authStore.userId)
  }
})

// ログアウト
function handleLogout() {
  authStore.logout()
  router.push('/')
}

// スコア入力画面へ（暫定）
function handleGoScore(examId: string) {
  console.log('スコア入力:', examId)
  // TODO: router.push(`/score/${examId}`)
}

// 分析画面へ（暫定）
function handleGoAnalysis(examId: string) {
  console.log('分析画面:', examId)
  // TODO: router.push(`/analysis/${examId}`)
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f0f4f8;
}

.header {
  background: white;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.logo {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-id {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.logout-btn {
  padding: 0.4rem 1rem;
  background: none;
  border: 1px solid #dce1e7;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #7f8c8d;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  border-color: #e74c3c;
  color: #e74c3c;
}

.main {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.add-btn {
  padding: 0.5rem 1.25rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-btn:hover {
  background-color: #2980b9;
}

.exam-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
}

.state-message {
  text-align: center;
  color: #7f8c8d;
  padding: 3rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
</style>
