import { defineStore } from 'pinia'
import { lotteryApi } from '../services/api'

export const useLotteryStore = defineStore('lottery', {
  state: () => ({
    latestResult: null,
    results: [],
    prediction: null,
    statistics: null,
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchLatestResult() {
      this.loading = true
      this.error = null
      try {
        const res = await lotteryApi.getLatestResult()
        if (res.success) {
          this.latestResult = res.data
        }
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    
    async fetchResults(params = {}) {
      this.loading = true
      this.error = null
      try {
        const res = await lotteryApi.getResults(params)
        if (res.success) {
          this.results = res.data.results
        }
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    
    async fetchPrediction() {
      this.loading = true
      this.error = null
      try {
        const res = await lotteryApi.getPrediction()
        if (res.success) {
          this.prediction = res.data
        }
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    
    async fetchStatistics() {
      this.loading = true
      this.error = null
      try {
        const res = await lotteryApi.getStatistics()
        if (res.success) {
          this.statistics = res.data
        }
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    
    async addResult(data) {
      this.loading = true
      this.error = null
      try {
        const res = await lotteryApi.addResult(data)
        if (res.success) {
          await this.fetchLatestResult()
          await this.fetchResults()
        }
        return res
      } catch (err) {
        this.error = err.message
        throw err
      } finally {
        this.loading = false
      }
    },
    
    async savePrediction(data) {
      this.loading = true
      this.error = null
      try {
        const res = await lotteryApi.savePrediction(data)
        return res
      } catch (err) {
        this.error = err.message
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})
