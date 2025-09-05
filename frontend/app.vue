<template>
  <div class="container">
    <div class="header">
      <h1>Task Manager - Deployment Test</h1>
      <p>簡易的前後端與資料庫交互測試</p>
    </div>

    <!-- Status Messages -->
    <div v-if="error" class="error">
      {{ error }}
    </div>
    <div v-if="successMessage" class="success">
      {{ successMessage }}
    </div>

    <!-- API Status Check -->
    <div class="task-form">
      <h3>API 連線狀態</h3>
      <button @click="checkApiHealth" class="btn">檢查 API 連線</button>
      <div v-if="apiStatus" :class="apiStatus.success ? 'success' : 'error'" style="margin-top: 10px;">
        {{ apiStatus.message }}
      </div>
    </div>

    <!-- Add Task Form -->
    <div class="task-form">
      <h3>新增任務</h3>
      <form @submit.prevent="addTask">
        <div class="form-group">
          <label for="title">任務標題:</label>
          <input 
            id="title"
            v-model="newTask.title" 
            type="text" 
            required
            placeholder="輸入任務標題"
          />
        </div>
        <div class="form-group">
          <label for="description">任務描述:</label>
          <textarea 
            id="description"
            v-model="newTask.description" 
            placeholder="輸入任務描述（可選）"
          ></textarea>
        </div>
        <button type="submit" class="btn" :disabled="loading">
          {{ loading ? '新增中...' : '新增任務' }}
        </button>
      </form>
    </div>

    <!-- Tasks List -->
    <div class="tasks-list">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3>任務列表</h3>
        <button @click="fetchTasks" class="btn">重新整理</button>
      </div>

      <div v-if="loading && tasks.length === 0" class="loading">
        載入任務中...
      </div>

      <div v-if="!loading && tasks.length === 0" class="loading">
        目前沒有任務
      </div>

      <div 
        v-for="task in tasks" 
        :key="task.id" 
        :class="['task-item', { completed: task.completed }]"
      >
        <div class="task-content">
          <div :class="['task-title', { completed: task.completed }]">
            {{ task.title }}
          </div>
          <div v-if="task.description" class="task-description">
            {{ task.description }}
          </div>
          <div style="margin-top: 5px;">
            <span :class="['status-indicator', task.completed ? 'status-completed' : 'status-pending']">
              {{ task.completed ? '已完成' : '進行中' }}
            </span>
          </div>
        </div>
        <div class="task-actions">
          <button 
            @click="toggleTask(task)"
            :class="['btn', task.completed ? 'btn-success' : 'btn']"
          >
            {{ task.completed ? '標記未完成' : '標記完成' }}
          </button>
          <button 
            @click="deleteTask(task.id)"
            class="btn btn-danger"
          >
            刪除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()

const tasks = ref([])
const loading = ref(false)
const error = ref('')
const successMessage = ref('')
const apiStatus = ref(null)

const newTask = ref({
  title: '',
  description: ''
})

// API base URL
const apiBase = config.public.apiBase

// Check API health
const checkApiHealth = async () => {
  try {
    const response = await $fetch(`${apiBase}/health`)
    apiStatus.value = {
      success: true,
      message: `API 連線成功！時間戳: ${new Date(response.timestamp).toLocaleString()}`
    }
  } catch (err) {
    apiStatus.value = {
      success: false,
      message: `API 連線失敗: ${err.message}`
    }
  }
}

// Fetch all tasks
const fetchTasks = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const data = await $fetch(`${apiBase}/tasks`)
    tasks.value = data
  } catch (err) {
    error.value = `載入任務失敗: ${err.message}`
  } finally {
    loading.value = false
  }
}

// Add new task
const addTask = async () => {
  if (!newTask.value.title.trim()) return
  
  loading.value = true
  error.value = ''
  successMessage.value = ''
  
  try {
    await $fetch(`${apiBase}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: newTask.value.title,
        description: newTask.value.description,
        completed: false
      })
    })
    
    successMessage.value = '任務新增成功！'
    newTask.value = { title: '', description: '' }
    await fetchTasks()
  } catch (err) {
    error.value = `新增任務失敗: ${err.message}`
  } finally {
    loading.value = false
  }
}

// Toggle task completion
const toggleTask = async (task) => {
  try {
    await $fetch(`${apiBase}/tasks/${task.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: task.title,
        description: task.description,
        completed: !task.completed
      })
    })
    
    await fetchTasks()
    successMessage.value = '任務狀態更新成功！'
  } catch (err) {
    error.value = `更新任務失敗: ${err.message}`
  }
}

// Delete task
const deleteTask = async (taskId) => {
  if (!confirm('確定要刪除這個任務嗎？')) return
  
  try {
    await $fetch(`${apiBase}/tasks/${taskId}`, {
      method: 'DELETE'
    })
    
    await fetchTasks()
    successMessage.value = '任務刪除成功！'
  } catch (err) {
    error.value = `刪除任務失敗: ${err.message}`
  }
}

// Clear messages after some time
const clearMessages = () => {
  setTimeout(() => {
    error.value = ''
    successMessage.value = ''
  }, 5000)
}

watch([error, successMessage], () => {
  clearMessages()
})

// Load tasks on component mount
onMounted(() => {
  fetchTasks()
  checkApiHealth()
})
</script>
