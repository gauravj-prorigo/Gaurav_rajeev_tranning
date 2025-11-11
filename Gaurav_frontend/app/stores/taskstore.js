import { defineStore } from 'pinia'

export const useTaskStore = defineStore('tasks', {
  state: () => ({
    todos: [],
    newTodo: ''
  }),

  getters: {
    selectedCount: (state) => state.todos.filter(t => t.done).length
  },

  actions: {
    add() {
      if (this.newTodo.trim() !== '') {
        this.todos.push({ text: this.newTodo, done: false })
        this.newTodo = ''
        this.saveTodos()
      }
    },
    deleteTodo(index) {
      const ok = window.confirm('Are you sure you want to delete this task?')
      if (ok) {
        this.todos.splice(index, 1)
        this.saveTodos()
        window.alert('Task Deleted')
      }
    },
    deleteSelected() {
      const count = this.selectedCount
      if (count === 0) return
      const ok = window.confirm(`Delete ${count} selected task(s)?`)
      if (!ok) return
      this.todos = this.todos.filter(t => !t.done)
      this.saveTodos()
      window.alert(`${count} task(s) deleted`)
    },
    saveTodos() {
      localStorage.setItem("todos", JSON.stringify(this.todos));
    },

    loadTodos() {
    const saved = localStorage.getItem("todos");
    if (saved) {
      this.todos = JSON.parse(saved);
    }
  }
  }
})

