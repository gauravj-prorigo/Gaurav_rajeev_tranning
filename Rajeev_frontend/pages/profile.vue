<template>
  <aside class="profile-card" role="dialog" aria-label="User profile" v-show="visible">
    <header class="profile-header">
      <div class="header-content">
        <h2 class="profile-title">{{ title }}</h2>
      </div>
      <button class="close-btn" @click="close" aria-label="Close profile">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </header>

    <div class="profile-avatar-section">
      <div class="profile-avatar" aria-hidden="true">{{ initials }}</div>
    </div>

    <div class="profile-details">
      <div class="detail-item">
        <div class="detail-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div class="detail-content">
          <span class="detail-label">Username</span>
          <span class="detail-value">{{ user?.username ?? '-' }}</span>
        </div>
      </div>

      <div class="detail-item">
        <div class="detail-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        <div class="detail-content">
          <span class="detail-label">Email</span>
          <span class="detail-value">{{ user?.email ? user.email : '-' }}</span>
        </div>
      </div>

      <div class="detail-item">
        <div class="detail-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        <div class="detail-content">
          <span class="detail-label">Role</span>
          <span :class="['role-badge', roleClass]">{{ roleLabel }}</span>
        </div>
      </div>
    </div>

    <footer class="profile-actions">
      <button class="btn btn-edit" @click="$emit('edit', user)" :disabled="!user">
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
        Edit Profile
      </button>
      <button class="btn btn-logout" @click="onLogout" :disabled="!user">
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        Logout
      </button>
    </footer>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '#imports'
import { useRouter, useRoute } from 'vue-router'

const props = defineProps({
  visible: { type: Boolean, default: true },
  title: { type: String, default: 'Profile' } // can be "Admin Profile" etc.
})
const emit = defineEmits(['close', 'edit'])

// auth store
const auth = useAuthStore()
const user = computed(() => auth.user ?? null)

// initials for avatar
const initials = computed(() => {
  const name = user.value?.username || user.value?.first_name || ''
  if (!name) return '?'
  const parts = name.trim().split(/\s+/)
  if (parts.length === 1) return parts[0].slice(0,2).toUpperCase()
  return (parts[0][0] + parts[1][0]).toUpperCase()
})

// display role label and class
const roleLabel = computed(() => (user.value?.role ?? (auth.user?.is_superuser ? 'admin' : 'user')).toString())
const roleClass = computed(() => {
  const r = roleLabel.value.toLowerCase()
  return r === 'admin' ? 'role-admin' : (r === 'employee' ? 'role-employee' : 'role-user')
})

// router for logout redirect
const router = useRouter()
const route = useRoute()

function close() {
  emit('close')
}

function onLogout() {
  // logout in store
  auth.logout()

  // redirect to login page and include ?next=currentPath so user can come back after login
  const next = encodeURIComponent(route.fullPath || '/')
  router.push({ path: '/login', query: { next } })
}
</script>

<style scoped>
.profile-card {
  width: 380px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.8);
  overflow: hidden;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  position: relative;
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
}

/* Header */
.profile-header {
  padding: 2rem 2rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.profile-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.profile-card:hover .profile-header::before {
  transform: translateX(100%);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;
}

.profile-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  color: white;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.close-btn svg {
  width: 20px;
  height: 20px;
}

/* Avatar Section */
.profile-avatar-section {
  display: flex;
  justify-content: center;
  padding: 1rem 2rem 0;
  position: relative;
  z-index: 1;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.75rem;
  border: 3px solid rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  color: white;
}

.profile-card:hover .profile-avatar {
  transform: scale(1.1) rotate(5deg);
  background: rgba(255, 255, 255, 0.35);
}

/* Details */
.profile-details {
  padding: 1.5rem 2rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.25rem 0;
  border-bottom: 1px solid #f1f5f9;
  transition: all 0.3s ease;
  border-radius: 12px;
  margin: 0 -0.75rem;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  position: relative;
  overflow: hidden;
}

.detail-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.detail-item:hover {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  transform: translateX(8px);
  border-bottom-color: transparent;
}

.detail-item:hover::before {
  transform: scaleY(1);
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.detail-item:hover .detail-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: scale(1.1) rotate(-5deg);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.detail-item:hover .detail-icon svg {
  color: white;
  transform: scale(1.1);
}

.detail-icon svg {
  width: 20px;
  height: 20px;
  color: #64748b;
  transition: all 0.3s ease;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.detail-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.75px;
  transition: color 0.3s ease;
}

.detail-item:hover .detail-label {
  color: #667eea;
}

.detail-value {
  font-weight: 700;
  color: #1e293b;
  font-size: 1rem;
  letter-spacing: -0.025em;
  transition: color 0.3s ease;
}

.detail-item:hover .detail-value {
  color: #334155;
}

/* Role Badge */
.role-badge {
  padding: 0.6rem 1.25rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.75px;
  display: inline-block;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.role-admin {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border: 1px solid rgba(253, 230, 138, 0.8);
}

.role-employee {
  background: linear-gradient(135deg, #cffafe 0%, #a5f3fc 100%);
  color: #035e7b;
  border: 1px solid rgba(165, 243, 252, 0.8);
}

.role-user {
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  color: #1e293b;
  border: 1px solid rgba(224, 231, 255, 0.8);
}

.detail-item:hover .role-badge {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Actions */
.profile-actions {
  padding: 1.5rem 2rem 2rem;
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  border-top: 1px solid #f1f5f9;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  line-height: 1;
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.btn-edit {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(6, 182, 212, 0.3);
}

.btn-edit:hover:not(:disabled) {
  background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(6, 182, 212, 0.4);
}

.btn-logout {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.btn-logout:hover:not(:disabled) {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.4);
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .profile-card {
    background: #1e293b;
    border-color: #334155;
  }
  
  .detail-value {
    color: #f1f5f9;
  }
  
  .detail-label {
    color: #94a3b8;
  }
  
  .detail-item {
    border-bottom-color: #334155;
  }
  
  .detail-item:hover {
    background: linear-gradient(135deg, #334155 0%, #475569 100%);
  }
  
  .detail-item:hover .detail-value {
    color: #f1f5f9;
  }
  
  .detail-item:hover .detail-label {
    color: #cbd5e1;
  }
  
  .detail-icon {
    background: linear-gradient(135deg, #334155 0%, #475569 100%);
  }
  
  .detail-icon svg {
    color: #cbd5e1;
  }
  
  .profile-actions {
    border-top-color: #334155;
  }
}

/* Small screens */
@media (max-width: 420px) {
  .profile-card {
    width: 92%;
    padding: 0;
  }
  
  .profile-header,
  .profile-details,
  .profile-actions {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  
  .profile-actions {
    flex-direction: column;
  }
  
  .profile-actions .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>