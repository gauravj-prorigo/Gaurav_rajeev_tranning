// stores/blogs.js
import { defineStore } from 'pinia'
import { useToast } from 'vue-toastification'

export const useBlogStore = defineStore('blog', {
  state: () => ({
    blogs: [],
    editingBlog: null
  }),
  actions: {
    async fetchBlogs(apiBase) {
      const toast = useToast()
      try {
        this.blogs = await $fetch(`${apiBase}/blogs/`)
      } catch (err) {
        console.error(err)
        toast.error('Failed to load blogs')
      }
    },
    async addBlog(apiBase, title, content) {
      const toast = useToast()
      try {
        const created = await $fetch(`${apiBase}/blogs/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, content })
        })
        this.blogs.unshift(created)
        toast.success('Blog created')
      } catch (err) {
        console.error(err)
        toast.error('Failed to create blog')
      }
    },
    startEditing(blog) { this.editingBlog = { ...blog } },
    cancelEditing() { this.editingBlog = null },
    async updateBlog(apiBase, id, title, content) {
      const toast = useToast()
      try {
        const updated = await $fetch(`${apiBase}/blogs/${id}/`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, content })
        })
        const idx = this.blogs.findIndex(b => b.id === id)
        if (idx !== -1) this.blogs.splice(idx, 1, updated)
        this.editingBlog = null
        toast.success('Blog updated')
      } catch (err) {
        console.error(err)
        toast.error('Failed to update blog')
      }
    },
    async deleteBlog(apiBase, id) {
      const toast = useToast()
      try {
        await $fetch(`${apiBase}/blogs/${id}/`, { method: 'DELETE' })
        this.blogs = this.blogs.filter(b => b.id !== id)
        toast.info('Blog deleted')
      } catch (err) {
        console.error(err)
        toast.error('Failed to delete blog')
      }
    }
  },
  getters: {
    allBlogs: (s) => s.blogs,
    currentEdit: (s) => s.editingBlog
  }
})
