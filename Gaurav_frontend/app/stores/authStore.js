// stores/useAuth.js
import { defineStore } from '#imports'
export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role ?? null,
  },

  actions: {
    initFromStorage() {
      try {
        const data = localStorage.getItem('auth')
        console.log(data, "from the initFromStorage")
        if (data) {
          const { token, user } = JSON.parse(data)
          this.token = token
          this.user = user
        }
      } catch (err) {
        console.error('Failed to read auth from storage', err)
      }
    },

    persist() {
      try {
        localStorage.setItem('auth', JSON.stringify({ token: this.token, user: this.user }))
      } catch (err) {
        console.error('Failed to persist auth to storage', err)
      }
    },

    clearPersist() {
      try {
        localStorage.removeItem('auth')
      } catch (err) { }
    },

    async login(credentials) {
      try {
        const url = 'http://127.0.0.1:8000/login/'

        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials)
        })

        const data = await res.json().catch(() => null)

        if (!res.ok) {
          const msg = data?.detail || data?.message || `Login failed (${res.status})`
          throw new Error(msg)
        }
      

        // ✅ extract nested token
        const token = data?.tokens?.access ?? data?.token ?? data?.access ?? null
        const user = data?.user ?? null
        console.log("user is  ->>", user)

        if (!token) {
          console.warn('Login response missing token:', data)
          throw new Error('Login response missing access token')
        }

        this.token = token
        this.user = user
        this.persist()

        return data
      } catch (err) {
        throw err
      }
    }
    ,

    async register(payload) {
      const url = 'http://127.0.0.1:8000/register/'

      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })

      if (!res.ok) {
        console.log("Something is wrong")
      }

      // success → parse data
      const data = await res.json()
      return data
    },

    logout() {
      this.token = null
      this.user = null
      this.clearPersist()
    },

    setTokenAndUser(token, user) {
      this.token = token
      this.user = user
      this.persist()
    },

    hasRole(role) {
      if (!this.user) return false
      // role can be string or array
      if (Array.isArray(role)) return role.includes(this.user.role)
      return this.user.role === role
    }
  }
})
