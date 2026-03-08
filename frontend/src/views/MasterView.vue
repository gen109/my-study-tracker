<template>
  <div class="dashboard">

    <!-- ヘッダー -->
    <header class="header">
      <button class="back-btn" @click="router.push('/dashboard')">← 戻る</button>
      <h1 class="logo">出題範囲マスタ</h1>
      <span class="user-id">👤 {{ authStore.userId }}</span>
    </header>

    <main class="main">

      <div class="toolbar">
        <button class="csv-btn" @click="triggerCsvUpload">＋ CSV読み込み</button>
        <input ref="csvInput" type="file" accept=".csv" class="hidden" @change="handleCsvUpload" />
        <a class="template-link" :href="csvTemplateUrl" download="master_template.csv">
          CSVテンプレートをダウンロード
        </a>
      </div>

      <p v-if="importMessage" class="success">{{ importMessage }}</p>
      <p v-if="masterStore.errorMessage" class="error">{{ masterStore.errorMessage }}</p>

      <div class="content">

        <!-- 左：マスタ一覧 -->
        <div class="panel">
          <h2 class="panel-title">登録済みマスタ</h2>

          <div v-if="masterStore.isLoading" class="state-message">読み込み中...</div>
          <div v-else-if="masterStore.categories.length === 0" class="state-message">
            マスタが登録されていません。
          </div>
          <div v-else class="master-tree">
            <MasterNode
              v-for="node in masterStore.categories"
              :key="node.master_id"
              :node="node"
              :depth="0"
              @delete="handleDelete"
            />
          </div>
        </div>

        <!-- 右：手動登録フォーム -->
        <div class="panel">
          <h2 class="panel-title">手動登録</h2>
          <div class="form-group">
            <label>カテゴリ名</label>
            <input v-model="newName" type="text" placeholder="例：テクノロジ系" />
          </div>
          <div class="form-group">
            <label>親カテゴリ（任意）</label>
            <select v-model="newParentId" class="select-input">
              <option value="">なし（ルート）</option>
              <option
                v-for="flat in flatMasterCategories"
                :key="flat.master_id"
                :value="flat.master_id"
              >{{ '　'.repeat(flat.depth) }}{{ flat.name }}</option>
            </select>
          </div>
          <p v-if="formError" class="error">{{ formError }}</p>
          <button class="submit-btn" :disabled="masterStore.isLoading" @click="handleAdd">
            {{ masterStore.isLoading ? '登録中...' : '追加する' }}
          </button>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useMasterStore } from '@/stores/master'
import type { MasterCategory } from '@/stores/master'
import MasterNode from '@/components/MasterNode.vue'

const router = useRouter()
const authStore = useAuthStore()
const masterStore = useMasterStore()

const newName = ref('')
const newParentId = ref('')
const formError = ref('')
const importMessage = ref('')
const csvInput = ref<HTMLInputElement | null>(null)

// CSVテンプレートのデータURL
const csvTemplateUrl = computed(() => {
  const content = 'name,parent_name\n科目A,\nテクノロジ系,科目A\n基礎理論,テクノロジ系\n'
  const blob = new Blob([content], { type: 'text/csv' })
  return URL.createObjectURL(blob)
})

// フラットなマスタカテゴリ一覧（選択肢用）
const flatMasterCategories = computed(() => {
  const result: { master_id: string; name: string; depth: number }[] = []
  const flatten = (nodes: MasterCategory[], depth = 0) => {
    for (const node of nodes) {
      result.push({ master_id: node.master_id, name: node.name, depth })
      if (node.children?.length) flatten(node.children, depth + 1)
    }
  }
  flatten(masterStore.categories)
  return result
})

onMounted(async () => {
  if (authStore.userId) {
    await masterStore.fetchCategories(authStore.userId)
  }
})

function triggerCsvUpload() {
  csvInput.value?.click()
}

async function handleCsvUpload(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file || !authStore.userId) return
  const msg = await masterStore.importCsv(authStore.userId, file)
  if (msg) importMessage.value = msg
  ;(e.target as HTMLInputElement).value = ''
}

async function handleAdd() {
  if (!newName.value.trim()) {
    formError.value = 'カテゴリ名を入力してください'
    return
  }
  formError.value = ''
  await masterStore.createCategory(authStore.userId!, {
    name: newName.value.trim(),
    parent_id: newParentId.value || null,
  })
  await masterStore.fetchCategories(authStore.userId!)
  newName.value = ''
  newParentId.value = ''
}

async function handleDelete(masterId: string) {
  if (!authStore.userId) return
  await masterStore.deleteCategory(authStore.userId, masterId)
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

.toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.csv-btn {
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

.csv-btn:hover { background-color: #2980b9; }

.template-link {
  font-size: 0.85rem;
  color: #7f8c8d;
  text-decoration: underline;
  cursor: pointer;
}

.hidden { display: none; }

.content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.panel-title {
  font-size: 1rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 1rem;
}

.master-tree {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.state-message {
  color: #7f8c8d;
  font-size: 0.9rem;
  text-align: center;
  padding: 2rem 0;
}

.form-group { margin-bottom: 1.25rem; }

label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  color: #34495e;
  margin-bottom: 0.4rem;
}

input[type='text'] {
  width: 100%;
  padding: 0.65rem 0.75rem;
  border: 1px solid #dce1e7;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

input[type='text']:focus {
  outline: none;
  border-color: #3498db;
}

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

.select-input:focus {
  outline: none;
  border-color: #3498db;
}

.submit-btn {
  width: 100%;
  padding: 0.65rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:hover:not(:disabled) { background-color: #2980b9; }
.submit-btn:disabled { background-color: #bdc3c7; cursor: not-allowed; }

.success { color: #27ae60; font-size: 0.85rem; margin-bottom: 0.5rem; }
.error { color: #e74c3c; font-size: 0.85rem; margin-bottom: 0.5rem; }
</style>
