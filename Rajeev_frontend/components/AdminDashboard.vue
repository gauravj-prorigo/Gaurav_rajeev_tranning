<template>
    <section class="admin-dashboard">
        <!-- Profile card -->
        <div class="dashboard-grid">
            
            <div class="profile-card">
                <div class="profile-header">
                    <h2 class="profile-title">Admin Profile</h2>
                    <div class="profile-avatar">
                        {{ getInitials(auth.user.username) }}
                    </div>
                </div>
                <div class="profile-details">
                    <div class="detail-item">
                        <span class="detail-label">Username:</span>
                        <span class="detail-value">{{ auth.user.username }}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Email:</span>
                        <span class="detail-value">{{ auth.user.email ? auth.user.email : '-' }}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Role:</span>
                        <span class="role-badge">Admin</span>
                    </div>
                       
                </div>
              
            </div>
            

            <!-- Users table -->
            <div class="users-card">
                <div class="card-header">
                    <h3 class="card-title">All Users</h3>
                    <button class="btn btn-primary" @click="fetchUsers" :disabled="loadingUsers">
                        <span v-if="loadingUsers" class="btn-loading">
                            <span class="spinner"></span>
                            Loading...
                        </span>
                        <span v-else>Refresh</span>
                    </button>
                </div>

                <div v-if="loadingUsers" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading users...</p>
                </div>

                <div v-else class="table-container">
                    <table class="users-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Username</th>
                                <th>Email</th>
                                <th>Role</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="u in users" :key="u.id">
                                <td data-label="ID">{{ u.id }}</td>
                                <td data-label="Username">{{ u.username }}</td>
                                <td data-label="Email">{{ u.email ? u.email : '-' }}</td>
                                <td data-label="Role">
                                    <select v-model="u.role" @change="assignRole(u)" class="role-select"
                                        :class="`role-${u.role}`">
                                        <option value="user">User</option>
                                        <option value="employee">Employee</option>
                                        <option value="admin">Admin</option>
                                    </select>
                                </td>
                                <td data-label="Actions">
                                    <button class="btn btn-sm" @click="viewUser(u)">View</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <UserModal v-if="selectedUser" :key="selectedUser.id" :user="selectedUser" @close="closeUserModal" />
        </div>

        <!-- All Blogs -->
        <!-- <div class="blogs-card">

            <div class="card-header">
                <h3 class="card-title">All Blogs</h3>
                <button class="btn btn-primary" @click="fetchBlogs" :disabled="loadingBlogs">
                    <span v-if="loadingBlogs" class="btn-loading">
                        <span class="spinner"></span>
                        Loading...
                    </span>
                    <span v-else>Refresh</span>
                </button>
            </div>

            <div v-if="loadingBlogs" class="loading-state">
                <div class="spinner"></div>
                <p>Loading blogs...</p>
            </div>

            <div v-else class="blogs-list">
                <div v-for="b in blogs" :key="b.id" class="blog-item">
                    <div class="blog-content">
                        <h4 class="blog-title">{{ b.title }}</h4>
                        <div class="blog-meta">
                            <span class="blog-author">By: {{ b.author?.username ?? '—' }}</span>
                            <span class="blog-date" v-if="b.created_at">{{ formatDate(b.created_at) }}</span>
                        </div>
                        <p class="blog-excerpt">{{ excerpt(b.content) }}</p>
                    </div>
                    <div class="blog-actions">
                        <button class="btn btn-secondary" @click="openEditor(b)">Edit</button>
                        <button class="btn btn-danger" @click="deleteBlog(b)">Delete</button>
                    </div>
                </div>

                <div v-if="blogs.length === 0" class="empty-state">
                    <p>No blogs found</p>
                </div>
            </div>
        </div> -->
        <div>
             <button class="btn btn-primary" @click="showBlogForm = true">Add Post</button>
                      <BlogList :blogs="blogs" @edit="onEdit" @delete="onDelete" @view="onView" />

        </div>
        <!-- Blog editor modal -->
         <!-- <BlogList/> -->
   <BlogForm v-if="showBlogForm" @close="showBlogForm = false" />
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '#imports'
import BlogForm from '~/components/BlogForm.vue'
import UserModal from '../pages/usermodel.vue'

const showBlogForm = ref(false)
const auth = useAuthStore()
const API_BASE = 'http://127.0.0.1:8000' // adjust if needed

const users = ref([])
const blogs = ref([])
const loadingUsers = ref(false)
const loadingBlogs = ref(false)
const selectedUser = ref(null)


const editorOpen = ref(false)
const editing = ref(null)

onMounted(() => {
    fetchUsers()
    fetchBlogs()
})

