<template>
  <div class="dashboard">

    <header class="header">
      <button class="back-btn" @click="router.push('/dashboard')">← 戻る</button>
      <h1 class="logo">スコア入力</h1>
      <span class="user-id">👤 {{ authStore.userId }}</span>
    </header>

    <main class="main">

      <div class="section-header">
        <h2 class="section-title">{{ examName }}</h2>
      </div>

      <div v-if="isLoadingCategories" class="state-message"><p>読み込み中...</p></div>

      <div v-else-if="flatCategories.length === 0" class="state-message">
        <p>カテゴリが登録されていません。</p>
        <button class="add-btn" @click="router.push('/registry')">試験設定に戻る</button>
      </div>

      <div v-else>
        <div class="score-table">
          <div class="table-header">
            <span></span>
            <span class="col-name">カテゴリ</span>
            <span class="col-score">満点</span>
            <span class="col-score">得点</span>
            <span class="col-compare">初回</span>
            <span class="col-compare">前回</span>
            <span class="col-compare">最新</span>
            <span></span>
          </div>

          <template v-for="category in flatCategories" :key="category.category_id">
            <ScoreRow
              v-if="scoreInputs[category.category_id] !== undefined && enabledMap[category.category_id] !== undefined"
              :category="category"
              :comparison="comparisonMap[category.category_id] ?? null"
              v-model="scoreInputs[category.category_id]!"
              v-model:enabled="enabledMap[category.category_id]!"
              :historyList="historyMap[category.category_id] ?? []"
              :isLoadingHistory="loadingHistoryMap[category.category_id] ?? false"
              @load-history="fetchHistory(category.category_id)"
              @delete-score="(scoreId: string) => handleDeleteScore(category.category_id, scoreId)"
              @update-score="(scoreId: string, body: ScoreUpdateBody) => handleUpdateScore(category.category_id, scoreId, body)"
            />
          </template>
        </div>

        <p v-if="successMessage" class="success">{{ successMessage }}</p>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button class="submit-btn" :disabled="isSaving" @click="handleSubmit">
          {{ isSaving ? '保存中...' : '保存する' }}
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
import ScoreRow from '@/components/ScoreRow.vue'

// ScoreStoreに依存しない型定義
interface ScoreUpdateBody {
  score: number
  max_score: number
  note?: string
}

interface ScoreRecord {
  score_id: string
  category_id: string
  score: number
  max_score: number
  note?: string
  recorded_at: string
}

interface ComparisonData {
  category_id: string
  category_name: string
  initial: number | null
  previous: number | null
  latest: number | null
}

interface CategoryFlat {
  category_id: string
  name: string
  depth: number
}

const API = 'http://localhost:8000'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const examStore = useExamStore()
const categoryStore = useCategoryStore()

const examId = route.params.examId as string

const scoreInputs = ref<Record<string, { score: string; max_score: string }>>({})
const enabledMap = ref<Record<string, boolean>>({})
const historyMap = ref<Record<string, ScoreRecord[]>>({})
const loadingHistoryMap = ref<Record<string, boolean>>({})
const comparisonMap = ref<Record<string, ComparisonData>>({})

const isLoadingCategories = ref(true)
const isSaving = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const examName = computed(() =>
  examStore.exams.find(e => e.exam_id === examId)?.name ?? '試験'
)

const flatCategories = computed((): CategoryFlat[] => {
  const result: CategoryFlat[] = []
  const flatten = (nodes: typeof categoryStore.categories, depth = 0) => {
    for (const node of nodes) {
      result.push({ category_id: node.category_id, name: node.name, depth })
      if (node.children?.length) flatten(node.children, depth + 1)
    }
  }
  flatten(categoryStore.categories)
  return result
})

watch(flatCategories, (cats) => {
  for (const cat of cats) {
    if (!scoreInputs.value[cat.category_id]) {
      scoreInputs.value[cat.category_id] = { score: '', max_score: '' }
    }
    if (enabledMap.value[cat.category_id] === undefined) {
      enabledMap.value[cat.category_id] = false
    }
  }
}, { immediate: true })

async function fetchComparisons() {
  const cats = flatCategories.value
  for (const cat of cats) {
    const r = await fetch(
      `${API}/scores/${examId}/comparison?user_id=${authStore.userId}&category_id=${cat.category_id}`
    )
    if (r.ok) {
      const data = await r.json()
      comparisonMap.value[cat.category_id] = {
        category_id: cat.category_id,
        category_name: data.category_name ?? cat.name,
        initial:  data.initial  != null ? Math.round(data.initial  * 100) : null,
        previous: data.previous != null ? Math.round(data.previous * 100) : null,
        latest:   data.latest   != null ? Math.round(data.latest   * 100) : null,
      }
    }
  }
}

