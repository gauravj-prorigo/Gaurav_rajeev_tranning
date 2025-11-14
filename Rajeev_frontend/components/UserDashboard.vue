<template>
  <section class="user-dashboard">
    <div class="dashboard-grid">
      <!-- Profile Card -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="header-content">
            <h2 class="profile-title">Profile</h2>
            <div class="profile-avatar">
              {{ getInitials(auth.user.username) }}
            </div>
          </div>
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
              <span class="detail-value">{{ auth.user.username }}</span>
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
              <span class="detail-value">{{ auth.user.email }}</span>
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
              <span class="role-badge user">User</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Blog List Section -->
      <div class="blog-list-container">
        <BlogList />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '#imports'
import BlogList from './BlogList.vue'

const auth = useAuthStore()
const API_BASE = 'http://127.0.0.1:8000'

const blogs = ref([])
const loading = ref(false)

onMounted(() => { 
  fetchBlogs() 
})

async function fetchBlogs() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/api/blogs/`, { 
      headers: { Authorization: `Bearer ${auth.token}` } 
    })
    blogs.value = await res.json()
  } catch (e) { 
    console.error(e) 
  } finally { 
    loading.value = false 
  }
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
.user-dashboard {
  padding: 1.5rem;
  max-width: 1500px;
  margin: 0 auto;

  min-height: 100vh;
}

/* Main Grid Layout */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 380px 1fr;
  }
}

/* Profile Card Styles */
.profile-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  overflow: hidden;
  transition: all 0.3s ease;
  height: fit-content;
  backdrop-filter: blur(10px);
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.profile-header {
  padding: 2rem;
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
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.025em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-avatar {
  width: 65px;
  height: 65px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.4rem;
  border: 2px solid rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.profile-card:hover .profile-avatar {
  transform: scale(1.1) rotate(5deg);
  background: rgba(255, 255, 255, 0.35);
}

.profile-details {
  padding: 1.75rem;
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
  width: 48px;
  height: 48px;
  border-radius: 14px;
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
  width: 22px;
  height: 22px;
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
  font-size: 1.05rem;
  letter-spacing: -0.025em;
  transition: color 0.3s ease;
}

.detail-item:hover .detail-value {
  color: #334155;
}

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

.role-badge.user {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #475569;
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.detail-item:hover .role-badge.user {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* Blog List Container */
.blog-list-container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  overflow: hidden;
  min-height: 400px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.blog-list-container:hover {
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
}

/* Responsive adjustments */
@media (max-width: 767px) {
  .user-dashboard {
    padding: 1rem;
  }
  
  .profile-header {
    padding: 1.5rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .profile-details {
    padding: 1.5rem;
  }
  
  .detail-item {
    padding: 1rem 0.75rem;
    margin: 0;
    gap: 1rem;
  }
  
  .dashboard-grid {
    gap: 1.5rem;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .user-dashboard {
    background: #0f172a;
  }
  
  .profile-card,
  .blog-list-container {
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
  
  .role-badge.user {
    background: linear-gradient(135deg, #334155 0%, #475569 100%);
    color: #cbd5e1;
    border-color: #475569;
  }
  
  .detail-item:hover .detail-icon {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  .detail-item:hover .role-badge.user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }
}
</style>