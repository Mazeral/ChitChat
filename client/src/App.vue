<template>
  <div class="background-container"></div>
  <div class="content-container">
    <WelcomeCard
      v-show="!isRoomJoined"
      @room-joined="handleRoomJoined"
      @room-created="handleRoomCreated"
      @name-submitted="handleJoinedChat"
      :class="welcomeCardTransitionClass"
    />
    <Chat
      v-if="isRoomJoined"
      @leave-room="handleLeaveChat"
      @send-message="sendWsMessage"
      :userName="userName"
      :messages="messages"
      :class="chatTransitionClass"
      :roomId="roomId"
    />
    <div v-if="showNotification" class="notification" :class="notificationType">
      {{ notificationMessage }}
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
// Import nextTick
import { ref, computed, onMounted, watch, nextTick } from 'vue'

// Reactive state to track if the user has joined a chat room
const isRoomJoined = ref(false)
const isWelcomeCardLeaving = ref(false)
const isChatLeaving = ref(false)
const isWelcomeCardEntering = ref(true) // Start entering on mount
const isChatEntering = ref(false)
const showNotification = ref(false)
const notificationMessage = ref('')
const userName = ref('')
const messages = ref([])
const websocket = ref(null)
const roomId = ref('')
const notificationType = ref('success') // Default to success

// Function to handle the event when the user submits their name
const handleJoinedChat = (name) => {
  userName.value = name
  console.log('handleJoinedChat (name submitted) called with name:', name)
}

const handleLeaveChat = async () => {
  isChatLeaving.value = true

  try {
    if (websocket.value?.readyState === WebSocket.OPEN) {
      // Wait for disconnect message to be sent
      await websocket.value.send(
        JSON.stringify({
          action: 'disconnect',
          room_id: roomId.value,
          username: userName.value,
        }),
      )

      // Give server time to process before closing
      await new Promise((resolve) => setTimeout(resolve, 500))
    }
  } catch (error) {
    console.error('Error during disconnect:', error)
  } finally {
    // Proceed with UI transition regardless of WebSocket state
    isRoomJoined.value = false
    messages.value = []
    isWelcomeCardEntering.value = true

    // Close WebSocket if still open
    if (websocket.value?.readyState === WebSocket.OPEN) {
      websocket.value.close()
    }

    // Reset animation after transition
    setTimeout(() => {
      isChatLeaving.value = false
    }, 500)
  }
}

const handleRoomCreated = ({ roomId: newRoomId, userName: creatorName }) => {
  roomId.value = newRoomId
  connectWebSocket(newRoomId, creatorName, 'create') // Add 'create' action
  showNotification.value = true
}

const handleRoomJoined = ({ roomId: joinRoomId, userName: participantName }) => {
  roomId.value = joinRoomId
  connectWebSocket(joinRoomId, participantName, 'join') // Add 'join' action
  showNotification.value = true
}

// --- Computed Classes (Unchanged but verify class names match CSS) ---
const welcomeCardTransitionClass = computed(() => {
  if (isWelcomeCardLeaving.value) {
    return 'slide-out-top'
  } else if (!isRoomJoined.value && isWelcomeCardEntering.value) {
    // This condition might need adjustment based on handleLeaveChat logic
    // Ensure 'scale-in-center' is applied when returning from chat
    return 'scale-in-center'
  }
  return ''
})

const chatTransitionClass = computed(() => {
  if (isChatLeaving.value) {
    return 'slide-out-bottom'
  } else if (isRoomJoined.value && isChatEntering.value) {
    return 'scale-in-center'
  }
  return ''
})

const getWebSocketServer = () => {
  if (window.location.host === "mazeral.github.io") {
    return "wss://conventional-jenine-gigaorga-4011379f.koyeb.app/";
  } else if (window.location.host === "localhost:5173") {
    return "ws://localhost:8001/";
  } else {
    throw new Error(`Unsupported host: ${window.location.host}`);
  }
}

