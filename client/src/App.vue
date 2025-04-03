<template>
  <div class="background-container"></div>
  <div class="content-container">
	  <WelcomeCard v-show="!isChatJoined" @joined-chat="handleJoinedChat"/>
    <Chat v-if="isChatJoined" @leave-chat="handleLeaveChat"/>
  </div>
</template>

<script setup>
import WelcomeCard from './components/WelcomeCard.vue'
import Chat from './components/Chat.vue'
import { ref } from 'vue'

// Reactive state to track if the user has joined a chat room
const isChatJoined = ref(false);

// Function to handle the event when the user joins the chat room
const handleJoinedChat = () => {
  isChatJoined.value = true;
};

const handleLeaveChat = () => {
	isChatJoined.value = false
}
</script>

<style scoped>
.background-container {
  background-image: url('./assets/blurry-gradient-haikei.svg');
  min-height: 100vh;
  width: 100%;
  background-repeat: no-repeat;
  background-size: cover;
  position: fixed;
  top: 0;
  left: 0;
  z-index: -1; /* Ensure it's behind the content */
}

.content-container {
  /* Add any styling for the content container if needed */
  padding-top: 20px; /* Example: Add some top padding so content isn't right at the top */
}

main {
}

.scale-up-center {
  animation: scale-up-center 1s cubic-bezier(0.445, 0.05, 0.55, 0.95) both;
}

@keyframes scale-up-center {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
