<template>
  <div class="background-container"></div>
  <div class="content-container">
    <WelcomeCard
      v-show="!isChatJoined"
      @joined-chat="handleJoinedChat"
      @room-created="handleRoomCreated"
      :class="welcomeCardTransitionClass"
    />
    <Chat v-if="isChatJoined" @leave-chat="handleLeaveChat" :class="chatTransitionClass" />

    <div v-if="showNotification" class="notification">
      Room created with ID: {{ notificationMessage }}
      <button @click="closeNotification" class="close-button">
        <svg
          viewBox="0 0 24 24"
          fill="white"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
        >
          <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
          <g id="SVGRepo_iconCarrier">
            <path
              opacity="0.4"
              d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z"
              fill="#292D32"
            ></path>
            <path
              d="M13.0594 12.0001L15.3594 9.70011C15.6494 9.41011 15.6494 8.93011 15.3594 8.64011C15.0694 8.35011 14.5894 8.35011 14.2994 8.64011L11.9994 10.9401L9.69937 8.64011C9.40937 8.35011 8.92937 8.35011 8.63938 8.64011C8.34938 8.93011 8.34938 9.41011 8.63938 9.70011L10.9394 12.0001L8.63938 14.3001C8.34938 14.5901 8.34938 15.0701 8.63938 15.3601C8.78938 15.5101 8.97937 15.5801 9.16937 15.5801C9.35937 15.5801 9.54937 15.5101 9.69937 15.3601L11.9994 13.0601L14.2994 15.3601C14.4494 15.5101 14.6394 15.5801 14.8294 15.5801C15.0194 15.5801 15.2094 15.5101 15.3594 15.3601C15.6494 15.0701 15.6494 14.5901 15.3594 14.3001L13.0594 12.0001Z"
              fill="white"
            ></path>
          </g>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import WelcomeCard from './components/WelcomeCard.vue'
import Chat from './components/Chat.vue'
import { ref, computed, onMounted, watch } from 'vue'

// Reactive state to track if the user has joined a chat room
const isChatJoined = ref(false)
const isWelcomeCardLeaving = ref(false)
const isChatLeaving = ref(false)
const isWelcomeCardEntering = ref(false)
const isChatEntering = ref(false)
const showNotification = ref(false)
const notificationMessage = ref('')

// Function to handle the event when the user joins the chat room
const handleJoinedChat = () => {
  isWelcomeCardLeaving.value = true
  // Wait for the animation to finish before actually hiding the component
  setTimeout(() => {
    // Trigger the enter animation for Chat *before* setting isChatJoined
    isChatEntering.value = true
    isChatJoined.value = true
    isWelcomeCardLeaving.value = false
  }, 500) // Duration of the slide-out-top animation
}

const handleLeaveChat = () => {
  isChatLeaving.value = true
  // Wait for the animation to finish before actually hiding the component
  setTimeout(() => {
    // Trigger the enter animation for WelcomeCard *before* setting isChatJoined
    isWelcomeCardEntering.value = true
    isChatJoined.value = false
    isChatLeaving.value = false
  }, 500) // Duration of the slide-out-top animation
}

const welcomeCardTransitionClass = computed(() => {
  if (isWelcomeCardLeaving.value) {
    return 'slide-out-top'
  } else if (!isChatJoined.value && isWelcomeCardEntering.value) {
    return 'scale-in-center'
  }
  return ''
})

const chatTransitionClass = computed(() => {
  if (isChatLeaving.value) {
    return 'slide-out-bottom'
  } else if (isChatJoined.value && isChatEntering.value) {
    return 'scale-in-center'
  }
  return ''
})

// Trigger initial enter animation for WelcomeCard on mount
onMounted(() => {
  isWelcomeCardEntering.value = true
})

// Reset enter animation flags after the animation duration
const resetWelcomeCardEnter = () => {
  setTimeout(() => {
    isWelcomeCardEntering.value = false
  }, 500) // Duration of scale-in-center
}

const resetChatEnter = () => {
  setTimeout(() => {
    isChatEntering.value = false
  }, 500) // Duration of scale-in-center
}

