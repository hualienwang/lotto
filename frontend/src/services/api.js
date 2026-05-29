import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 攔截器處理錯誤
api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// API 方法
export const lotteryApi = {
  // 取得所有開獎結果
  getResults(params = {}) {
    return api.get('/results', { params })
  },
  
  // 取得最新開獎結果
  getLatestResult() {
    return api.get('/results/latest')
  },
  
  // 新增開獎結果
  addResult(data) {
    return api.post('/results', null, { params: data })
  },
  
  // 取得預測
  getPrediction() {
    return api.get('/prediction')
  },
  
  // 儲存預測
  savePrediction(data) {
    return api.post('/prediction', null, { params: data })
  },
  
  // 取得統計數據
  getStatistics() {
    return api.get('/statistics')
  }
}

export default api
