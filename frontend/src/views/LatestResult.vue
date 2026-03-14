<template>
  <div class="card">
    <h2>📊 最新開獎結果</h2>
    <div v-if="store.loading" class="loading">載入中...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>
    <div v-else-if="store.latestResult" class="latest-result">
      <div class="period">第 {{ store.latestResult.period }} 期</div>
      <div class="numbers">
        <span 
          v-for="num in formattedNumbers" 
          :key="num" 
          class="number"
        >
          {{ num }}
        </span>
      </div>
      <div class="draw-date">開獎日期：{{ store.latestResult.draw_date }}</div>
    </div>
    <div v-else class="loading">尚無開獎資料</div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useLotteryStore } from '../stores/lottery'

const store = useLotteryStore()

const formattedNumbers = computed(() => {
  if (!store.latestResult?.numbers) return []
  return store.latestResult.numbers.split(',').map(n => n.trim())
})

onMounted(() => {
  store.fetchLatestResult()
})
</script>
