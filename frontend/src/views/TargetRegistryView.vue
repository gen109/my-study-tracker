<template>
  <div class="registry-container">
    <div class="registry-card">
      <h1 class="title">ターゲット・レジストリ</h1>
      <p class="subtitle">試験の登録・カテゴリ追加</p>

      <!-- モード切替 -->
      <div class="mode-tabs">
        <button class="tab-btn" :class="{ active: mode === 'new' }" @click="mode = 'new'">新規登録</button>
        <button class="tab-btn" :class="{ active: mode === 'add' }" @click="switchToAddMode">カテゴリ追加</button>
      </div>

      <!-- 新規登録モード -->
      <form v-if="mode === 'new'" @submit.prevent="handleSubmit">

        <div class="form-group">
          <label for="examName">試験名称</label>
          <input id="examName" v-model="examName" type="text" placeholder="例：基本情報技術者試験、AWS SAP" required />
        </div>

        <div class="form-group">
          <label for="examDate">試験日</label>
          <input id="examDate" v-model="examDate" type="date" />
        </div>

        <div class="form-group">
          <label>出題範囲設定</label>
          <div class="radio-group">
            <label class="radio-label"><input type="radio" v-model="hasRange" :value="false" /> なし</label>
            <label class="radio-label"><input type="radio" v-model="hasRange" :value="true" /> あり</label>
          </div>
        </div>

        <div v-if="hasRange" class="form-group">
          <label>階層カテゴリ</label>
          <div class="category-tree">
            <CategoryNode
              v-for="node in categoryTree"
              :key="node.id"
              :node="node"
              :depth="0"
              @add-child="addChild"
              @remove-node="removeNode"
            />
          </div>
          <button type="button" class="add-root-btn" @click="addRootCategory">＋ カテゴリを追加</button>
        </div>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>

        <button v-if="successMessage" type="button" class="back-btn-main" @click="router.push('/dashboard')">
          試験一覧に戻る
        </button>
        <button v-else type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? '登録中...' : '登録する' }}
        </button>

      </form>

      <!-- カテゴリ追加モード -->
      <form v-else @submit.prevent="handleAddCategories">

        <div class="form-group">
          <label>対象試験</label>
          <select v-model="selectedExamId" class="select-input" required>
            <option value="" disabled>試験を選択してください</option>
            <option v-for="exam in examStore.exams" :key="exam.exam_id" :value="exam.exam_id">
              {{ exam.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>追加するカテゴリ</label>
          <div class="category-tree">
            <CategoryNode
              v-for="node in categoryTree"
              :key="node.id"
              :node="node"
              :depth="0"
              @add-child="addChild"
              @remove-node="removeNode"
            />
          </div>
          <button type="button" class="add-root-btn" @click="addRootCategory">＋ カテゴリを追加</button>
        </div>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>

        <button v-if="successMessage" type="button" class="back-btn-main" @click="router.push('/dashboard')">
          試験一覧に戻る
        </button>
        <button v-else type="submit" class="submit-btn" :disabled="isLoading || !selectedExamId">
          {{ isLoading ? '追加中...' : 'カテゴリを追加する' }}
        </button>

      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useExamStore } from '@/stores/exam'
import CategoryNode from '@/components/CategoryNode.vue'

const router = useRouter()
const authStore = useAuthStore()
const examStore = useExamStore()

const mode = ref<'new' | 'add'>('new')
const examName = ref('')
const examDate = ref('')
const hasRange = ref(false)
const selectedExamId = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

interface CategoryNodeType {
  id: string
  name: string
  children: CategoryNodeType[]
}

const categoryTree = ref<CategoryNodeType[]>([])

onMounted(async () => {
  if (authStore.userId) {
    await examStore.fetchExams(authStore.userId)
  }
})

async function switchToAddMode() {
  mode.value = 'add'
  categoryTree.value = []
  errorMessage.value = ''
  successMessage.value = ''
  if (authStore.userId) {
    await examStore.fetchExams(authStore.userId)
  }
}

function addRootCategory() {
  categoryTree.value.push({ id: crypto.randomUUID(), name: '', children: [] })
}

function addChild(parentId: string) {
  const addToNode = (nodes: CategoryNodeType[]): boolean => {
    for (const node of nodes) {
      if (node.id === parentId) {
        node.children.push({ id: crypto.randomUUID(), name: '', children: [] })
        return true
      }
      if (addToNode(node.children)) return true
    }
    return false
  }
  addToNode(categoryTree.value)
}

function removeNode(nodeId: string) {
  const removeFromNodes = (nodes: CategoryNodeType[]): CategoryNodeType[] => {
    return nodes
      .filter((n) => n.id !== nodeId)
      .map((n) => ({ ...n, children: removeFromNodes(n.children) }))
  }
  categoryTree.value = removeFromNodes(categoryTree.value)
}

// カテゴリを登録する共通処理（一時ID→実際のcategory_id マッピング）
async function registerCategories(examId: string, nodes: CategoryNodeType[]): Promise<boolean> {
  const idMap: Record<string, string> = {}
  const duplicates: string[] = []

  async function registerNode(node: CategoryNodeType, parentTempId: string | null) {
    const realParentId = parentTempId ? (idMap[parentTempId] ?? null) : null
    const res = await fetch(
      `http://localhost:8000/categories/?user_id=${authStore.userId}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: node.name, exam_id: examId, parent_id: realParentId }),
      }
    )
    const created = await res.json()
    idMap[node.id] = created.category_id

    if (node.children.length === 0 && created.is_new === false) {
      duplicates.push(node.name)
    }

    for (const child of node.children) {
      await registerNode(child, node.id)
    }
  }

  for (const node of nodes) {
    await registerNode(node, null)
  }

  if (duplicates.length > 0) {
    errorMessage.value = `「${duplicates.join('、')}」はすでに登録済みです`
    return false
  }
  return true
}

// 新規試験登録
async function handleSubmit() {
  if (!examName.value) {
    errorMessage.value = '試験名称を入力してください'
    return
  }
  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  const result = await examStore.createExam(authStore.userId!, {
    name: examName.value,
    exam_date: examDate.value || null,
    has_range: hasRange.value,
  })

  if (!result) {
    errorMessage.value = examStore.errorMessage
    isLoading.value = false
    return
  }

  if (hasRange.value && categoryTree.value.length > 0) {
    const ok = await registerCategories(result.exam_id, categoryTree.value)
    if (!ok) {
      isLoading.value = false
      return
    }
  }

  isLoading.value = false
  successMessage.value = `「${result.name}」を登録しました！`
  examName.value = ''
  examDate.value = ''
  hasRange.value = false
  categoryTree.value = []
}

// カテゴリ追加
async function handleAddCategories() {
  if (!selectedExamId.value) {
    errorMessage.value = '試験を選択してください'
    return
  }
  if (categoryTree.value.length === 0) {
    errorMessage.value = 'カテゴリを追加してください'
    return
  }
  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  const ok = await registerCategories(selectedExamId.value, categoryTree.value)
  isLoading.value = false

  if (ok) {
    successMessage.value = 'カテゴリを追加しました！'
    categoryTree.value = []
  }
}
</script>

<style scoped>
.registry-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  background-color: #f0f4f8;
  padding: 2rem;
}

.registry-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 560px;
}

.title {
  font-size: 1.6rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.subtitle {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.mode-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #f0f4f8;
}

.tab-btn {
  padding: 0.5rem 1.25rem;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #7f8c8d;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn.active { color: #3498db; border-bottom-color: #3498db; }
.tab-btn:hover { color: #3498db; }

.form-group { margin-bottom: 1.5rem; }

label {
  display: block;
  margin-bottom: 0.4rem;
  font-size: 0.9rem;
  color: #34495e;
  font-weight: 500;
}

input[type='text'],
input[type='date'] {
  width: 100%;
  padding: 0.65rem 0.75rem;
  border: 1px solid #dce1e7;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

input[type='text']:focus,
input[type='date']:focus { outline: none; border-color: #3498db; }

.select-input {
  width: 100%;
  padding: 0.65rem 0.75rem;
  border: 1px solid #dce1e7;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
  background: white;
  cursor: pointer;
}

.select-input:focus { outline: none; border-color: #3498db; }

.radio-group { display: flex; gap: 1.5rem; }

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: normal;
  cursor: pointer;
}

.category-tree { margin-bottom: 0.75rem; }

.add-root-btn {
  background: none;
  border: 1px dashed #3498db;
  color: #3498db;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.add-root-btn:hover { background-color: #ebf5fb; }

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
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) { background-color: #2980b9; }
.submit-btn:disabled { background-color: #bdc3c7; cursor: not-allowed; }

.back-btn-main {
  width: 100%;
  padding: 0.75rem;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.5rem;
}

.back-btn-main:hover { background-color: #219a52; }

.error { color: #e74c3c; font-size: 0.85rem; margin-bottom: 0.75rem; }
.success { color: #27ae60; font-size: 0.85rem; margin-bottom: 0.75rem; }
</style>
