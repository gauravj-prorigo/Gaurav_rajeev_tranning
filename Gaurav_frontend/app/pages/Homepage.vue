<template>
    <div class="home-page">
        <section class="hero">
            <div class="overlay">
                <h1>Welcome to My Blog</h1>
                <p>Read, write, and share your thoughts. Stay updated with the latest ideas!</p>
                <NuxtLink to="/BlogList" class="btn-primary">View Blogs</NuxtLink>
            </div>
        </section>

    
    </div>
</template>

<script setup>
import { useAuthStore } from '#imports';
import { useRouter } from '#imports'
import auth from '~/middleware/auth';
definePageMeta({
    middleware: [auth],
    layout: 'authenticated'
})
const store = useAuthStore()
const router = useRouter()
</script>

<style scoped>
.home-page {
    font-family: "Segoe UI", Roboto, sans-serif;
    color: #fff;
}

.hero {
    /* background: url(../../assets/photo-1507525428034-b723cf961d3e.avif) center/cover no-repeat; */
    height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.hero .overlay {
    text-align: center;
    background: rgba(0, 0, 0, 0.5);
    padding: 40px;
    border-radius: 10px;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 20px;
    color: #ffd700;
}

.hero p {
    font-size: 1.2rem;
    margin-bottom: 20px;
}

.btn-primary {
    background-color: #3498db;
    color: white;
    padding: 12px 25px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: bold;
    transition: all 0.3s;
}

.btn-primary:hover {
    background-color: #2980b9;
    transform: translateY(-3px);
}

.intro {
    text-align: center;
    background: #f4f4f4;
    color: #333;
    padding: 50px 20px;
}

.intro h2 {
    font-size: 2rem;
    margin-bottom: 15px;
}

.intro p {
    font-size: 1.1rem;
    max-width: 700px;
    margin: auto;
    line-height: 1.6;
}
</style>