// Hanlding WebSocket connections with a single source of truth
const connectWebSocket = (roomIdToSend, userNameToSend, action) => {
  websocket.value = new WebSocket(getWebSocketServer())
  websocket.value.onopen = () => {
    websocket.value.send(
      JSON.stringify({
        action: action, // Include the action type
        room_id: roomIdToSend,
        username: userNameToSend,
      }),
    )
  }

  // Handles disconnections:
  websocket.value.onclose = (event) => {
    console.log(`Disconnected from the webocket server: ${event.reason}`)
    isRoomJoined.value = false
  }

  websocket.value.onerror = (error) => {
    console.error(`Error: ${error.message}`)
  }

  // handling messages
  websocket.value.onmessage = (event) => {
    try {
      console.log('the event:')
      console.log(event)
      const data = JSON.parse(event.data)
      console.log('App.vue: Received message:', data)

      switch (data.type) {
        case 'success':
          console.log(`Success: ${data.message}`, data)
          if (data.room_id) {
            roomId.value = data.room_id

            // Use the presence of room_id to determine transition
            notificationMessage.value = `Joined A Room With ID: ${data.room_id}`
            showNotification.value = true
            startTransitionToChat(data.room_id)
            notificationType.value = 'success'
          }
          break

        case 'error':
          console.error(`App.vue: Server error: ${data.message}`)
          notificationMessage.value = `Error: ${data.message}`
          showNotification.value = true
          // Reset roomId if join failed
          if (data.action === 'join') {
            roomId.value = ''
          }
          notificationType.value = 'error'
          break

        case 'message':
          if (data.content && data.username) {
            const isOwnMessage = data.username === userName.value

            // Check if we already have this message
            const existingIndex = messages.value.findIndex((m) => m.id === data.message_id)

            if (existingIndex > -1) {
              // Update existing message status
              messages.value[existingIndex].status = isOwnMessage ? 'delivered' : 'received'
            } else {
              // Add new message with proper type and status
              messages.value.push({
                id: data.message_id,
                content: data.content,
                userName: data.username,
                type: isOwnMessage ? 'sent' : 'received',
                status: isOwnMessage ? 'sending' : 'received',
              })

              // Send receipt for received messages only
              if (!isOwnMessage) {
                websocket.value.send(
                  JSON.stringify({
                    action: 'received',
                    message_id: data.message_id,
                    room_id: roomId.value,
                    username: userName.value,
                  }),
                )
              }
            }
          }
          break

        // In your WebSocket message handler:
        case 'user_joined':
          console.log(`App.vue: User joined: ${data.username}`)
          // Add simple system message without type checking
          messages.value.push({
            id: Date.now() + Math.random(),
            content: `${data.username} joined the room`,
          })
		  if (data.members)
			  messages.value.push({
				id: Date.now() + Math.random(),
				content: `Current users: ${data.members}`,
			  })
          break

        case 'user_left':
          console.log(`App.vue: User left: ${data.username}`)
          messages.value.push({
            id: Date.now() + Math.random(),
            content: `${data.username} left the room`,
          })
          break
        default:
          console.log('App.vue: Received unhandled message type:', data)
      }
    } catch (error) {
      console.error('App.vue: Error parsing message:', error, event.data)
    }
  }
}

// Helper function:
const sendWsMessage = async (messageContent) => {
  const messageId = `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`

  messages.value.push({
    id: messageId,
    content: messageContent,
    userName: userName.value,
    type: 'sent',
    status: 'sending', // Starts as sending
  })

  if (websocket.value?.readyState === WebSocket.OPEN) {
    websocket.value.send(
      JSON.stringify({
        action: 'send',
        message: messageContent,
        message_id: messageId,
        room_id: roomId.value,
        username: userName.value,
      }),
    )

    // Optimistically update to sent status
    const sentMessage = messages.value.find((m) => m.id === messageId)
    if (sentMessage) sentMessage.status = 'sent'
  }
}

const handleJoinRoom = (receivedRoomId) => {
  roomId.value = receivedRoomId
  connectWebSocket(receivedRoomId, userName.value, 'join') // Add action
  startTransitionToChat(receivedRoomId)
}

const startTransitionToChat = (newRoomId) => {
  console.log(`transitioning to the room`)
  isWelcomeCardLeaving.value = true
  setTimeout(() => {
    isWelcomeCardLeaving.value = false
    isRoomJoined.value = true
    isChatEntering.value = true
    resetChatEnter()
  }, 500)
}

// --- Watchers (Keep for resetting animation flags, review logic if needed) ---
// This logic might need adjustment based on the new animation flow
onMounted(() => {
  // Initial setup handled by ref defaults now
  // Ensure the initial animation flag is reset
  resetWelcomeCardEnter()
})

// // Reset enter animation flags after the animation duration - These might be redundant now
const resetWelcomeCardEnter = () => {
  setTimeout(() => {
    isWelcomeCardEntering.value = false
  }, 500) // Duration of scale-in-center
}

const handleRoomSuccess = (data) => {
  roomId.value = data.room_id
  notificationMessage.value = `Room ${data.action}: ${data.room_id}`
  showNotification.value = true
  console.log(`starting transitioning in handleRoomSuccess function`)
  startTransitionToChat(data.room_id)
}

const resetChatEnter = () => {
  setTimeout(() => {
    isChatEntering.value = false
  }, 500) // Duration of scale-in-center
}

watch(
  () => !isRoomJoined.value,
  (newValue, oldValue) => {
    // Trigger enter animation only when transitioning from chat back to welcome
    if (newValue && !oldValue) {
      isWelcomeCardEntering.value = true
      resetWelcomeCardEnter()
    }
  },
)

watch(
  () => isRoomJoined.value,
  (newValue, oldValue) => {
    // Trigger enter animation only when transitioning from welcome to chat
    if (newValue && !oldValue) {
      // isChatEntering handled within the event handlers now
      resetChatEnter()
    }
  },
)

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

.notification.success {
  background-color: #4caf50; /* Green */
}

.notification.error {
  background-color: #f44336; /* Red */
}

/* Add these media queries */
@media (max-width: 768px) {
  .content-container {
    padding-top: 10px;
  }

  .notification {
	  z-index: 10; /* Higher than notification */
	  top: 10px; /* Adjusted from -60px */
  }

  .close-button svg {
    width: 16px;
    height: 16px;
  }
}
/* Add to global styles in App.vue */
@media (max-width: 768px) {
  input {
    -webkit-appearance: none; /* Remove iOS styling */
    border-radius: 8px; /* Consistent border radius */
    border: 1px solid #ccc; /* Visible border */
    background: rgba(255, 255, 255, 0.9); /* Better contrast */
  }

  input:focus {
    outline: none;
    border-color: #93a8ac; /* Match your theme */
    box-shadow: 0 0 0 2px rgba(147, 168, 172, 0.3); /* Focus indicator */
  }
}
</style>
