<template>
  <div>
    <div class="card">
      <h2>🔮 本期預測</h2>
      <div class="prediction-box">
        <p>基於大數據分析，計算出最有可能開出的號碼</p>
        
        <div v-if="store.loading" class="loading">載入中...</div>
        <div v-else-if="predictionNumbers.length > 0" class="prediction-numbers">
          <div class="numbers">
            <span 
              v-for="num in predictionNumbers" 
              :key="num" 
              class="number"
            >
              {{ num }}
            </span>
          </div>
          <button class="btn" @click="getNewPrediction">重新預測</button>
          <button class="btn btn-secondary" @click="saveCurrentPrediction">儲存預測</button>
          <div v-if="message" :class="messageClass">{{ message }}</div>
        </div>
        <div v-else class="loading">載入預測中...</div>
      </div>
    </div>

    <div class="card">
      <h2>🔥 熱門號碼 TOP 10</h2>
      <div v-if="hotNumbers.length > 0" class="hot-numbers">
        <span 
          v-for="num in hotNumbers" 
          :key="num" 
          class="hot-number"
        >
          {{ String(num).padStart(2, '0') }}
          <span class="count">({{ frequencyData[num] }})</span>
        </span>
      </div>
      <div v-else class="loading">載入中...</div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useLotteryStore } from '../stores/lottery'

const store = useLotteryStore()
const message = ref('')
const messageClass = ref('')

const predictionNumbers = computed(() => {
  if (!store.prediction?.numbers) return []
  return store.prediction.numbers.split(',').map(n => n.trim())
})

const hotNumbers = computed(() => {
  return store.prediction?.analysis?.hot_numbers || []
})

const frequencyData = computed(() => {
  return store.prediction?.analysis?.frequency || {}
})

const getNewPrediction = () => {
  message.value = ''
  store.fetchPrediction()
}

const saveCurrentPrediction = async () => {
  if (!store.prediction?.numbers) return
  
  try {
    const period = store.latestResult ? String(Number(store.latestResult.period) + 1) : '000000'
    await store.savePrediction({
      period,
      numbers: store.prediction.numbers
    })
    message.value = '預測已儲存成功！'
    messageClass.value = 'success'
  } catch (err) {
    message.value = '儲存失敗：' + err.message
    messageClass.value = 'error'
  }
}

onMounted(() => {
  store.fetchPrediction()
  store.fetchLatestResult()
})
</script>
