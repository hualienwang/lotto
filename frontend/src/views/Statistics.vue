<template>
  <div>
    <div class="card">
      <h2>📉 數據分析</h2>
      
      <div v-if="store.loading" class="loading">載入中...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div v-else-if="hasStatistics">
        <div class="stats-grid">
          <div class="stat-card">
            <h3>單數</h3>
            <div class="value">{{ oddCount }}</div>
          </div>
          <div class="stat-card">
            <h3>雙數</h3>
            <div class="value">{{ evenCount }}</div>
          </div>
          <div class="stat-card">
            <h3>總開獎次數</h3>
            <div class="value">{{ totalDraws }}</div>
          </div>
        </div>
      </div>
      <div v-else class="loading">尚無資料</div>
    </div>

    <div class="card">
      <h2>📊 號碼區間分布</h2>
      
      <div v-if="hasRanges" class="stats-grid">
        <div class="range-item">
          <span class="range-label">1-10</span>
          <span class="range-value">{{ rangeData['1-10'] }}</span>
        </div>
        <div class="range-item">
          <span class="range-label">11-20</span>
          <span class="range-value">{{ rangeData['11-20'] }}</span>
        </div>
        <div class="range-item">
          <span class="range-label">21-30</span>
          <span class="range-value">{{ rangeData['21-30'] }}</span>
        </div>
        <div class="range-item">
          <span class="range-label">31-39</span>
          <span class="range-value">{{ rangeData['31-39'] }}</span>
        </div>
      </div>
      <div v-else class="loading">載入中...</div>
    </div>

    <div class="card">
      <h2>🎯 號碼出現頻率</h2>
      
      <div v-if="hasFrequency" class="frequency-chart">
        <div class="frequency-grid">
          <div 
            v-for="n in 39" 
            :key="n" 
            class="frequency-item"
          >
            <span class="freq-count">{{ frequencyData[n] }}</span>
            <div class="freq-bar-container" v-if="frequencyData[n] > 0">
              <div 
                class="freq-bar" 
                :style="{ height: getBarHeight(frequencyData[n]) + 'px' }"
              ></div>
            </div>
            <div class="freq-bar-container" v-else style="height: 60px;"></div>
            <span class="freq-number">{{ String(n).padStart(2, '0') }}</span>
          </div>
        </div>
      </div>
      <div v-else class="loading">載入中...</div>
    </div>

    <div class="card">
      <h2>🔥 號碼分類</h2>
      
      <div v-if="hasFrequency" class="number-classification">
        <div class="classification-section hot-numbers">
          <h3>熱門號碼 (4次以上)</h3>
          <div class="number-list">
            <span 
              v-for="num in hotNumbers" 
              :key="num" 
              class="number-tag hot"
            >{{ String(num).padStart(2, '0') }}</span>
            <span v-if="hotNumbers.length === 0" class="no-data">無</span>
          </div>
        </div>
        
        <div class="classification-section normal-numbers">
          <h3>普通號碼 (2-3次)</h3>
          <div class="number-list">
            <span 
              v-for="num in normalNumbers" 
              :key="num" 
              class="number-tag normal"
            >{{ String(num).padStart(2, '0') }}</span>
            <span v-if="normalNumbers.length === 0" class="no-data">無</span>
          </div>
        </div>
        
        <div class="classification-section cold-numbers">
          <h3>冷門號碼 (0-1次)</h3>
          <div class="number-list">
            <span 
              v-for="num in coldNumbers" 
              :key="num" 
              class="number-tag cold"
            >{{ String(num).padStart(2, '0') }}</span>
            <span v-if="coldNumbers.length === 0" class="no-data">無</span>
          </div>
        </div>
      </div>
      <div v-else class="loading">載入中...</div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useLotteryStore } from '../stores/lottery'

const store = useLotteryStore()

const hasStatistics = computed(() => {
  return store.statistics && store.statistics.odd_even
})

const oddCount = computed(() => {
  return store.statistics?.odd_even?.odd || 0
})

const evenCount = computed(() => {
  return store.statistics?.odd_even?.even || 0
})

