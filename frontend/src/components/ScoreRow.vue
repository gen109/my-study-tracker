<template>
  <div class="score-row-wrapper">
    <!-- メイン行 -->
    <div class="score-row" :style="{ paddingLeft: `${category.depth * 20 + 16}px` }">
      <span class="col-check">
        <input
          type="checkbox"
          :checked="enabled"
          @change="$emit('update:enabled', ($event.target as HTMLInputElement).checked)"
        />
      </span>
      <span class="col-name" :class="{ disabled: !enabled }">
        <span v-if="category.depth > 0" class="depth-icon">└</span>
        {{ category.name }}
      </span>
      <span class="col-score">
        <input
          type="number"
          class="score-input"
          placeholder="満点"
          min="0"
          :value="modelValue.max_score"
          :disabled="!enabled"
          @input="updateField('max_score', ($event.target as HTMLInputElement).value)"
        />
      </span>
      <span class="col-score">
        <input
          type="number"
          class="score-input"
          placeholder="得点"
          min="0"
          :value="modelValue.score"
          :disabled="!enabled"
          @input="updateField('score', ($event.target as HTMLInputElement).value)"
        />
      </span>
      <span class="col-compare" :class="{ disabled: !enabled }">
        {{ comparison?.initial != null ? comparison.initial + '%' : '—' }}
      </span>
      <span class="col-compare" :class="{ disabled: !enabled }">
        {{ comparison?.previous != null ? comparison.previous + '%' : '—' }}
      </span>
      <span class="col-compare" :class="[{ disabled: !enabled }, latestClass]">
        {{ comparison?.latest != null ? comparison.latest + '%' : '—' }}
      </span>
      <span class="col-actions">
        <button class="icon-btn" title="履歴を表示" @click="toggleHistory">
          {{ showHistory ? '▲' : '▼' }}
        </button>
      </span>
    </div>

    <!-- 履歴パネル -->
    <div v-if="showHistory" class="history-panel">
      <div v-if="isLoadingHistory" class="history-loading">読み込み中...</div>
      <div v-else-if="historyList.length === 0" class="history-empty">履歴がありません</div>
      <div v-else class="history-list">
        <div
          v-for="(item, index) in historyList"
          :key="item.score_id"
          class="history-item"
        >
          <span class="history-label">{{ index + 1 }}回目</span>
          <span class="history-date">{{ formatDate(item.recorded_at) }}</span>

          <!-- 通常表示 -->
          <template v-if="editingScoreId !== item.score_id">
            <span class="history-score">{{ item.score }} / {{ item.max_score }}</span>
            <span class="history-rate">
              {{ item.max_score > 0 ? Math.round(item.score / item.max_score * 100) : 0 }}%
            </span>
            <span class="history-note">{{ item.note || '' }}</span>
            <div class="history-btns">
              <button class="edit-btn" @click="startEdit(item)">編集</button>
              <button class="delete-btn" @click="$emit('delete-score', item.score_id)">削除</button>
            </div>
          </template>

          <!-- 編集モード -->
          <template v-else>
            <input
              v-model="editScore"
              type="number"
              class="edit-input"
              placeholder="得点"
              min="0"
            />
            <span class="history-sep">/</span>
            <input
              v-model="editMaxScore"
              type="number"
              class="edit-input"
              placeholder="満点"
              min="0"
            />
            <input
              v-model="editNote"
              type="text"
              class="edit-input edit-note"
              placeholder="メモ"
            />
            <div class="history-btns">
              <button class="save-btn" @click="submitEdit(item)">保存</button>
              <button class="cancel-btn" @click="cancelEdit">キャンセル</button>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { Score, ScoreComparison, ScoreUpdate } from '@/stores/score'

const props = defineProps<{
  category: { category_id: string; name: string; depth: number }
  comparison: ScoreComparison | null
  modelValue: { score: string; max_score: string }
  enabled: boolean
  historyList: Score[]
  isLoadingHistory: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: { score: string; max_score: string }): void
  (e: 'update:enabled', value: boolean): void
  (e: 'load-history'): void
  (e: 'delete-score', scoreId: string): void
  (e: 'update-score', scoreId: string, body: ScoreUpdate): void
}>()

const showHistory = ref(false)
const editingScoreId = ref<string | null>(null)
const editScore = ref('')
const editMaxScore = ref('')
const editNote = ref('')

function toggleHistory() {
  showHistory.value = !showHistory.value
  if (showHistory.value) {
    emit('load-history')
  }
}

