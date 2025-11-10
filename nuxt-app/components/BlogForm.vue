<template>
  <form @submit.prevent="submit">
    <input v-model="title" placeholder="Title" />
    <textarea v-model="content" rows="6" placeholder="Content"></textarea>
    <div style="display:flex;gap:.5rem;justify-content:flex-end">
      <button type="submit">{{ editing ? 'Save' : 'Publish' }}</button>
      <button v-if="editing" type="button" @click="cancel">Cancel</button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useBlogStore } from '~/stores/blogs'
const store = useBlogStore()
const config = useRuntimeConfig()

const title = ref('')
const content = ref('')

const editing = computed(() => !!store.currentEdit)

watch(() => store.currentEdit, (val) => {
  if (val) {
    title.value = val.title
    content.value = val.content
  } else {
    title.value = ''
    content.value = ''
  }
})

const submit = async () => {
  const t = title.value.trim()
  const c = content.value.trim()
  if (!t || !c) return
  if (editing.value) {
    await store.updateBlog(config.public.apiBase, store.currentEdit.id, t, c)
  } else {
    await store.addBlog(config.public.apiBase, t, c)
  }
  title.value = ''
  content.value = ''
}
const cancel = () => store.cancelEditing()
</script>

<style scoped>
input, textarea { width:100%; padding:.6rem; border-radius:8px; border:1px solid #ddd; margin-bottom:.5rem }
button { background:linear-gradient(90deg,#667eea,#764ba2); color:#fff; border:none; padding:.5rem .8rem; border-radius:8px }
</style>
