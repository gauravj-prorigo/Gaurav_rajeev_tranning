<template>
  <!-- :key forces remount when route changes (helps SPA redirect -> fresh layout) -->
  <div class="auth-page" :key="route.fullPath">
    <div class="auth-card" role="region" aria-labelledby="register-title">
      <h1 id="register-title">Register</h1>

      <p v-if="infoMessage" class="info">{{ infoMessage }}</p>

      <form @submit.prevent="onSubmit" class="form" novalidate>
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            autocomplete="username"
            required
            :class="{ invalid: fieldErrors.username }"
            @blur="validateField('username')"
            placeholder="Choose a username"
          />
          <p v-if="fieldErrors.username" class="field-error">{{ fieldErrors.username }}</p>
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            type="email"
            v-model="form.email"
            autocomplete="email"
            required
            :class="{ invalid: fieldErrors.email }"
            @blur="validateField('email')"
            placeholder="you@example.com"
          />
          <p v-if="fieldErrors.email" class="field-error">{{ fieldErrors.email }}</p>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            type="password"
            v-model="form.password"
            autocomplete="new-password"
            required
            minlength="6"
            :class="{ invalid: fieldErrors.password }"
            @blur="validateField('password')"
            placeholder="At least 6 characters"
          />
          <p v-if="fieldErrors.password" class="field-error">{{ fieldErrors.password }}</p>
        </div>

        <div class="form-group">
          <label for="role">Role</label>
          <select
            id="role"
            v-model="form.role"
            required
            :class="{ invalid: fieldErrors.role }"
            @blur="validateField('role')"
          >
            <option disabled value="">Select role</option>
            <option value="user">User</option>
            <option value="employee">Employee</option>
            <option value="admin">Admin</option>
          </select>
          <p v-if="fieldErrors.role" class="field-error">{{ fieldErrors.role }}</p>
        </div>

        <button type="submit" :disabled="loading" class="btn-primary" aria-busy="loading">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>

        <p class="server-error" v-if="error">{{ error }}</p>
      </form>

      <p class="switch-text">
        Already have an account?
        <NuxtLink to="/">Login</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter, useRoute } from '#imports'
import { useAuthStore } from '#imports'

const auth = useAuthStore()
// restore store on client (safe)
if (process.client && typeof auth.initFromStorage === 'function') {
  auth.initFromStorage()
}

const router = useRouter()
const route = useRoute()

const form = reactive({
  username: '',
  email: '',
  password: '',
  role: ''
})

const loading = ref(false)
const error = ref(null)

const fieldErrors = reactive({
  username: null,
  email: null,
  password: null,
  role: null
})

// Optional info message (if you pass reason/next to register route)
const reason = computed(() => route.query.reason)
const infoMessage = computed(() => {
  if (reason.value === 'auth_required') return 'Please register or login to continue.'
  return ''
})

function validateField(field) {
  fieldErrors[field] = null

  if (field === 'username') {
    if (!form.username || form.username.trim().length < 3) {
      fieldErrors.username = 'Enter username (min 3 chars).'
    }
  }

  if (field === 'email') {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!form.email || !re.test(form.email)) {
      fieldErrors.email = 'Enter a valid email address.'
    }
  }

  if (field === 'password') {
    if (!form.password || form.password.length < 6) {
      fieldErrors.password = 'Password must be at least 6 characters.'
    }
  }

  if (field === 'role') {
    if (!form.role) {
      fieldErrors.role = 'Please select a role.'
    }
  }
}

async function onSubmit() {
  // run validations
  validateField('username')
  validateField('email')
  validateField('password')
  validateField('role')

  if (fieldErrors.username || fieldErrors.email || fieldErrors.password || fieldErrors.role) {
    error.value = 'Please fix the highlighted fields.'
    return
  }

  loading.value = true
  error.value = null

  try {
    const res = await auth.register({
      username: form.username,
      email: form.email,
      password: form.password,
      role: form.role
    })

    // if backend returns tokens => auto-login possible, else go to login
    // we check common keys (tokens.access or token)
    const token = res?.tokens?.access ?? res?.token ?? res?.access ?? null
    if (token) {
      // backend returned token; persist and redirect to intended page
      auth.setTokenAndUser(token, res.user ?? { username: form.username, role: form.role })
      const next = route.query.next ? decodeURIComponent(String(route.query.next)) : '/Homepage'
      router.push(next)
    } else {
      // no token: send user to login page
      router.push('/')
    }
  } catch (err) {
    // show error message
    error.value = err?.message || err?.data?.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Page wrapper */
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f6f8fb;
  padding: 24px;
  box-sizing: border-box;
}

/* Card */
.auth-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  border-radius: 8px;
  padding: 22px;
  box-sizing: border-box;
  border: 1px solid #e6eef8;
  box-shadow: 0 6px 18px rgba(20, 40, 80, 0.04);
}

/* Title */
h1 {
  margin: 0 0 10px;
  font-size: 1.25rem;
  color: #102a43;
  text-align: center;
}

/* Info message shown when redirected */
.info {
  margin: 0 0 12px;
  text-align: center;
  color: #276749; /* greenish */
  background: #ecfdf5;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.95rem;
}

/* Form */
.form { display: grid; gap: 12px; }

/* Form group */
.form-group { display: flex; flex-direction: column; gap: 6px; }

label {
  font-weight: 600;
  font-size: 0.9rem;
  color: #243b53;
}

/* Inputs */
input, select {
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid #dbe9fb;
  background: #fbfdff;
  font-size: 0.95rem;
  outline: none;
  transition: border-color .12s ease, box-shadow .12s ease;
}

input:focus, select:focus {
  border-color: #2b6cb0;
  box-shadow: 0 6px 14px rgba(43,108,176,0.06);
}

/* Invalid input */
.invalid {
  border-color: #e53e3e !important;
}

/* Field error */
.field-error {
  color: #e53e3e;
  font-size: 0.85rem;
  margin-top: 4px;
}

/* Primary button */
.btn-primary {
  margin-top: 4px;
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: none;
  font-weight: 700;
  background: linear-gradient(90deg, #2b6cb0, #1f4ea6);
  color: white;
  cursor: pointer;
  transition: transform .12s ease, opacity .12s ease;
}

.btn-primary[disabled] {
  opacity: 0.65;
  cursor: not-allowed;
  transform: none;
}

.server-error {
  margin-top: 8px;
  color: #972a2a;
  text-align: center;
  font-weight: 600;
}

/* Footer text */
.switch-text {
  margin-top: 12px;
  text-align: center;
  color: #334e68;
  font-size: 0.95rem;
}

.switch-text a {
  color: #1f6feb;
  text-decoration: none;
  font-weight: 700;
}

/* Small screens */
@media (max-width: 420px) {
  .auth-card { padding: 16px; border-radius: 6px; }
  input, select { padding: 9px 10px; }
  .btn-primary { padding: 10px; border-radius: 6px; }
}
</style>