const totalDraws = computed(() => {
  return store.statistics?.total_draws || 0
})

const hasRanges = computed(() => {
  return store.statistics && store.statistics.ranges
})

const rangeData = computed(() => {
  return store.statistics?.ranges || {}
})

// 只取最近30期的資料
const recentResults = computed(() => {
  const results = store.results || []
  // 假設結果已經按日期排序，最新的在陣列前面
  return results.slice(0, 30)
})

// 計算每個號碼的出現頻率 (僅最近30期)
const frequency = computed(() => {
  const freq = {}
  for (let i = 1; i <= 39; i++) {
    freq[i] = 0
  }
  
  recentResults.value.forEach(row => {
    if (row.numbers) {
      const numbers = row.numbers.split(',').map(n => parseInt(n.trim()))
      numbers.forEach(num => {
        if (num >= 1 && num <= 39) {
          freq[num]++
        }
      })
    }
  })
  
  return freq
})

const hasFrequency = computed(() => {
  return recentResults.value.length > 0
})

const frequencyData = computed(() => {
  return frequency.value
})

// 取得柱狀圖高度
const getBarHeight = (count) => {
  const maxFreq = Math.max(...Object.values(frequency.value))
  if (maxFreq > 0) {
    return Math.round((count / maxFreq) * 60)
  }
  return 0
}

// 熱門號碼 (4次以上)
const hotNumbers = computed(() => {
  const nums = []
  for (let i = 1; i <= 39; i++) {
    if (frequency.value[i] >= 4) {
      nums.push(i)
    }
  }
  return nums.sort((a, b) => frequency.value[b] - frequency.value[a])
})

// 普通號碼 (2-3次)
const normalNumbers = computed(() => {
  const nums = []
  for (let i = 1; i <= 39; i++) {
    if (frequency.value[i] >= 2 && frequency.value[i] <= 3) {
      nums.push(i)
    }
  }
  return nums.sort((a, b) => frequency.value[b] - frequency.value[a])
})

// 冷門號碼 (0-1次)
const coldNumbers = computed(() => {
  const nums = []
  for (let i = 1; i <= 39; i++) {
    if (frequency.value[i] <= 1) {
      nums.push(i)
    }
  }
  return nums.sort((a, b) => frequency.value[a] - frequency.value[b])
})

onMounted(() => {
  store.fetchResults()
  store.fetchStatistics()
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
}

.stat-card h3 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #333;
}

.stat-card .value {
  font-size: 24px;
  font-weight: bold;
  color: #008000;
}

.range-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 8px;
}

.range-label {
  font-weight: bold;
  color: #333;
}

.range-value {
  font-size: 18px;
  font-weight: bold;
  color: #008000;
}

.frequency-chart {
  overflow-x: auto;
}

.frequency-grid {
  display: flex;
  gap: 4px;
  min-width: 600px;
}

.frequency-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 28px;
}

.freq-bar-container {
  height: 60px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.freq-bar {
  width: 13px;
  background-color: #4CAF50;
  min-height: 2px;
}

.freq-number {
  font-size: 10px;
  color: #FFD700;
  margin-top: 4px;
}

.freq-count {
  font-size: 10px;
  color: #FFD700;
  margin-bottom: 2px;
}

.number-classification {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.classification-section {
  padding: 12px;
  border-radius: 8px;
}

.classification-section h3 {
  margin: 0 0 8px 0;
  font-size: 14px;
}

.hot-numbers {
  background: #ffebee;
}

.hot-numbers h3 {
  color: #c62828;
}

.normal-numbers {
  background: #fff3e0;
}

.normal-numbers h3 {
  color: #e65100;
}

.cold-numbers {
  background: #e3f2fd;
}

.cold-numbers h3 {
  color: #1565c0;
}

.number-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.number-tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.number-tag.hot {
  background-color: #ef5350;
  color: white;
}

.number-tag.normal {
  background-color: #ff9800;
  color: white;
}

.number-tag.cold {
  background-color: #42a5f5;
  color: white;
}

.no-data {
  color: #999;
  font-style: italic;
}
</style>
