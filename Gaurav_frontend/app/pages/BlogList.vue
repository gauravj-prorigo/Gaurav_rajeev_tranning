<template>
    <div class="blog-page">
        <header class="page-header">
            <h1>Blog Management</h1>
            <NuxtLink  to="/AddEdit" class="add-btn">
                + Add New Blog</NuxtLink>
        </header>

        <div v-if="store.loading" class="loading">
            <div class="spinner"></div>
            <p>Loading blogs...</p>
        </div>
        <div v-if="store.error" class="error">{{ store.error }}</div>

        <div v-else class="blog-list">
            <div v-for="blog in store.blog" :key="blog.id" class="blog-card">
                <h2>{{ blog.title }}</h2>
                <p>{{ blog.content }}</p>

                <div class="actions">
                    <NuxtLink :to="`/AddEdit?id=${blog.id}`" class="edit-btn">
                        <Icon icon="line-md:edit-twotone" width="20" height="20" />
                        <span>Edit</span>
                    </NuxtLink>

                    <button   @click="confirmDelete(blog.id)" class="delete-btn">
                        <Icon icon="material-symbols:delete-forever-outline" width="20" height="20" />
                        <span>Delete</span>
                    </button>
                </div>

            </div>
            <p v-if="!store.blog.length && !store.loading" class="empty">
                No blogs available. Click “Add New Blog” to create one!
            </p>
        </div>
    </div>
</template>

<script setup>
import { Icon } from '@iconify/vue'
import { UseBlogstore } from '#imports'
import auth from '~/middleware/auth';
definePageMeta({
    middleware: [auth],
    layout: 'authenticated'
})

const store = UseBlogstore()
store.fetchBlogs()

const confirmDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this blog?')) {
        await store.DeleteBlog(id)
        alert('Blog deleted successfully!')
    }
}

const isAdminOrEmployee = computed(() => {
  const role = auth.user?.role || ''
  console.log("isadmin ", role)
  return role === 'admin' || role === 'employee'
})
</script>

<style scoped>
.blog-page {
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
    font-family: "Segoe UI", Roboto, sans-serif;
    color: #2c3e50;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.page-header h1 {
    font-size: 2rem;
    color: #3498db;
}

.add-btn {
    background-color: #2ecc71;
    padding: 10px 20px;
    border-radius: 6px;
    color: white;
    text-decoration: none;
    transition: background 0.3s ease;
}

.add-btn:hover {
    background-color: #27ae60;
}

.blog-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.blog-card {
    background: #f9f9f9;
    border-radius: 10px;
    padding: 20px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s, box-shadow 0.2s;
}

.blog-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 12px rgba(0, 0, 0, 0.1);
}

.blog-card h2 {
    color: #3498db;
    margin-bottom: 10px;
    font-size: 1.4rem;
}

.blog-card p {
    color: #555;
    line-height: 1.5;
}

.actions {
    margin-top: 15px;
    display: flex;
    gap: 10px;
}

.edit-btn,
.delete-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 4px;
    text-decoration: none;
    color: white;
    cursor: pointer;
    border: none;
}

.edit-btn {
    background-color: #3498db;
}

.delete-btn {
    background-color: #e74c3c;
}

.delete-btn {
    background-color: #e74c3c;
    color: white;
}

.delete-btn:hover {
    background-color: #c0392b;
    transform: scale(1.05);
}

.error {
    color: #e74c3c;
    text-align: center;
    font-weight: bold;
    margin-top: 20px;
}

.empty {
    text-align: center;
    color: #888;
    margin-top: 40px;
    font-style: italic;
}
</style>
