<template>
  <div class="exam-card">
    <div class="card-header">
      <h2 class="exam-name">{{ props.exam.name }}</h2>
      <span class="badge" :class="props.exam.has_range ? 'badge-active' : 'badge-none'">
        {{ props.exam.has_range ? '出題範囲あり' : '出題範囲なし' }}
      </span>
    </div>

    <div class="card-body">
      <p class="exam-date">
        📅 試験日：{{ props.exam.exam_date ? formatDate(props.exam.exam_date) : '未設定' }}
      </p>
    </div>

    <div class="card-footer">
      <button class="btn btn-primary" @click="$emit('go-score', props.exam.exam_id)">
        スコア入力
      </button>
      <button class="btn btn-secondary" @click="$emit('go-analysis', props.exam.exam_id)">
        分析を見る
      </button>
      <button class="btn btn-danger" @click="handleDelete">
        削除
      </button>
    </div>

    <!-- 削除確認ダイアログ -->
    <div v-if="showConfirm" class="confirm-overlay">
      <div class="confirm-dialog">
        <p>「{{ props.exam.name }}」を削除しますか？</p>
        <p class="confirm-note">この操作は元に戻せません。</p>
        <div class="confirm-actions">
          <button class="btn btn-secondary" @click="showConfirm = false">キャンセル</button>
          <button class="btn btn-danger" @click="confirmDelete">削除する</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Exam } from '@/stores/exam'

const props = defineProps<{
  exam: Exam
}>()

const emit = defineEmits<{
  (e: 'go-score', examId: string): void
  (e: 'go-analysis', examId: string): void
  (e: 'delete', examId: string): void
}>()

const showConfirm = ref(false)

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

function handleDelete() {
  showConfirm.value = true
}

function confirmDelete() {
  showConfirm.value = false
  emit('delete', props.exam.exam_id)
}
</script>

<style scoped>
.exam-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: box-shadow 0.2s;
  position: relative;
}

.exam-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.exam-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.6rem;
  border-radius: 20px;
  white-space: nowrap;
}

.badge-active {
  background-color: #ebf5fb;
  color: #2980b9;
}

.badge-none {
  background-color: #f2f3f4;
  color: #7f8c8d;
}

.exam-date {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0;
}

.card-footer {
  display: flex;
  gap: 0.75rem;
}

.btn {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover { background-color: #2980b9; }

.btn-secondary {
  background-color: #f0f4f8;
  color: #2c3e50;
}

.btn-secondary:hover { background-color: #dce1e7; }

.btn-danger {
  background-color: #fdf0f0;
  color: #e74c3c;
}

.btn-danger:hover { background-color: #fadbd8; }

.confirm-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.confirm-dialog {
  text-align: center;
  padding: 1rem;
}

.confirm-dialog p {
  font-size: 0.95rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.25rem;
}

.confirm-note {
  font-size: 0.8rem !important;
  font-weight: normal !important;
  color: #e74c3c !important;
  margin-bottom: 1rem !important;
}

.confirm-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.confirm-actions .btn {
  flex: none;
  padding: 0.4rem 1.25rem;
}
</style>
