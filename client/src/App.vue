<script setup>
import WelcomeCard from './components/WelcomeCard.vue'
</script>

<template>
  <main>
    <WelcomeCard class="bottomup-effect" />
  </main>
</template>

<style scoped>
main {
  background-image: url('./assets/blurry-gradient-haikei.svg');
  min-height: 100vh; /* Add this */
  width: 100%; /* Add this */
  background-repeat: no-repeat;
  background-size: cover;
  margin: 0;
  padding: 0;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>
