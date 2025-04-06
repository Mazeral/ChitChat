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
		@mark-seen="handleMarkSeen"
      :userName="userName"
      :messages="messages"
      :class="chatTransitionClass"
      :roomId="roomId"
    />
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

// Function to handle the event when the user submits their name
const handleJoinedChat = (name) => {
  userName.value = name
  console.log('handleJoinedChat (name submitted) called with name:', name)
}

const handleLeaveChat = () => {
  isChatLeaving.value = true // Start the chat exit animation

  // Wait for the chat exit animation to complete (0.5s)
  setTimeout(() => {
    isRoomJoined.value = false // Now remove the Chat component from the DOM

    // Immediately trigger the WelcomeCard enter animation
    isWelcomeCardEntering.value = true
    messages.value = []

    // Reset the WelcomeCard enter animation flag after it plays
    setTimeout(() => {
      isWelcomeCardEntering.value = false
    }, 500) // Duration of welcome card enter animation

    isChatLeaving.value = false // Reset chat leaving flag
  }, 500) // Duration of chat exit animation
  console.log('handleLeaveChat called')
}

const handleRoomCreated = ({ roomId: newRoomId, userName: creatorName }) => {
  roomId.value = newRoomId
  console.log(`handleRoomCreated called with roomId: ${newRoomId}, userName: ${creatorName}`)
  console.log(
    `Current roomId ref value: ${roomId.value}, current userName ref value: ${userName.value}`,
  )
  connectWebSocket(newRoomId, creatorName, 'create')
  console.log(`After connectWebSocket call in handleRoomCreated`)
  startTransitionToChat(newRoomId)
}

const handleRoomJoined = ({ roomId: joinRoomId, userName: participantName }) => {
  roomId.value = joinRoomId
  console.log(`handleRoomJoined called with roomId: ${joinRoomId}, userName: ${participantName}`)
  console.log(
    `Current roomId ref value: ${roomId.value}, current userName ref value: ${userName.value}`,
  )
  connectWebSocket(joinRoomId, participantName, 'join')
  console.log(`After connectWebSocket call in handleRoomJoined`)
  startTransitionToChat(joinRoomId)
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

// Hanlding WebSocket connections with a single source of truth
const connectWebSocket = (roomIdToSend, userNameToSend, actionType) => {
  // Ensures only one connection for each client
  if (websocket.value && websocket.value.readyState === WebSocket.OPEN) {
    console.log(`WebSocket already open`)
    // If the connection is open, send the action immediately
    websocket.value?.send(
      JSON.stringify({
        action: actionType,
        room_id: roomIdToSend,
        username: userNameToSend,
      }),
    )
    return // Exit the function as the message is sent
  }

  // Creates a connection if there's none or not open
  websocket.value = new WebSocket('ws://localhost:8765')
  websocket.value.onopen = () => {
    console.log(`Connection has been made`)
    websocket.value?.send(
      JSON.stringify({
        action: actionType,
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
        case 'success': // Handle Join/Create Success
          console.log(`App.vue: ${data.message}`)
          roomId.value = data.room_id
          notificationMessage.value = `Room ${data.action === 'create' ? 'created' : 'joined'}: ${data.room_id}`
          showNotification.value = true
          console.log('Success: notificationMessage.value:', notificationMessage.value)
          console.log('Success: showNotification.value:', showNotification.value)
          startTransitionToChat()
          break

        case 'error':
          console.error(`App.vue: Server error: ${data.message}`)
          notificationMessage.value = `Error: ${data.message}`
          showNotification.value = true
          break

        case 'message':
          if (data.content && data.username) {
            messages.value.push({
              id: Date.now() + Math.random(),
              userName: data.username,
              content: data.content,
              type: data.username === userName.value ? 'sent' : 'received',
            })
          }
          break

        case 'user_joined':
          console.log(`App.vue: User joined: ${data.username}`)
          messages.value.push({
            id: Date.now() + Math.random(),
            type: 'system',
            content: `${data.username} joined the room.`,
          })
          break

        case 'user_left':
          console.log(`App.vue: User left: ${data.username}`)
          messages.value.push({
            id: Date.now() + Math.random(),
            type: 'system',
            content: `${data.username} left the room.`,
          })
          break
        case 'room-created':
        case 'room-joined':
          handleRoomSuccess(data)
          break
		case 'message_ack':
			const ackedMessage = messages.value.find(m => m.id === data.message_id);
			if (ackedMessage) ackedMessage.status = 'delivered';
			break;
		case 'message_seen':
			const seenMessage = messages.value.find(m => m.id === data.message_id);
			if (seenMessage) seenMessage.status = 'seen';
			break;

        default:
          console.log('App.vue: Received unhandled message type:', data)
      }
    } catch (error) {
      console.error('App.vue: Error parsing message:', error, event.data)
    }
  }
}

// Helper function:
const sendWsMessage = (messageContent) => {
    const messageId = `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
    
    messages.value.push({
        id: messageId,
        content: messageContent,
        userName: userName.value,
        type: 'sent',
        status: 'sending'
    });

    if (websocket.value?.readyState === WebSocket.OPEN) {
        websocket.value.send(JSON.stringify({
            action: 'send',
            message: messageContent,
            message_id: messageId
        }));
        // Optimistically update to sent status
        const sentMessage = messages.value.find(m => m.id === messageId);
        if (sentMessage) sentMessage.status = 'sent';
    }
};

// Add mark seen handler
const handleMarkSeen = (messageIds) => {
    if (websocket.value?.readyState === WebSocket.OPEN) {
        websocket.value.send(JSON.stringify({
            action: "mark_seen",
            message_ids: messageIds
        }));
    }
};

const handleJoinRoom = (receivedRoomId) => {
  roomId.value = receivedRoomId
  connectWebSocket(receivedRoomId, userName.value, 'join')
  // Reuse the same transition logic as room creation
  startTransitionToChat(receivedRoomId)
}

const startTransitionToChat = (newRoomId) => {
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
</style>
