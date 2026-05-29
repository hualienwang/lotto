<template>
  <div class="app">
    <header>
      <h1>🎰 台灣彩券539開獎系統</h1>
      <p>Taiwan Lottery 539 Results & Prediction</p>
    </header>

    <nav class="tabs">
      <router-link to="/" class="tab-btn" :class="{ active: $route.path === '/' }">最新開獎</router-link>
      <router-link to="/history" class="tab-btn" :class="{ active: $route.path === '/history' }">歷次開獎</router-link>
      <router-link to="/prediction" class="tab-btn" :class="{ active: $route.path === '/prediction' }">本期預測</router-link>
      <router-link to="/statistics" class="tab-btn" :class="{ active: $route.path === '/statistics' }">數據分析</router-link>
      <router-link to="/admin" class="tab-btn" :class="{ active: $route.path === '/admin' }">管理系統</router-link>
    </nav>

    <main class="container">
      <router-view />
    </main>

    <footer>
      <p>© 2024 台灣彩券539開獎系統</p>
    </footer>
  </div>
</template>

<script setup>
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  width: 100%;
}

footer {
  text-align: center;
  padding: 20px;
  margin-top: 30px;
  color: rgba(255,255,255,0.5);
}
</style>
