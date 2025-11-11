// plugins/toast.client.js
import { defineNuxtPlugin } from '#app'
import Vue3Toastify, { toast, ToastContainer } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export default defineNuxtPlugin((nuxtApp) => {
  // register the toast library with Vue (client only)
  nuxtApp.vueApp.use(Vue3Toastify, {
    autoClose: 3000,
    position: 'top-right',
    theme: 'colored',
    pauseOnHover: true,
    draggable: true,
  })

  // register ToastContainer as a global component so layouts can use <ToastContainer />
  nuxtApp.vueApp.component('ToastContainer', ToastContainer)

  // provide $toast so useNuxtApp().$toast works
  return {
    provide: {
      $toast: toast
    }
  }
})
