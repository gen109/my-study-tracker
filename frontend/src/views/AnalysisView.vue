<template>
  <div class="dashboard">

    <!-- ヘッダー -->
    <header class="header">
      <button class="back-btn" @click="router.push('/dashboard')">← 戻る</button>
      <h1 class="logo">分析</h1>
      <span class="user-id">👤 {{ authStore.userId }}</span>
    </header>

    <main class="main">

      <!-- 試験名 -->
      <div class="section-header">
        <h2 class="section-title">{{ currentExam?.name ?? '試験' }}</h2>
      </div>

      <!-- データなし -->
      <div v-if="scoreStore.comparisons.length === 0" class="state-message">
        <p>スコアデータがありません。</p>
        <button class="add-btn" @click="router.push(`/score/${examId}`)">
          スコアを入力する
        </button>
      </div>

      <div v-else class="charts">

        <!-- レーダーチャート -->
        <div class="chart-card">
          <h3 class="chart-title">カテゴリ別得点率（初回・前回・最新）</h3>
          <v-chart v-if="hasEnoughCategories" class="chart" :option="radarOption" autoresize />
          <p v-else class="chart-notice">レーダーチャートはカテゴリが3つ以上必要です。</p>
        </div>

        <!-- 棒グラフ -->
        <div class="chart-card">
          <h3 class="chart-title">カテゴリ別得点比較</h3>
          <v-chart class="chart" :option="barOption" autoresize />
        </div>

      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useExamStore } from '@/stores/exam'
import { useScoreStore } from '@/stores/score'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { RadarChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  RadarComponent,
} from 'echarts/components'

use([
  CanvasRenderer,
  RadarChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  RadarComponent,
])

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const examStore = useExamStore()
const scoreStore = useScoreStore()

const examId = route.params.examId as string

const currentExam = computed(() =>
  examStore.exams.find((e) => e.exam_id === examId)
)

const hasEnoughCategories = computed(() =>
  scoreStore.comparisons.length >= 3
)

onMounted(async () => {
  if (!authStore.userId) return
  await examStore.fetchExams(authStore.userId)
  await scoreStore.fetchComparisons(authStore.userId, examId)
})

// バックエンドは score/max_score の生値を返すので、ここで%に変換
const toRate = (v: number | null): number => {
  if (v === null) return 0
  // 値が1以下なら割合（0〜1）、それ以上なら生スコアと判断して変換しない
  return v <= 1 ? Math.round(v * 100) : Math.round(v)
}

const toRateNullable = (v: number | null): number | null => {
  if (v === null) return null
  return v <= 1 ? Math.round(v * 100) : Math.round(v)
}

const radarOption = computed(() => {
  const comparisons = scoreStore.comparisons
  const indicators = comparisons.map((c) => ({
    name: c.category_name,
    max: 100,
  }))

  return {
    tooltip: { trigger: 'item' },
    legend: {
      data: ['初回', '前回', '最新'],
      bottom: 0,
    },
    radar: {
      indicator: indicators,
      radius: '60%',
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            name: '初回',
            value: comparisons.map((c) => toRate(c.initial)),
            lineStyle: { color: '#95a5a6' },
            itemStyle: { color: '#95a5a6' },
            areaStyle: { color: 'rgba(149,165,166,0.1)' },
          },
          {
            name: '前回',
            value: comparisons.map((c) => toRate(c.previous)),
            lineStyle: { color: '#3498db' },
            itemStyle: { color: '#3498db' },
            areaStyle: { color: 'rgba(52,152,219,0.1)' },
          },
          {
            name: '最新',
            value: comparisons.map((c) => toRate(c.latest)),
            lineStyle: { color: '#27ae60' },
            itemStyle: { color: '#27ae60' },
            areaStyle: { color: 'rgba(39,174,96,0.15)' },
          },
        ],
      },
    ],
  }
})

const barOption = computed(() => {
  const comparisons = scoreStore.comparisons
  const categories = comparisons.map((c) => c.category_name)

  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params: { seriesName: string; value: number | null }[]) =>
        params
          .filter((p) => p.value !== null)
          .map((p) => `${p.seriesName}: ${p.value}%`)
          .join('<br/>'),
    },
    legend: {
      data: ['初回', '前回', '最新'],
      bottom: 0,
    },
    grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: { rotate: 15, fontSize: 11 },
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      axisLabel: { formatter: '{value}%' },
    },
    series: [
      {
        name: '初回',
        type: 'bar',
        data: comparisons.map((c) => toRateNullable(c.initial)),
        itemStyle: { color: '#95a5a6' },
      },
      {
        name: '前回',
        type: 'bar',
        data: comparisons.map((c) => toRateNullable(c.previous)),
        itemStyle: { color: '#3498db' },
      },
      {
        name: '最新',
        type: 'bar',
        data: comparisons.map((c) => toRateNullable(c.latest)),
        itemStyle: { color: '#27ae60' },
      },
    ],
  }
})
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

.charts {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.chart-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.chart-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 1rem;
}

.chart {
  height: 360px;
  width: 100%;
}

.chart-notice {
  text-align: center;
  color: #7f8c8d;
  padding: 2rem 0;
  font-size: 0.9rem;
}

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
</style>
