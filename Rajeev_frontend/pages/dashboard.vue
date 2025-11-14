<template>
  <div class="dashboard-layout">
    <div class="dashboard-container">
      <header class="dashboard-header">
        <div class="header-content">
          <div class="header-title">
            <h1 class="title">Dashboard</h1>
            <p class="subtitle">Welcome back, {{ auth.user?.username }}</p>
          </div>
          <div class="header-actions">
            <div class="user-info">
              <div class="user-avatar" @click="showprofile = true">
                {{ getInitials(auth.user?.username) }}
              </div>
              <!-- <div class="user-details">
                <div class="username">{{ auth.user?.username }}</div>
                <div class="user-role">
                  <span class="role-badge" :class="auth.user?.role">
                    {{ auth.user?.role }}
                  </span>
                </div>
              </div> -->
            </div>
            <button class="btn btn-logout" @click="logout">
              <!-- <svg class="logout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg> -->
              Logout
            </button>
            <Profile  v-if="showprofile" @close="showprofile = false" />
          </div>
        </div>
      </header>

      <main class="dashboard-main">
        <div class="dashboard-content">
          <AdminDashboard v-if="auth.hasRole('admin')" />
          <EmployeeDashboard v-else-if="auth.hasRole('employee')" />
          <UserDashboard v-else-if="auth.hasRole('user')" />
          <div v-else class="unknown-role">
            <div class="unknown-content">
              <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              <h2>Unknown Role</h2>
              <p>Your account has an unrecognized role. Please contact the system administrator.</p>
              <button class="btn btn-primary" @click="logout">Return to Login</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref} from 'vue'
import { useAuthStore } from '#imports'
import AdminDashboard from '~/components/AdminDashboard.vue'
import EmployeeDashboard from '~/components/EmployeeDashboard.vue'
import UserDashboard from '~/components/UserDashboard.vue'
import auths from '~/middleware/auth';
import Profile from './profile.vue'
const showprofile = ref(false)
definePageMeta({
    middleware: [auths],
    // layout: 'authenticated'
})
const auth = useAuthStore()
const router = useRouter()

function logout() {
  auth.logout()
  router.push('/')
}

function getInitials(username) {
  if (!username) return '??'
  return username
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
}
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 1rem;
}

.dashboard-container {
  max-width: 1800px;
  margin: 0 auto;
  height: 100%;
}

/* Header Styles */
.dashboard-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

@media (min-width: 768px) {
  .header-content {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
  }
}

.header-title .title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  line-height: 1.2;
}

.header-title .subtitle {
  font-size: 1rem;
  color: #64748b;
  margin: 0;
  font-weight: 500;
}

.header-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: stretch;
}

@media (min-width: 640px) {
  .header-actions {
    flex-direction: row;
    align-items: center;
    gap: 1.5rem;
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.username {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.875rem;
}

.user-role {
  display: flex;
}

.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
  letter-spacing: 0.025em;
}

.role-badge.admin {
  background: #dbeafe;
  color: #1e40af;
  border: 1px solid #bfdbfe;
}

.role-badge.employee {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fde68a;
}

.role-badge.user {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
}

/* Button Styles */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-decoration: none;
  line-height: 1;
  white-space: nowrap;
}

.btn:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.btn:active {
  transform: translateY(1px);
}

.btn-logout {
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
  padding: 0.75rem 1.25rem;
}

.btn-logout:hover {
  background: #f8fafc;
  color: #475569;
  border-color: #cbd5e1;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
}

.logout-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

/* Main Content */
.dashboard-main {
  min-height: 60vh;
}

.dashboard-content {
  height: 100%;
}

/* Unknown Role State */
.unknown-role {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 2rem;
}

.unknown-content {
  text-align: center;
  max-width: 400px;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.warning-icon {
  width: 4rem;
  height: 4rem;
  color: #f59e0b;
  margin: 0 auto 1.5rem;
}

.unknown-content h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.unknown-content p {
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 1.5rem 0;
}

/* Animation for smooth transitions */
.dashboard-content > * {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .dashboard-layout {
    padding: 0.5rem;
  }
  
  .header-content {
    padding: 1rem;
  }
  
  .header-title .title {
    font-size: 1.5rem;
  }
  
  .unknown-role {
    padding: 1rem;
  }
  
  .unknown-content {
    padding: 1.5rem;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .dashboard-layout {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  }
  
  .header-content,
  .unknown-content {
    background: #1e293b;
    border-color: #334155;
  }
  
  .header-title .title {
    color: #f1f5f9;
  }
  
  .header-title .subtitle {
    color: #94a3b8;
  }
  
  .user-info {
    background: #334155;
    border-color: #475569;
  }
  
  .username {
    color: #f1f5f9;
  }
  
  .btn-logout {
    background: #334155;
    color: #cbd5e1;
    border-color: #475569;
  }
  
  .btn-logout:hover {
    background: #475569;
    color: #f1f5f9;
  }
  
  .unknown-content h2 {
    color: #f1f5f9;
  }
  
  .unknown-content p {
    color: #94a3b8;
  }
}
</style>