async function fetchHistory(categoryId: string) {
  loadingHistoryMap.value[categoryId] = true
  const res = await fetch(
    `${API}/scores/${examId}/history?user_id=${authStore.userId}&category_id=${categoryId}`
  )
  historyMap.value[categoryId] = res.ok ? await res.json() : []
  loadingHistoryMap.value[categoryId] = false
}

onMounted(async () => {
  if (!authStore.userId) return
  await examStore.fetchExams(authStore.userId)
  await categoryStore.fetchCategories(authStore.userId, examId)
  isLoadingCategories.value = false
  await fetchComparisons()
})

async function handleSubmit() {
  successMessage.value = ''
  errorMessage.value = ''
  isSaving.value = true

  const entries = Object.entries(scoreInputs.value).filter(
    ([id, v]) => enabledMap.value[id] && v.score !== '' && v.max_score !== ''
  )

  if (entries.length === 0) {
    errorMessage.value = 'チェックを入れてスコアを入力してください'
    isSaving.value = false
    return
  }

  for (const [categoryId, values] of entries) {
    await fetch(`${API}/scores/?user_id=${authStore.userId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        exam_id: examId,
        category_id: categoryId,
        score: Number(values.score),
        max_score: Number(values.max_score),
      }),
    })
    enabledMap.value[categoryId] = false
    scoreInputs.value[categoryId] = { score: '', max_score: '' }
  }

  await fetchComparisons()
  isSaving.value = false
  successMessage.value = 'スコアを保存しました！'
}

async function handleDeleteScore(categoryId: string, scoreId: string) {
  await fetch(`${API}/scores/${examId}/${scoreId}?user_id=${authStore.userId}`, {
    method: 'DELETE',
  })
  await fetchHistory(categoryId)
  await fetchComparisons()
}

async function handleUpdateScore(categoryId: string, scoreId: string, body: ScoreUpdateBody) {
  await fetch(`${API}/scores/${examId}/${scoreId}?user_id=${authStore.userId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  await fetchHistory(categoryId)
  await fetchComparisons()
}
</script>

<style scoped>
.dashboard { min-height: 100vh; background-color: #f0f4f8; }

.header {
  background: white;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.logo { font-size: 1.3rem; font-weight: 700; color: #2c3e50; margin: 0; }

.back-btn {
  background: none; border: none; color: #3498db;
  font-size: 0.95rem; cursor: pointer; padding: 0;
}
.back-btn:hover { text-decoration: underline; }

.user-id { font-size: 0.9rem; color: #7f8c8d; }

.main { max-width: 960px; margin: 0 auto; padding: 2rem; }
.section-header { margin-bottom: 1.5rem; }
.section-title { font-size: 1.3rem; font-weight: 700; color: #2c3e50; margin: 0; }

.score-table {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.table-header {
  display: grid;
  grid-template-columns: 40px 2fr 1fr 1fr 1fr 1fr 1fr 40px;
  background-color: #f8f9fa;
  padding: 0.75rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #7f8c8d;
  border-bottom: 1px solid #dce1e7;
}

.col-name { text-align: left; }
.col-score { text-align: center; }
.col-compare { text-align: center; }

.submit-btn {
  width: 100%; padding: 0.75rem;
  background-color: #3498db; color: white;
  border: none; border-radius: 6px;
  font-size: 1rem; font-weight: 600;
  cursor: pointer; transition: background-color 0.2s;
}
.submit-btn:hover:not(:disabled) { background-color: #2980b9; }
.submit-btn:disabled { background-color: #bdc3c7; cursor: not-allowed; }

.add-btn {
  padding: 0.5rem 1.25rem; background-color: #3498db; color: white;
  border: none; border-radius: 6px; font-size: 0.9rem; font-weight: 600; cursor: pointer;
}

.state-message {
  text-align: center; color: #7f8c8d; padding: 3rem 0;
  display: flex; flex-direction: column; align-items: center; gap: 1rem;
}

.success { color: #27ae60; font-size: 0.9rem; margin-bottom: 0.75rem; }
.error { color: #e74c3c; font-size: 0.9rem; margin-bottom: 0.75rem; }
</style>