function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  return `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}`
}

function startEdit(item: Score) {
  editingScoreId.value = item.score_id
  editScore.value = String(item.score)
  editMaxScore.value = String(item.max_score)
  editNote.value = item.note ?? ''
}

function cancelEdit() {
  editingScoreId.value = null
}

function submitEdit(item: Score) {
  emit('update-score', item.score_id, {
    score: parseFloat(editScore.value),
    max_score: parseFloat(editMaxScore.value),
    note: editNote.value,
  })
  editingScoreId.value = null
}

function updateField(field: 'score' | 'max_score', value: string) {
  emit('update:modelValue', { ...props.modelValue, [field]: value })
}

const latestClass = computed(() => {
  const { latest, previous } = props.comparison ?? {}
  if (latest == null || previous == null) return ''
  if (latest > previous) return 'up'
  if (latest < previous) return 'down'
  return ''
})

// 履歴が更新されたら編集モードを解除
watch(() => props.historyList, () => {
  editingScoreId.value = null
})
</script>

<style scoped>
.score-row-wrapper {
  border-bottom: 1px solid #f0f4f8;
}

.score-row-wrapper:last-child {
  border-bottom: none;
}

.score-row {
  display: grid;
  grid-template-columns: 40px 2fr 1fr 1fr 1fr 1fr 1fr 40px;
  align-items: center;
  padding-top: 0.65rem;
  padding-bottom: 0.65rem;
  padding-right: 1rem;
  font-size: 0.9rem;
  color: #2c3e50;
}

.col-check { text-align: center; }
.col-name { display: flex; align-items: center; gap: 0.3rem; }
.col-score { text-align: center; }
.col-compare { text-align: center; color: #7f8c8d; }
.col-actions { text-align: center; }

.depth-icon { color: #bdc3c7; font-size: 0.8rem; }
.disabled { color: #bdc3c7; }

.score-input {
  width: 70px;
  padding: 0.3rem 0.5rem;
  border: 1px solid #dce1e7;
  border-radius: 4px;
  font-size: 0.9rem;
  text-align: center;
  transition: background-color 0.2s;
}

.score-input:focus { outline: none; border-color: #3498db; }
.score-input:disabled { background-color: #f2f3f4; color: #bdc3c7; cursor: not-allowed; }

.up { color: #2980b9; font-weight: 600; }
.down { color: #e74c3c; font-weight: 600; }

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #7f8c8d;
  font-size: 0.75rem;
  padding: 0.2rem 0.4rem;
}

.icon-btn:hover { color: #3498db; }

/* 履歴パネル */
.history-panel {
  background: #f8fafc;
  border-top: 1px solid #f0f4f8;
  padding: 0.75rem 1rem 0.75rem 3rem;
  font-size: 0.85rem;
}

.history-loading,
.history-empty {
  color: #7f8c8d;
  text-align: center;
  padding: 0.5rem 0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.history-item {
  display: grid;
  grid-template-columns: 60px 90px 100px 50px 1fr auto;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0;
}

.history-label {
  font-weight: 600;
  color: #2c3e50;
}

.history-date { color: #7f8c8d; }
.history-score { color: #2c3e50; }

.history-rate {
  font-weight: 600;
  color: #3498db;
}

.history-note { color: #7f8c8d; font-size: 0.8rem; }
.history-sep { color: #7f8c8d; }

.history-btns {
  display: flex;
  gap: 0.4rem;
}

.edit-btn,
.delete-btn,
.save-btn,
.cancel-btn {
  padding: 0.2rem 0.6rem;
  border: none;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
}

.edit-btn { background: #ebf5fb; color: #2980b9; }
.edit-btn:hover { background: #d6eaf8; }

.delete-btn { background: #fdf0f0; color: #e74c3c; }
.delete-btn:hover { background: #fadbd8; }

.save-btn { background: #eafaf1; color: #27ae60; }
.save-btn:hover { background: #d5f5e3; }

.cancel-btn { background: #f2f3f4; color: #7f8c8d; }
.cancel-btn:hover { background: #e5e8e8; }

.edit-input {
  width: 60px;
  padding: 0.2rem 0.4rem;
  border: 1px solid #dce1e7;
  border-radius: 4px;
  font-size: 0.85rem;
  text-align: center;
}

.edit-note {
  width: 120px;
  text-align: left;
}

.edit-input:focus { outline: none; border-color: #3498db; }
</style>
