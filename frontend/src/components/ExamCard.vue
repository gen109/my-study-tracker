<template>
  <div class="exam-card">
    <div class="card-header">
      <h2 class="exam-name">{{ exam.name }}</h2>
      <span class="badge" :class="exam.has_range ? 'badge-active' : 'badge-none'">
        {{ exam.has_range ? '出題範囲あり' : '出題範囲なし' }}
      </span>
    </div>

    <div class="card-body">
      <p class="exam-date">
        📅 試験日：{{ exam.exam_date ? formatDate(exam.exam_date) : '未設定' }}
      </p>
    </div>

    <div class="card-footer">
      <button class="btn btn-primary" @click="$emit('go-score', exam.exam_id)">
        スコア入力
      </button>
      <button class="btn btn-secondary" @click="$emit('go-analysis', exam.exam_id)">
        分析を見る
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Exam } from '@/stores/exam'

defineProps<{
  exam: Exam
}>()

defineEmits<{
  (e: 'go-score', examId: string): void
  (e: 'go-analysis', examId: string): void
}>()

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
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

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #f0f4f8;
  color: #2c3e50;
}

.btn-secondary:hover {
  background-color: #dce1e7;
}
</style>