watch(
  () => !isChatJoined.value,
  (newValue) => {
    if (newValue) {
      resetWelcomeCardEnter()
    }
  },
)

watch(
  () => isChatJoined.value,
  (newValue) => {
    if (newValue) {
      resetChatEnter()
    }
  },
)

const handleRoomCreated = (roomId) => {
  notificationMessage.value = `${roomId}`
  showNotification.value = true
}

const closeNotification = () => {
  showNotification.value = false
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
.slide-out-top {
  -webkit-animation: slide-out-top 0.5s cubic-bezier(0.55, 0.085, 0.68, 0.53) both;
  animation: slide-out-top 0.5s cubic-bezier(0.55, 0.085, 0.68, 0.53) both;
}

/* ----------------------------------------------
 * Generated by Animista on 2025-4-4 6:8:30
 * Licensed under FreeBSD License.
 * See http://animista.net/license for more info.
 * w: http://animista.net, t: @cssanimista
 * ---------------------------------------------- */

/**
 * ----------------------------------------
 * animation slide-out-top
 * ----------------------------------------
 */
@-webkit-keyframes slide-out-top {
  0% {
    -webkit-transform: translateY(0);
    transform: translateY(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: translateY(-1000px);
    transform: translateY(-1000px);
    opacity: 0;
  }
}
@keyframes slide-out-top {
  0% {
    -webkit-transform: translateY(0);
    transform: translateY(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: translateY(-1000px);
    transform: translateY(-1000px);
    opacity: 0;
  }
}
.slide-out-bottom {
  -webkit-animation: slide-out-bottom 0.5s cubic-bezier(0.55, 0.085, 0.68, 0.53) both;
  animation: slide-out-bottom 0.5s cubic-bezier(0.55, 0.085, 0.68, 0.53) both;
}

/* ----------------------------------------------
 * Generated by Animista on 2025-4-4 6:9:36
 * Licensed under FreeBSD License.
 * See http://animista.net/license for more info.
 * w: http://animista.net, t: @cssanimista
 * ---------------------------------------------- */

/**
 * ----------------------------------------
 * animation slide-out-bottom
 * ----------------------------------------
 */
@-webkit-keyframes slide-out-bottom {
  0% {
    -webkit-transform: translateY(0);
    transform: translateY(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: translateY(1000px);
    transform: translateY(1000px);
    opacity: 0;
  }
}
@keyframes slide-out-bottom {
  0% {
    -webkit-transform: translateY(0);
    transform: translateY(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: translateY(1000px);
    transform: translateY(1000px);
    opacity: 0;
  }
}
.scale-in-center {
  -webkit-animation: scale-in-center 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  animation: scale-in-center 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  /* Add this to ensure the element starts scaled down */
  transform: scale(0);
}

/* ----------------------------------------------
 * Generated by Animista on 2025-4-4 6:12:57
 * Licensed under FreeBSD License.
 * See http://animista.net/license for more info.
 * w: http://animista.net, t: @cssanimista
 * ---------------------------------------------- */

/**
 * ----------------------------------------
 * animation scale-in-center
 * ----------------------------------------
 */
@-webkit-keyframes scale-in-center {
  0% {
    -webkit-transform: scale(0);
    transform: scale(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(1);
    transform: scale(1);
    opacity: 1;
  }
}
@keyframes scale-in-center {
  0% {
    -webkit-transform: scale(0);
    transform: scale(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(1);
    transform: scale(1);
    opacity: 1;
  }
}

/* Notification styles */
.notification {
  position: absolute;
  top: 10px; /* Adjust as needed */
  left: 50%;
  transform: translateX(-50%);
  background-color: #4caf50; /* Example background color */
  color: white;
  padding: 15px 20px;
  border-radius: 5px;
  z-index: 10; /* Ensure it's on top */
  opacity: 0.9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.close-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  margin-left: 10px;
  padding: 0;
  line-height: 1;
  display: flex; /* To center the SVG inside the button */
  align-items: center;
  justify-content: center;
}
</style>