async function fetchUsers() {
    loadingUsers.value = true
    try {
        const res = await fetch(`${API_BASE}/api/users/`, {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        users.value = await res.json()
    } catch (e) {
        console.error(e)
    } finally {
        loadingUsers.value = false
    }
}

async function fetchBlogs() {
    loadingBlogs.value = true
    try {
        const res = await fetch(`${API_BASE}/api/blogs/`, {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        blogs.value = await res.json()
    } catch (e) {
        console.error(e)
    } finally {
        loadingBlogs.value = false
    }
}

async function assignRole(user) {
    const originalRole = user.role
    try {
        await fetch(`${API_BASE}/api/users/${user.id}/role/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${auth.token}`
            },
            body: JSON.stringify({ role: user.role })
        })
        // Show success feedback
        console.log(`Role updated to ${user.role} for user ${user.username}`)
    } catch (e) {
        console.error(e)
        // Revert on error
        user.role = originalRole
    }
}

function viewUser(u) {
    // simple view - you can open a modal or route to user's page
    // alert(`User: ${u.username}\nEmail: ${u.email}\nRole: ${u.role}`)
    selectedUser.value = { ...u }
}
function closeUserModal() {
    selectedUser.value = null
}

function excerpt(text = '', len = 160) {
    return text.length > len ? text.slice(0, len) + '…' : text
}

function openEditor(blog) {
    editing.value = blog ? { ...blog } : null
    editorOpen.value = true
}

function closeEditor() {
    editorOpen.value = false;
    editing.value = null
}

function onSaved() {
    closeEditor();
    fetchBlogs()
}

async function deleteBlog(blog) {
    if (!confirm('Are you sure you want to delete this blog?')) return
    try {
        await fetch(`${API_BASE}/api/blogs/${blog.id}/`, {
            method: 'DELETE',
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        fetchBlogs()
    } catch (e) {
        console.error(e)
    }
}

function getInitials(username) {
    return username
        .split(' ')
        .map(name => name.charAt(0))
        .join('')
        .toUpperCase()
        .substring(0, 2)
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' }
    return new Date(dateString).toLocaleDateString(undefined, options)
}
</script>

<style scoped>
.admin-dashboard {
    padding: 1rem;
    max-width: 1500px;
    margin: 0 auto;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #334155;
}

/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
    .dashboard-grid {
        grid-template-columns: 1fr 2fr;
    }
}

/* Card Styles */
.profile-card,
.users-card,
.blogs-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.profile-card:hover,
.users-card:hover,
.blogs-card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transform: translateY(-2px);
}

/* Profile Card */
.profile-header {
    padding: 1.5rem;
    background: linear-gradient(305deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.profile-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
}

.profile-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.1rem;
}

.profile-details {
    padding: 1.5rem;
}

.detail-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid #f1f5f9;
}

.detail-item:last-child {
    border-bottom: none;
}

.detail-label {
    font-weight: 500;
    color: #64748b;
}

.detail-value {
    font-weight: 600;
}

.role-badge {
    background: #f1f5f9;
    color: #475569;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Card Header */
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #f1f5f9;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
    color: #1e293b;
}

/* Button Styles */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
    line-height: 1;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background: #3b82f6;
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background: #2563eb;
}

.btn-secondary {
    background: #e2e8f0;
    color: #475569;
}

.btn-secondary:hover:not(:disabled) {
    background: #cbd5e1;
}

.btn-danger {
    background: #ef4444;
    color: white;
}

.btn-danger:hover:not(:disabled) {
    background: #dc2626;
}

.btn-sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
}

.btn-loading {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Loading State */
.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    color: #64748b;
}

.spinner {
    width: 24px;
    height: 24px;
    border: 2px solid transparent;
    border-top: 2px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* Table Styles */
.table-container {
    overflow-x: auto;
    max-height: 400px;
}

.users-table {
    width: 100%;
    border-collapse: collapse;
}

.users-table th {
    background: #f8fafc;
    padding: 0.75rem 1rem;
    text-align: left;
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1px solid #e2e8f0;
}

.users-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #f1f5f9;
    font-size: 0.875rem;
}

.users-table tr:last-child td {
    border-bottom: none;
}

.users-table tr:hover {
    background: #f8fafc;
}

/* Role Select */
.role-select {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 0.875rem;
    background: white;
    cursor: pointer;
    transition: border-color 0.2s;
}

.role-select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.role-user {
    color: #475569;
}

.role-employee {
    color: #d97706;
}

.role-admin {
    color: #059669;
}

/* Blog List Styles */
.blogs-card {
    padding: 0;
}

.blogs-list {
    padding: 0 1.5rem;
}

.blog-item {
    display: flex;
    flex-direction: column;
    padding: 1.5rem 0;
    border-bottom: 1px solid #f1f5f9;
    gap: 1rem;
}

.blog-item:last-child {
    border-bottom: none;
}

@media (min-width: 768px) {
    .blog-item {
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
    }
}

.blog-content {
    flex: 1;
}

.blog-title {
    font-size: 1.125rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    color: #1e293b;
}

.blog-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.75rem;
    font-size: 0.875rem;
    color: #64748b;
}

.blog-author {
    font-weight: 500;
}

.blog-date {
    font-style: italic;
}

.blog-excerpt {
    margin: 0;
    color: #64748b;
    line-height: 1.5;
}

.blog-actions {
    display: flex;
    gap: 0.5rem;
}

@media (max-width: 767px) {
    .blog-actions {
        width: 100%;
    }

    .blog-actions .btn {
        flex: 1;
    }
}

/* Empty State */
.empty-state {
    padding: 3rem;
    text-align: center;
    color: #64748b;
}

/* Responsive Table */
@media (max-width: 767px) {
    .users-table {
        display: block;
    }

    .users-table thead {
        display: none;
    }

    .users-table tbody,
    .users-table tr,
    .users-table td {
        display: block;
        width: 100%;
    }

    .users-table tr {
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }

    .users-table td {
        padding: 0.75rem;
        border-bottom: 1px solid #f1f5f9;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .users-table td:last-child {
        border-bottom: none;
    }

    .users-table td::before {
        content: attr(data-label);
        font-weight: 600;
        color: #64748b;
        margin-right: 1rem;
    }
}
</style>