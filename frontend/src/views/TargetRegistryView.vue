<template>
  <div class="registry-container">
    <div class="registry-card">
      <h1 class="title">ターゲット・レジストリ</h1>
      <p class="subtitle">試験の登録・設定</p>

      <form @submit.prevent="handleSubmit">

        <!-- 試験名称 -->
        <div class="form-group">
          <label for="examName">試験名称</label>
          <input
            id="examName"
            v-model="examName"
            type="text"
            placeholder="例：基本情報技術者試験、AWS SAP"
            required
          />
        </div>

        <!-- 試験日 -->
        <div class="form-group">
          <label for="examDate">試験日</label>
          <input
            id="examDate"
            v-model="examDate"
            type="date"
          />
        </div>

        <!-- 出題範囲設定 -->
        <div class="form-group">
          <label>出題範囲設定</label>
          <div class="radio-group">
            <label class="radio-label">
              <input type="radio" v-model="hasRange" :value="false" /> なし
            </label>
            <label class="radio-label">
              <input type="radio" v-model="hasRange" :value="true" /> あり
            </label>
          </div>
        </div>

        <!-- 階層カテゴリ -->
        <div v-if="hasRange" class="form-group">
          <label>階層カテゴリ</label>
          <div class="category-tree">
            <CategoryNode
              v-for="(node, index) in categoryTree"
              :key="node.id"
              :node="node"
              :depth="0"
              @add-child="addChild"
              @remove-node="removeNode"
            />
          </div>
          <button type="button" class="add-root-btn" @click="addRootCategory">
            ＋ カテゴリを追加
          </button>
        </div>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? '登録中...' : '登録する' }}
        </button>

      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useExamStore } from '@/stores/exam'
import CategoryNode from '@/components/CategoryNode.vue'

const authStore = useAuthStore()
const examStore = useExamStore()

const examName = ref('')
const examDate = ref('')
const hasRange = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

// カテゴリツリーの型定義
interface CategoryNodeType {
  id: string
  name: string
  children: CategoryNodeType[]
}

const categoryTree = ref<CategoryNodeType[]>([])

// ルートカテゴリを追加
function addRootCategory() {
  categoryTree.value.push({
    id: crypto.randomUUID(),
    name: '',
    children: [],
  })
}

// 子カテゴリを追加
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

// カテゴリを削除
function removeNode(nodeId: string) {
  const removeFromNodes = (nodes: CategoryNodeType[]): CategoryNodeType[] => {
    return nodes
      .filter((n) => n.id !== nodeId)
      .map((n) => ({ ...n, children: removeFromNodes(n.children) }))
  }
  categoryTree.value = removeFromNodes(categoryTree.value)
}

// フォーム送信
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

  isLoading.value = false

  if (result) {
    successMessage.value = `「${result.name}」を登録しました！`
    examName.value = ''
    examDate.value = ''
    hasRange.value = false
    categoryTree.value = []
  } else {
    errorMessage.value = examStore.errorMessage
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

input[type='text'],
input[type='date'] {
  width: 100%;
  padding: 0.65rem 0.75rem;
  border: 1px solid #dce1e7;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input[type='text']:focus,
input[type='date']:focus {
  outline: none;
  border-color: #3498db;
}

.radio-group {
  display: flex;
  gap: 1.5rem;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: normal;
  cursor: pointer;
}

.category-tree {
  margin-bottom: 0.75rem;
}

.add-root-btn {
  background: none;
  border: 1px dashed #3498db;
  color: #3498db;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.add-root-btn:hover {
  background-color: #ebf5fb;
}

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
  transition: background-color 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.submit-btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.error {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-bottom: 0.75rem;
}

.success {
  color: #27ae60;
  font-size: 0.85rem;
  margin-bottom: 0.75rem;
}
</style>
