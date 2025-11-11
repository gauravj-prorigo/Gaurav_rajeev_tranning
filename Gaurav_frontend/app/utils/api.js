import { useAuthStore } from '../stores/authStore.js'

export const api = $fetch.create({
  baseURL: 'http://127.0.0.1:8000/',
  async onRequest({ options }) {
    const auth = useAuthStore()
    if (auth.token) {
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${auth.token}`
      }
    }
  }
})
