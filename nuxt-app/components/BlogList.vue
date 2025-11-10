<template>
  <div>
    <div v-if="blogs.length">
      <div v-for="b in blogs" :key="b.id" class="card">
        <div v-if="store.currentEdit && store.currentEdit.id === b.id">
          <!-- editing is handled in BlogForm; this is normal view -->
          <small>Editing...</small>
        </div>
        <div v-else>
          <h3>{{ b.title }}</h3>
          <p>{{ b.content }}</p>
          <small>{{ formatDate(b.created_at) }}</small>
          <div style="text-align:right;margin-top:.5rem">
            <button @click="store.startEditing(b)">Edit</button>
            <button @click="remove(b.id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
    <p v-else>No blogs yet.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useBlogStore } from '~/stores/blogs'
const store = useBlogStore()
const blogs = computed(() => store.allBlogs)
const config = useRuntimeConfig()

const remove = (id) => {
  if (confirm('Delete this blog?')) store.deleteBlog(config.public.apiBase, id)
}
const formatDate = (d) => d ? new Date(d).toLocaleString() : ''
</script>

<style scoped>
.card{ background:#fff; padding:1rem; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.06); margin-bottom:1rem }
button{ margin-left:.5rem; padding:.3rem .6rem; border-radius:6px; border:none; cursor:pointer }
</style>
