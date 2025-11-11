<template>
  <div class="app">
    <NuxtLink to="/Homepage" class="return-btn">← Return Home</NuxtLink>
    <h1>Simple Todo App (Nuxt)</h1>

    <input v-model="taskStore.newTodo" placeholder="Enter a task..." />
    <button @click="taskStore.add">Add</button>

    <div class="actions" style="margin-top:12px;">
      <button
        class="delete-selected"
        @click="taskStore.deleteSelected"
        :disabled="taskStore.selectedCount === 0"
        title="Delete all checked tasks"
      >
        Delete Selected ({{ taskStore.selectedCount }})
      </button>
    </div>

    <ul style="margin-top:14px;">
      <li
        v-for="(todo, index) in taskStore.todos"
        :key="index"
        :class="{ done: todo.done }"
      >
        <div class="todo-item">
          <input type="checkbox" v-model="todo.done" @change="taskStore.saveTodos" />
          <span>{{ todo.text }}</span>
        </div>
        <button @click="taskStore.deleteTodo(index)" class="delete-btn"><DeleteIcon/></button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import DeleteIcon from 'vue-material-design-icons/Delete.vue';
import { useTaskStore } from '#imports'
import { onMounted } from 'vue'

const taskStore = useTaskStore()

onMounted(() => {
  taskStore.loadTodos()
})

definePageMeta({
    layout: 'authenticated'
})
</script>

<style scoped>
.app {
  max-width: 420px;
  margin: 40px auto;
  padding: 18px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  text-align: center;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial;
}
input {
  padding: 8px;
  width: 70%;
  margin-right: 8px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
button {
  padding: 8px 12px;
  border: none;
  background-color: #3498db;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.actions .delete-selected {
  background: #e74c3c;
  margin-left: 6px;
}
ul {
  list-style: none;
  padding: 0;
  margin-top: 12px;
}
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fbff;
  padding: 10px 12px;
  border-radius: 8px;
  margin-top: 8px;
}
.todo-item {
  display: flex;
  gap: 10px;
  align-items: center;
}
.delete-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 8px;
  border-radius: 6px;
  cursor: pointer;
}
.done span {
  text-decoration: line-through;
  color: gray;
}

.return-btn {
  display: inline-block;
  margin-bottom: 20px;
  padding: 8px 15px;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.return-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}
</style>

