<template>
    <div class="form-page">
        <div class="form-container">
            <h1 class="form-heading">
                <Icon :icon="isEdit ? 'line-md:edit-twotone' : 'line-md:file-document'" width="28" height="28"
                    class="icon" />
                {{ isEdit ? ' Edit Blog' : ' Add New Blog' }}
            </h1>


            <form @submit.prevent="handleSubmit">
                <div class="form-group">
                    <label for="title">Title</label>
                    <input id="title" v-model="form.title" type="text" placeholder="Enter blog title" required />
                </div>

                <div class="form-group">
                    <label for="content">Content</label>
                    <textarea id="content" v-model="form.content" rows="6" placeholder="Write your blog content here..."
                        required></textarea>
                </div>

                <div class="buttons">
                    <button type="submit" class="submit-btn">
                        {{ isEdit ? 'Update Blog' : 'Add Blog' }}
                    </button>
                    <NuxtLink to="/BlogList" class="cancel-btn">Cancel</NuxtLink>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { UseBlogstore } from '#imports'
import { Icon } from '@iconify/vue'
import auth from '~/middleware/auth';
definePageMeta({
    middleware: [auth],
    layout: 'authenticated'
})

const store = UseBlogstore()
const route = useRoute()
const router = useRouter()

const form = reactive({ title: '', content: '' })
const isEdit = computed(() => !!route.query.id)

if (isEdit.value) {
    const blog = store.blog.find(b => b.id === parseInt(route.query.id))
    if (blog) {
        form.title = blog.title
        form.content = blog.content
    }
}

async function handleSubmit() {
    if (isEdit.value) {
        await store.UpdateBlog(route.query.id, form)
        alert('Blog updated successfully!')
    } else {
        await store.AddBlogs(form)
        alert('Blog added successfully!')
    }
    router.push('/BlogList')
}
</script>

<style scoped>
.form-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 90vh;
    background: linear-gradient(135deg, #e3f2fd, #f9f9f9);
    padding: 20px;
}

.form-container {
    background-color: white;
    padding: 40px;
    border-radius: 10px;
    width: 100%;
    max-width: 600px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #3498db;
    margin-bottom: 30px;
    font-size: 2rem;
}

.form-group {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
}

label {
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 8px;
}


input,
textarea {
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 1rem;
    transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus,
textarea:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 6px rgba(52, 152, 219, 0.3);
}

.buttons {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.submit-btn {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.2s;
}

.submit-btn:hover {
    background-color: #2980b9;
    transform: scale(1.05);
}

.cancel-btn {
    background-color: #e74c3c;
    color: white;
    padding: 12px 20px;
    border-radius: 6px;
    text-decoration: none;
    transition: background 0.3s ease, transform 0.2s;
}

.cancel-btn:hover {
    background-color: #c0392b;
    transform: scale(1.05);
}
</style>
