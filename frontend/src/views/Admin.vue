<template>
  <div class="card">
    <h2>⚙️ 管理系統</h2>
    
    <form @submit.prevent="submitResult">
      <div class="form-group">
        <label for="period">期別：</label>
        <input 
          type="text" 
          id="period" 
          v-model="form.period" 
          placeholder="例如：113015"
          required
        >
      </div>
      
      <div class="form-group">
        <label for="drawDate">開獎日期：</label>
        <input 
          type="date" 
          id="drawDate" 
          v-model="form.draw_date" 
          required
        >
      </div>
      
      <div class="form-group">
        <label for="numbers">開獎號碼（5個號碼，用逗號分開）：</label>
        <input 
          type="text" 
          id="numbers" 
          v-model="form.numbers" 
          placeholder="例如：01, 05, 12, 23, 39"
          required
        >
      </div>
      
      <button type="submit" class="btn" :disabled="store.loading">
        {{ store.loading ? '儲存中...' : '儲存' }}
      </button>
    </form>
    
    <div v-if="message" :class="messageClass" style="margin-top: 15px;">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useLotteryStore } from '../stores/lottery'

const store = useLotteryStore()
const message = ref('')
const messageClass = ref('')

const form = reactive({
  period: '',
  draw_date: '',
  numbers: ''
})

const submitResult = async () => {
  message.value = ''
  messageClass.value = ''
  
  try {
    // 格式化號碼
    const formattedNumbers = form.numbers
      .split(',')
      .map(n => n.trim())
      .map(n => n.padStart(2, '0'))
      .join(', ')
    
    const res = await store.addResult({
      period: form.period,
      draw_date: form.draw_date,
      numbers: formattedNumbers
    })
    
    if (res.success) {
      message.value = '開獎結果已成功儲存！'
      messageClass.value = 'success'
      // 清空表單
      form.period = ''
      form.draw_date = ''
      form.numbers = ''
    }
  } catch (err) {
    message.value = '儲存失敗：' + (err.response?.data?.message || err.message)
    messageClass.value = 'error'
  }
}
</script>
