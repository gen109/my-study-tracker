<template>
  <div class="score-row" :style="{ paddingLeft: `${category.depth * 20 + 16}px` }">
    <span class="col-name">
      <span v-if="category.depth > 0" class="depth-icon">└</span>
      {{ category.name }}
    </span>
    <span class="col-score">
      <input
        type="number"
        class="score-input"
        placeholder="満点"
        min="0"
        :value="score.max_score"
        @input="updateScore('max_score', ($event.target as HTMLInputElement).value)"
      />
    </span>
    <span class="col-score">
      <input
        type="number"
        class="score-input"
        placeholder="得点"
        min="0"
        :value="score.score"
        @input="updateScore('score', ($event.target as HTMLInputElement).value)"
      />
    </span>
    <span class="col-compare">
      {{ comparison?.initial !== null && comparison?.initial !== undefined ? comparison.initial : '—' }}
    </span>
    <span class="col-compare">
      {{ comparison?.previous !== null && comparison?.previous !== undefined ? comparison.previous : '—' }}
    </span>
    <span class="col-compare" :class="latestClass">
      {{ comparison?.latest !== null && comparison?.latest !== undefined ? comparison.latest : '—' }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { ScoreComparison } from '@/stores/score'

const props = defineProps<{
  category: { category_id: string; name: string; depth: number }
  comparison: ScoreComparison | null
  score: { score: string; max_score: string }
}>()

const emit = defineEmits<{
  (e: 'update:score', value: { score: string; max_score: string }): void
}>()

function updateScore(field: 'score' | 'max_score', value: string) {
  emit('update:score', { ...props.score, [field]: value })
}

// 最新スコアの色（前回より上がれば青、下がれば赤）
const latestClass = computed(() => {
  const { latest, previous } = props.comparison ?? {}
  if (latest === null || latest === undefined) return ''
  if (previous === null || previous === undefined) return ''
  if (latest > previous) return 'up'
  if (latest < previous) return 'down'
  return ''
})
</script>

<style scoped>
.score-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
  align-items: center;
  padding-top: 0.65rem;
  padding-bottom: 0.65rem;
  padding-right: 1rem;
  border-bottom: 1px solid #f0f4f8;
  font-size: 0.9rem;
  color: #2c3e50;
}

.score-row:last-child {
  border-bottom: none;
}

.col-name {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.depth-icon {
  color: #bdc3c7;
  font-size: 0.8rem;
}

.col-score {
  text-align: center;
}

.col-compare {
  text-align: center;
  color: #7f8c8d;
}

.score-input {
  width: 70px;
  padding: 0.3rem 0.5rem;
  border: 1px solid #dce1e7;
  border-radius: 4px;
  font-size: 0.9rem;
  text-align: center;
}

.score-input:focus {
  outline: none;
  border-color: #3498db;
}

.up {
  color: #2980b9;
  font-weight: 600;
}

.down {
  color: #e74c3c;
  font-weight: 600;
}
</style>
