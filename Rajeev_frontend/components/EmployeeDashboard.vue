<template>
  <section class="user-dashboard">
    <div class="dashboard-grid">
      <!-- Profile Section -->
      <div class="profile-section">
        <div class="profile-card">
          <div class="profile-header">
            <div class="profile-avatar">
              {{ getInitials(auth.user.username) }}
            </div>
            <div class="profile-info">
              <h2 class="profile-name">{{ auth.user.username }}</h2>
            </div>
          </div>
          
          <div class="profile-details">
            <div class="detail-item">
              <span class="detail-label">Username:</span>
              <span class="detail-value">{{ auth.user.username }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Email:</span>
              <span class="detail-value">{{ auth.user.email }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Role:</span>
              <span class="role-badge">{{auth.user.role}}</span>
            </div>
          </div>
        </div>
        
        <button class="btn btn-primary" @click="showBlogForm = true">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Create Post
        </button>
      </div>

      <!-- Blog List Section -->
      <div class="blog-list-section">
        <BlogList />
        <BlogForm v-if="showBlogForm" @close="showBlogForm = false" @saved="onBlogSaved" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '#imports'
import BlogList from './BlogList.vue'
import BlogForm from './BlogForm.vue'

const showBlogForm = ref(false)
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

function onBlogSaved() {
  showBlogForm.value = false
  fetchBlogs()
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

/* Profile Section */
.profile-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.profile-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.profile-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.profile-header {
  padding: 1.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.profile-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.375rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 1.375rem;
  font-weight: 700;
  margin: 0 0 0.375rem 0;
  letter-spacing: -0.025em;
}

.profile-role {
  font-size: 0.875rem;
  opacity: 0.95;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.15);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  display: inline-block;
}

.profile-details {
  padding: 1.75rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #f1f5f9;
  transition: background-color 0.2s ease;
}

.detail-item:hover {
  background: #f8fafc;
  margin: 0 -1rem;
  padding: 1rem;
  border-radius: 8px;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.detail-value {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
}

.role-badge {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #475569;
  padding: 0.375rem 1rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: 1px solid #e2e8f0;
}

/* Button Styles */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  line-height: 1;
  width: 100%;
}

.btn:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

/* Blog List Section */
.blog-list-section {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  overflow: hidden;
  min-height: 400px;
}

/* Responsive Design */
@media (max-width: 767px) {
  .user-dashboard {
    padding: 1rem;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    padding: 1.5rem;
  }
  
  .dashboard-grid {
    gap: 1.5rem;
  }
  
  .detail-item:hover {
    margin: 0 -0.5rem;
    padding: 1rem 0.5rem;
  }
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  .user-dashboard {
    background: #0f172a;
  }
  
  .profile-card,
  .blog-list-section {
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
    background: #334155;
  }
  
  .role-badge {
    background: linear-gradient(135deg, #334155 0%, #475569 100%);
    color: #cbd5e1;
    border-color: #475569;
  }
  
  .btn-primary {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
  }
  
  .btn-primary:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.5);
  }
}
</style>