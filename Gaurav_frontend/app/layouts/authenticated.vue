<template>
  <div>
    <HeaderBar />
    <main>
      <NuxtPage /> <!-- actual page content -->
    </main>
    <FooterBar />
  </div>
</template>

<script setup>
import HeaderBar from '../pages/HeaderBar.vue'
import FooterBar from '~/pages/FooterBar.vue';

</script>

<style scoped>
main {
  min-height: 80vh; /* ensures footer at bottom */
}
</style>
