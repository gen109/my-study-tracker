<template>
  <div class="dashboard">

    <!-- ヘッダー -->
    <header class="header">
      <button class="back-btn" @click="router.push('/dashboard')">← 戻る</button>
      <h1 class="logo">スコア入力</h1>
      <span class="user-id">👤 {{ authStore.userId }}</span>
    </header>

    <main class="main">

      <!-- 試験名 -->
      <div class="section-header">
        <h2 class="section-title">{{ currentExam?.name ?? '試験' }}</h2>
      </div>

      <!-- カテゴリ一覧 -->
      <div v-if="categoryStore.categories.length === 0" class="state-message">
        <p>カテゴリが登録されていません。</p>
        <button class="add-btn" @click="router.push('/registry')">
          試験設定に戻る
        </button>
      </div>

      <div v-else>
        <div class="score-table">
          <div class="table-header">
            <span class="col-check"></span>
            <span class="col-name">カテゴリ</span>
            <span class="col-score">満点</span>
            <span class="col-score">得点</span>
            <span class="col-compare">初回</span>
            <span class="col-compare">前回</span>
            <span class="col-compare">最新</span>
          </div>

          <template v-for="category in flatCategories" :key="category.category_id">
            <ScoreRow
              v-if="scoreInputs[category.category_id]"
              :category="category"
              :comparison="getComparison(category.category_id)"
              :modelValue="scoreInputs[category.category_id]!"
              :enabled="enabledMap[category.category_id] ?? false"
              @update:modelValue="scoreInputs[category.category_id] = $event"
              @update:enabled="enabledMap[category.category_id] = $event"
            />
          </template>
        </div>

        <p v-if="successMessage" class="success">{{ successMessage }}</p>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button
          class="submit-btn"
          :disabled="scoreStore.isLoading"
          @click="handleSubmit"
        >
          {{ scoreStore.isLoading ? '保存中...' : '保存する' }}
        </button>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useExamStore } from '@/stores/exam'
import { useCategoryStore } from '@/stores/category'
import { useScoreStore } from '@/stores/score'
import ScoreRow from '@/components/ScoreRow.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const examStore = useExamStore()
const categoryStore = useCategoryStore()
const scoreStore = useScoreStore()

const examId = route.params.examId as string
const successMessage = ref('')
const errorMessage = ref('')

// スコア入力値（category_id → { score, max_score }）
const scoreInputs = ref<Record<string, { score: string; max_score: string }>>({})

// チェック状態（category_id → boolean）
const enabledMap = ref<Record<string, boolean>>({})

// 現在の試験
const currentExam = computed(() =>
  examStore.exams.find((e) => e.exam_id === examId)
)

// カテゴリをフラットなリストに変換
const flatCategories = computed(() => {
  const result: { category_id: string; name: string; depth: number }[] = []
  const flatten = (nodes: typeof categoryStore.categories, depth = 0) => {
    for (const node of nodes) {
      result.push({ category_id: node.category_id, name: node.name, depth })
      if (node.children?.length) flatten(node.children, depth + 1)
    }
  }
  flatten(categoryStore.categories)
  return result
})

// 比較データを取得
function getComparison(categoryId: string) {
  return scoreStore.comparisons.find((c) => c.category_id === categoryId) ?? null
}

onMounted(async () => {
  if (!authStore.userId) return
  await categoryStore.fetchCategories(authStore.userId, examId)
  await scoreStore.fetchComparisons(authStore.userId, examId)
})

// flatCategoriesが更新されたらscoreInputsとenabledMapを初期化
watch(flatCategories, (cats) => {
  for (const cat of cats) {
    if (!scoreInputs.value[cat.category_id]) {
      scoreInputs.value[cat.category_id] = { score: '', max_score: '' }
    }
    if (enabledMap.value[cat.category_id] === undefined) {
      enabledMap.value[cat.category_id] = false
    }
  }
})

// 保存処理
async function handleSubmit() {
  successMessage.value = ''
  errorMessage.value = ''

  // チェックが入っていてかつスコアが入力されている行のみ保存
  const entries = Object.entries(scoreInputs.value).filter(
    ([categoryId, v]) =>
      enabledMap.value[categoryId] &&
      v.score !== '' &&
      v.max_score !== ''
  )

  if (entries.length === 0) {
    errorMessage.value = 'チェックを入れてスコアを入力してください'
    return
  }

  for (const [categoryId, values] of entries) {
    await scoreStore.createScore(authStore.userId!, {
      exam_id: examId,
      category_id: categoryId,
      score: Number(values.score),
      max_score: Number(values.max_score),
    })
  }

  if (!scoreStore.errorMessage) {
    successMessage.value = 'スコアを保存しました！'
    await scoreStore.fetchComparisons(authStore.userId!, examId)
  } else {
    errorMessage.value = scoreStore.errorMessage
  }
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

.back-btn {
  background: none;
  border: none;
  color: #3498db;
  font-size: 0.95rem;
  cursor: pointer;
  padding: 0;
}

.back-btn:hover { text-decoration: underline; }

.user-id {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.main {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem;
}

.section-header { margin-bottom: 1.5rem; }

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.score-table {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.table-header {
  display: grid;
  grid-template-columns: 40px 2fr 1fr 1fr 1fr 1fr 1fr;
  background-color: #f8f9fa;
  padding: 0.75rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #7f8c8d;
  border-bottom: 1px solid #dce1e7;
}

.col-check { text-align: center; }
.col-name { text-align: left; }
.col-score { text-align: center; }
.col-compare { text-align: center; }

.submit-btn {
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

.submit-btn:hover:not(:disabled) { background-color: #2980b9; }
.submit-btn:disabled { background-color: #bdc3c7; cursor: not-allowed; }

.add-btn {
  padding: 0.5rem 1.25rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
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

.success { color: #27ae60; font-size: 0.9rem; margin-bottom: 0.75rem; }
.error { color: #e74c3c; font-size: 0.9rem; margin-bottom: 0.75rem; }
</style>
