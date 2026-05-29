<template>
  <div class="card">
    <h2>📈 歷次開獎資訊</h2>
    
    <div class="history-filter">
      <div class="date-filter">
        <label>開始日期：</label>
        <input type="date" v-model="startDate" @change="filterResults">
      </div>
      <div class="date-filter">
        <label>結束日期：</label>
        <input type="date" v-model="endDate" @change="filterResults">
      </div>
      <button class="btn" @click="resetFilter">重設篩選</button>
    </div>

    <div v-if="store.loading" class="loading">載入中...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>
    <div v-else-if="store.results.length === 0" class="error">無資料</div>
    <div v-else>
      <div class="history-info">
        今彩539開獎獎號總共查詢<span class="highlight">{{ store.results.length }}</span>期，從<span class="highlight">{{ store.results[0].period }}</span>({{ formatTaiwanDate(store.results[0].draw_date) }})期～<span class="highlight">{{ store.results[store.results.length - 1].period }}</span>({{ formatTaiwanDate(store.results[store.results.length - 1].draw_date) }})期
      </div>
      <div class="history-table-container">
        <table class="history-table">
          <thead>
            <tr>
              <th style="color: white;">日期</th>
              <th v-for="n in 39" :key="n" style="color: black;">{{ String(n).padStart(2, '0') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in store.results" :key="result.id">
              <td><div align="center" style="color: white;">{{ formatTaiwanDate(result.draw_date) }}</div></td>
              <td 
                v-for="n in 39" 
                :key="n"
                :class="{ 'hit-number': isHitNumber(result.numbers, n) }"
              >
                {{ isHitNumber(result.numbers, n) ? n : '' }}
              </td>
            </tr>
            <!-- 標注號碼行 -->
            <tr bgcolor="#CCCCCC">
              <td bgcolor="#efefef"><div align="center" style="color: black;">標注號碼</div></td>
              <td 
                v-for="n in 39" 
                :key="n"
                class="marker-cell"
                :style="{ color: 'black', textAlign: 'center', backgroundColor: isMarked(n) ? '#FF0000' : '#CCCCCC', cursor: 'pointer' }"
                @click="toggleMarker(n)"
              >
                <p>{{ String(n).padStart(2, '0') }}</p>
              </td>
            </tr>
            <!-- 出現次數行 -->
            <tr bgcolor="#ffff00">
              <td><div align="center"><font color="black"><b>出現次數</b></font></div></td>
              <td 
                v-for="n in 39" 
                :key="n"
                bgcolor="#ffffff" 
                align="center" 
                valign="bottom"
              >
                <div style="display: flex; flex-direction: column; align-items: center;">
                  <span style="color:black;">{{ getFrequency(n) }}</span>
                  <div class="freq-bar" :style="{ width: '13px', height: getBarHeight(getFrequency(n)) + 'px' }"></div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useLotteryStore } from '../stores/lottery'

const store = useLotteryStore()
const startDate = ref('')
const endDate = ref('')
const markedNumbers = ref(new Set())

// 格式化日期為民國年
const formatTaiwanDate = (dateStr) => {
  if (!dateStr) return ''
  const parts = dateStr.split('-')
  const year = parseInt(parts[0]) - 1911
  const month = parts[1]?.padStart(2, '0') || ''
  const day = parts[2]?.padStart(2, '0') || ''
  return `${year}/${month}/${day}`
}

// 檢查號碼是否開出
const isHitNumber = (numbersStr, num) => {
  if (!numbersStr) return false
  const numbers = numbersStr.split(',').map(n => parseInt(n.trim()))
  return numbers.includes(num)
}

// 計算每個號碼的出現次數
const frequency = computed(() => {
  const freq = {}
  for (let i = 1; i <= 39; i++) {
    freq[i] = 0
  }
  store.results.forEach(result => {
    const numbers = result.numbers.split(',').map(n => parseInt(n.trim()))
    numbers.forEach(num => {
      if (freq[num] !== undefined) {
        freq[num]++
      }
    })
  })
  return freq
})

// 取得號碼出現次數
const getFrequency = (num) => {
  return frequency.value[num] || 0
}

// 取得柱狀圖高度
const getBarHeight = (count) => {
  const maxFreq = Math.max(...Object.values(frequency.value))
  if (maxFreq > 0) {
    return Math.round((count / maxFreq) * 40)
  }
  return 0
}

// 切換標記
const toggleMarker = (num) => {
  if (markedNumbers.value.has(num)) {
    markedNumbers.value.delete(num)
  } else {
    markedNumbers.value.add(num)
  }
  markedNumbers.value = new Set(markedNumbers.value)
}

// 檢查號碼是否被標記
const isMarked = (num) => {
  return markedNumbers.value.has(num)
}

const filterResults = () => {
  store.fetchResults({
    start_date: startDate.value || undefined,
    end_date: endDate.value || undefined
  })
}

const resetFilter = () => {
  startDate.value = ''
  endDate.value = ''
  store.fetchResults()
}

onMounted(async () => {
  await store.fetchResults()
  
  // 預設顯示最近30期
  if (store.results && store.results.length > 0) {
    const sortedResults = [...store.results].sort((a, b) => 
      new Date(a.draw_date) - new Date(b.draw_date)
    )
    const last30 = sortedResults.slice(-30)
    if (last30.length > 0) {
      startDate.value = last30[0].draw_date
      endDate.value = last30[last30.length - 1].draw_date
      // 設定日期後重新過濾結果
      filterResults()
    }
  }
})
</script>

<style scoped>
.history-info {
  margin-bottom: 16px;
  font-size: 14px;
}

.highlight {
  color: #008000;
  font-weight: bold;
}

.history-table-container {
  overflow-x: auto;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.history-table th,
.history-table td {
  border: 1px solid #ddd;
  padding: 4px;
  text-align: center;
  min-width: 24px;
}

.history-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.history-table .hit-number {
  background-color: #ff6b6b;
  color: white;
  font-weight: bold;
}

.history-table .marker-cell {
  cursor: pointer;
  user-select: none;
}

.history-table .marker-cell:hover {
  opacity: 0.8;
}

.freq-bar {
  background-color: #4CAF50;
  margin-top: 2px;
}

.lottery-table {
  width: 100%;
  border-collapse: collapse;
}

.lottery-table th,
.lottery-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.lottery-table th {
  background-color: #f5f5f5;
}

.period-col {
  font-weight: bold;
}

.numbers-col .number {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  background-color: #ff6b6b;
  color: white;
  border-radius: 50%;
  margin: 2px;
  font-weight: bold;
}
</style>
