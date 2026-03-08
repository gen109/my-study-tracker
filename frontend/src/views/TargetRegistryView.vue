<template>
  <div class="registry-container">
    <div class="registry-card">
      <h1 class="title">ターゲット・レジストリ</h1>
      <p class="subtitle">試験の登録・カテゴリ追加</p>

      <!-- モード切替 -->
      <div class="mode-tabs">
        <button class="tab-btn" :class="{ active: mode === 'new' }" @click="switchToNewMode">新規登録</button>
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
          <div class="category-label-row">
            <label>階層カテゴリ</label>
            <button type="button" class="master-load-btn" @click="openMasterModal()">
              📚 マスタから読み込む
            </button>
          </div>
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
          <div class="category-label-row">
            <label>追加するカテゴリ</label>
            <button type="button" class="master-load-btn" @click="openMasterModal()">
              📚 マスタから読み込む
            </button>
          </div>
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

    <!-- マスタ読み込みモーダル -->
    <div v-if="showMasterModal" class="modal-overlay" @click.self="showMasterModal = false">
      <div class="modal">
        <div class="modal-header">
          <h2 class="modal-title">出題範囲マスタから読み込む</h2>
          <button class="modal-close" @click="showMasterModal = false">✕</button>
        </div>

        <div v-if="masterStore.isLoading" class="modal-loading">読み込み中...</div>
        <div v-else-if="masterStore.categories.length === 0" class="modal-empty">
          <p>マスタが登録されていません。</p>
          <button class="link-btn" @click="router.push('/master')">出題範囲マスタを登録する</button>
        </div>
        <div v-else>
          <p class="modal-note">登録したいカテゴリにチェックを入れてください。</p>
          <div class="master-check-tree">
            <MasterCheckNode
              v-for="node in masterStore.categories"
              :key="node.master_id"
              :node="node"
              :depth="0"
              :selected-ids="selectedMasterIds"
              @toggle="toggleMasterId"
            />
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="showMasterModal = false">キャンセル</button>
            <button class="confirm-btn" @click="applyMasterSelection">
              選択した範囲を読み込む（{{ selectedMasterIds.size }}件）
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useExamStore } from '@/stores/exam'
import { useMasterStore } from '@/stores/master'
import type { MasterCategory } from '@/stores/master'
import CategoryNode from '@/components/CategoryNode.vue'
import MasterCheckNode from '@/components/MasterCheckNode.vue'

const router = useRouter()
const authStore = useAuthStore()
const examStore = useExamStore()
const masterStore = useMasterStore()

const mode = ref<'new' | 'add'>('new')
const examName = ref('')
const examDate = ref('')
const hasRange = ref(false)
const selectedExamId = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

// マスタモーダル
const showMasterModal = ref(false)
const selectedMasterIds = ref<Set<string>>(new Set())

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

function resetMessages() {
  errorMessage.value = ''
  successMessage.value = ''
}

function switchToNewMode() {
  mode.value = 'new'
  categoryTree.value = []
  resetMessages()
}

async function switchToAddMode() {
  mode.value = 'add'
  categoryTree.value = []
  resetMessages()
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

// マスタモーダルを開く
async function openMasterModal() {
  selectedMasterIds.value = new Set()
  showMasterModal.value = true
  if (authStore.userId) {
    await masterStore.fetchCategories(authStore.userId)
  }
}

// チェックボックスのトグル
function toggleMasterId(masterId: string) {
  if (selectedMasterIds.value.has(masterId)) {
    selectedMasterIds.value.delete(masterId)
  } else {
    selectedMasterIds.value.add(masterId)
  }
  // Set の reactivity を保つため再代入
  selectedMasterIds.value = new Set(selectedMasterIds.value)
}

// 選択したマスタカテゴリをツリーに変換して読み込む
function applyMasterSelection() {
  const selectedIds = selectedMasterIds.value

  // 選択されたノードを収集（フラット）
  const flatSelected: Map<string, MasterCategory> = new Map()
  function collectSelected(nodes: MasterCategory[]) {
    for (const node of nodes) {
      if (selectedIds.has(node.master_id)) {
        flatSelected.set(node.master_id, node)
      }
      if (node.children?.length) collectSelected(node.children)
    }
  }
  collectSelected(masterStore.categories)

  // master_id → 新しい一時ID のマッピング
  const masterToTempId: Map<string, string> = new Map()

  // 選択ノードを CategoryNodeType に変換（階層を保持）
  function buildTree(nodes: MasterCategory[]): CategoryNodeType[] {
    const result: CategoryNodeType[] = []
    for (const node of nodes) {
      if (!selectedIds.has(node.master_id)) continue
      const tempId = crypto.randomUUID()
      masterToTempId.set(node.master_id, tempId)
      const children = node.children?.length ? buildTree(node.children) : []
      result.push({ id: tempId, name: node.name, children })
    }
    return result
  }

  const newNodes = buildTree(masterStore.categories)

  // 既存ツリーに追加（重複名を除外）
  const existingNames = new Set<string>()
  function collectNames(nodes: CategoryNodeType[]) {
    for (const n of nodes) {
      existingNames.add(n.name)
      if (n.children?.length) collectNames(n.children)
    }
  }
  collectNames(categoryTree.value)

  function filterDuplicates(nodes: CategoryNodeType[]): CategoryNodeType[] {
    return nodes
      .filter((n) => !existingNames.has(n.name))
      .map((n) => ({ ...n, children: filterDuplicates(n.children) }))
  }

  const filtered = filterDuplicates(newNodes)
  categoryTree.value = [...categoryTree.value, ...filtered]

  showMasterModal.value = false
  selectedMasterIds.value = new Set()
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
  resetMessages()
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
  resetMessages()
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

.category-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.4rem;
}

.category-label-row label { margin-bottom: 0; }

.master-load-btn {
  background: none;
  border: 1px solid #8e44ad;
  color: #8e44ad;
  padding: 0.3rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.master-load-btn:hover { background-color: #f5eef8; }

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

/* モーダル */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 480px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #f0f4f8;
}

.modal-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  color: #7f8c8d;
  font-size: 1rem;
  cursor: pointer;
}

.modal-close:hover { color: #e74c3c; }

.modal-note {
  font-size: 0.85rem;
  color: #7f8c8d;
  padding: 0.75rem 1.5rem 0;
  margin: 0;
}

.modal-loading,
.modal-empty {
  padding: 2rem;
  text-align: center;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.modal-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.master-check-tree {
  padding: 0.75rem 1.5rem;
  overflow-y: auto;
  max-height: 50vh;
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #f0f4f8;
}

.cancel-btn {
  flex: 1;
  padding: 0.6rem;
  background: #f0f4f8;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #7f8c8d;
  cursor: pointer;
}

.cancel-btn:hover { background: #e5e8e8; }

.confirm-btn {
  flex: 2;
  padding: 0.6rem;
  background: #8e44ad;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
}

.confirm-btn:hover { background: #7d3c98; }

.link-btn {
  background: none;
  border: none;
  color: #3498db;
  font-size: 0.9rem;
  cursor: pointer;
  text-decoration: underline;
}
</style>
