<template>
  <header class="header-bar">
    <nav>
      <ul class="nav-left">
        <li>
          <NuxtLink to="/Homepage" :class="{ active: isActive('/Homepage') }">Home</NuxtLink>
        </li>
        <li>
          <NuxtLink to="/About" :class="{ active: isActive('/About') }">About</NuxtLink>
        </li>
        <li>
          <NuxtLink to="/TaskTracker" :class="{ active: isActive('/TaskTracker') }">Task Tracker</NuxtLink>
        </li>
        <li>
          <NuxtLink to="/Contact" :class="{ active: isActive('/Contact') }">Contact Us</NuxtLink>
        </li>
      </ul>

      <ul class="nav-right">
        <li>
          <button @click="logout" class="logout-btn">Logout</button>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script setup>
import { useRoute, useRouter } from '#imports'
import { useAuthStore } from '#imports'

definePageMeta({ layout: 'authenticated' })

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

function isActive(path) {
  return route.path === path
}

function logout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.header-bar {
  background-color: #4e5a66;
  color: #fff;
  padding: 22px 24px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

nav {
  display: flex;
  align-items: center;
}

.nav-left, .nav-right {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 20px;
}

.nav-left li a {
  color: #fff;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 4px;
  transition: background 0.3s;
}

.nav-left li a:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-left li a.active {
  background-color: #fff;
  color: #007bff;
  font-weight: bold;
}

.nav-right {
  margin-left: auto;
}

.logout-btn {
  background-color: #ff4d4f;
  border: none;
  color: #fff;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.3s;
}

.logout-btn:hover {
  background-color: #e63946;
}
</style>
