<template>
  <div class="e-card-wrapper">
    <div class="e-card playing">
      <div class="wave"></div>
      <div class="wave"></div>
      <div class="wave"></div>

      <div
        v-if="!nameEntered"
        ref="infotopElement"
        class="infotop"
        :class="{
          'fade-in': shouldFadeInWelcome,
          'slide-out-left': isSlidingFromName,
        }"
      >
        <h1>Welcome To ChitChat!</h1>
        <input type="text" v-model="nameInput" placeholder="Enter Your Name" />
        <button @click.prevent="submitName" :disabled="!nameInput">Enter</button>
      </div>

      <div
        v-if="nameEntered && !joiningRoom"
        class="infotop"
        :class="{
          'fade-in': showOptions,
          'slide-out-left': isSlidingFromOptionsToJoin,
          'slide-out-right': shouldSlideOutToName,
        }"
      >
        <h1>Welcome {{ userName }}!</h1>
        <button @click.prevent="handleJoinRoom">Join A Room</button>
        <span> or </span>
        <button @click.prevent="createRoom">Create A Room</button>
        <button @click.prevent="goBackToName">Back</button>
      </div>

      <div
        v-if="nameEntered && joiningRoom"
        class="infotop"
        :class="{
          'fade-in': showJoinRoomInfo,
          'slide-out-right': isSlidingFromJoinToOptions,
        }"
      >
        <h1>Enter Room ID</h1>
        <input v-model="roomToJoin" type="text" placeholder="Room ID" />
        <button @click.prevent="joinRoom">Enter</button>
        <button @click.prevent="goBack">Back</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, defineEmits } from 'vue'

const emit = defineEmits(['joined-chat', 'room-created', 'name-submitted'])
const nameEntered = ref(false)
const nameInput = ref('')
const userName = ref('')
const joiningRoom = ref(false)
const showOptions = ref(false)
const showJoinRoomInfo = ref(false)
const shouldFadeInWelcome = ref(false)
const infotopElement = ref(null)
const isSlidingFromName = ref(false)
const isSlidingFromOptionsToJoin = ref(false)
const shouldSlideOutToName = ref(false)
const isSlidingFromJoinToOptions = ref(false)
const roomToJoin = ref('')
const currentRoomId = ref('')

onMounted(() => {
  setTimeout(() => {
    shouldFadeInWelcome.value = true // Fade in on initial load
  }, 100) // Small delay to ensure class is applied
})

const submitName = async () => {
  userName.value = nameInput.value
  isSlidingFromName.value = true
  await new Promise((resolve) => setTimeout(resolve, 1000))
  nameEntered.value = true
  showOptions.value = true
  isSlidingFromName.value = false
  emit('name-submitted', userName.value)
  console.log('WelcomeCard: emit name-submitted', userName.value)
}

const handleJoinRoom = async () => {
  showOptions.value = false
  isSlidingFromOptionsToJoin.value = true
  await new Promise((resolve) => setTimeout(resolve, 1000))
  joiningRoom.value = true
  showJoinRoomInfo.value = true
  isSlidingFromOptionsToJoin.value = false
  // emit('joined-chat'); // Remove this line
}

const goBack = async () => {
  showJoinRoomInfo.value = false
  isSlidingFromJoinToOptions.value = true
  await new Promise((resolve) => setTimeout(resolve, 750))
  joiningRoom.value = false
  showOptions.value = true
  isSlidingFromJoinToOptions.value = false
}

const goBackToName = async () => {
  showOptions.value = false
  shouldSlideOutToName.value = true
  await new Promise((resolve) => setTimeout(resolve, 750))
  nameEntered.value = false
  shouldFadeInWelcome.value = true
  shouldSlideOutToName.value = false
}

// a function to create the room id
function generateRandomAlphanumericWordSimple() {
  const possibleChars = 'abcdefghijklmnopqrstuvwxyz0123456789'
  return Array.from({ length: 4 }, () => {
    const randomIndex = Math.floor(Math.random() * possibleChars.length)
    return possibleChars[randomIndex]
  }).join('')
}

const websocket = new WebSocket('ws://localhost:8765')
// Checking if the connection was made
websocket.onopen = () => {
  console.log('Connection to the server has been established')
}

websocket.onclose = () => {
  console.log('Connection to the server has been closed')
}

// Helper function to make communication easier
const sendMessage = (action, data) => {
  if (websocket.readyState === WebSocket.OPEN) {
    websocket.send(JSON.stringify({ action, ...data }))
  } else {
    console.error('WebSocket connection is not open.')
  }
}

websocket.onmessage = (event) => {
  try {
    const data = JSON.parse(event.data)
    console.log('Received response in WelcomeCard:', data)

    switch (data.type) {
      case 'error':
        console.error('Join failed:', data.message)
        if (data.message === "Room doesn't exist") {
          // Optionally update the UI to show "Room doesn't exist" error
          console.log("Displaying 'Room doesn't exist' error to the user.")
        } else if (data.message === 'Missing room_id for join action') {
          console.log("Displaying 'Room ID required' error.")
        } else if (
          data.message === 'Missing username for join action' ||
          data.message === 'Missing username for create action'
        ) {
          console.log('Username is required.')
        } else if (data.message === 'Room already exists') {
          console.log('Room already exists.')
        } else {
          // Handle other potential errors
          console.log('Other error:', data.message)
        }
        break
      case 'success':
        console.log(`${data.message}`)
        const roomId = data.room_id
        currentRoomId.value = roomId
        console.log('Emitting room-created event with ID:', roomId)
        emit('room-created', roomId) // Emit the event with the room ID
        emit('joined-chat') // Emit the event to transition to chat
        break
      case 'user_joined':
        // This is typically for other users joining, the 'success' handles the current user
        console.log('Another user joined:', data.username)
        break
      default:
        console.log('Received unknown message type:', data)
        break
    }
  } catch (error) {
    console.error('Error parsing message:', error)
  }
}

const createRoom = () => {
  const room = generateRandomAlphanumericWordSimple()
  sendMessage('create', { room_id: room, username: userName.value })
  console.log(`created a room with ID: ${room}`)
}

const joinRoom = () => {
  if (roomToJoin.value) {
    currentRoomId.value = roomToJoin.value // for debugging
    console.log(`Attempting to join room: ${roomToJoin.value} with username: ${userName.value}`)
    sendMessage('join', { room_id: roomToJoin.value, username: userName.value })
  } else {
    console.log('Room ID cannot be empty!')
  }
}
</script>

<style scoped>
/* Optional wrapper to center the card */
.e-card-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 50px; /* Add padding if needed */
  min-height: 100vh; /* Example height */
  box-sizing: border-box;
  position: relative; /* To position the notification */
}

<style scoped>
/* Optional wrapper to center the card */
.e-card-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 50px; /* Add padding if needed */
  min-height: 100vh; /* Example height */
  box-sizing: border-box;
}

.e-card {
  /* --- CSS Variables for Dynamic Sizing --- */
  /* Modify these values to change the card size */
  --card-width: 80vh;
  --card-height: 80vh;

  /* Ratios for wave size relative to card size */
  /* Adjust if waves don't cover enough/too much on resize */
  --wave-width-ratio: 2.25; /* Approx 540 / 240 */
  --wave-height-ratio: 2.15; /* Approx 700 / 330 */

  /* Position for lower waves relative to card height */
  --wave-top-offset-ratio: 0.63; /* Approx 210 / 330 */
  /* Position for info section relative to card height */
  --info-top-ratio: 0.34; /* Approx 112 / 330 (based on original 5.6em * 20px) */

  /* --- Basic Card Styles --- */
  position: relative;
  width: var(--card-width);
  height: var(--card-height);
  /* margin: 100px auto; Remove fixed margin if using wrapper */
  background: transparent; /* Or use background-color if needed */
  border-radius: 16px; /* Consider making radius dynamic too, e.g., calc(var(--card-width) * 0.07) */
  box-shadow: 0px 8px 28px -9px rgba(0, 0, 0, 0.45);
  overflow: hidden; /* Keeps waves contained */
}

.wave {
  /* --- Wave Element Styles --- */
  position: absolute;
  /* Calculate wave dimensions based on card size and ratios */
  width: calc(var(--card-width) * var(--wave-width-ratio));
  height: calc(var(--card-height) * var(--wave-height-ratio));
  left: 0;
  top: 0; /* Default top position */
  /* Margins position the large wave's center roughly over the card's center */
  /* Using percentages relative to the wave's own size */
  margin-left: -50%;
  margin-top: -70%;
  background: linear-gradient(744deg, #2b59c3, #93a8ac 60%, #2b59c3);
  opacity: 0.6;
  border-radius: 40%; /* This keeps the oval shape */
  /* Default animation state (non-playing) */
  animation: wave 55s infinite linear;
  z-index: -1;
}

/* Position the second and third wave divs lower */
/* Use calculation based on card height */
.wave:nth-child(1), /* First visible wave */
.wave:nth-child(2) {
  /* Second visible wave */
  top: calc(var(--card-height) * var(--wave-top-offset-ratio));
}

/* Adjust animation duration for the second visible wave */
.wave:nth-child(1) {
  animation-duration: 50s;
}

/* Adjust animation duration for the third visible wave */
.wave:nth-child(2) {
  animation-duration: 45s;
}

/* --- Playing State Overrides --- */

/* Faster animation for all waves when .playing */
.playing .wave {
  animation-duration: 3000ms; /* Keep base faster speed */
}

/* Faster specific duration for the second visible wave when .playing */
.playing .wave:nth-child(1) {
  animation-duration: 4000ms;
}

/* Faster specific duration for the third visible wave when .playing */
.playing .wave:nth-child(2) {
  animation-duration: 5000ms;
}

/* --- Info Section Styles --- */

.infotop {
  position: absolute;
  /* Position relative to card height */
  top: calc(var(--card-height) * var(--info-top-ratio));
  left: 0;
  right: 0;
  padding: 0 10px; /* Add some padding to prevent text touching edges */
  box-sizing: border-box; /* Include padding in width calculation */
  text-align: center;
  /* Base font size - could also be made dynamic e.g. using vw or calc */
  font-size: 20px;
  color: rgb(255, 255, 255);
  font-weight: 600;
  z-index: 4; /* Ensure text is above waves */
  opacity: 0; /* Initially hide the content */
}

.infotop h1 {
  text-align: center;
  color: white;
  opacity: 1;
  background-color: transparent;
}

.infotop input[type='text'] {
  padding: 10px;
  margin: 15px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.infotop button {
  --color: #f5f5f5;
  font-family: inherit;
  display: inline-block;
  width: 8em;
  height: 2.6em;
  line-height: 2.5em;
  margin: 10px;
  position: relative;
  cursor: pointer;
  overflow: hidden;
  border: 2px solid #93a8ac;
  transition: color 0.5s;
  z-index: 1;
  font-size: 17px;
  font-weight: bold;
  text-shadow: horizontal-offset horizontal-offset blur-radius color;
  border-radius: 6px;
  color: var(--color);
  background-color: transparent;
}

.infotop button:before {
  content: '';
  position: absolute;
  z-index: -1;
  background: var(--color);
  height: 150px;
  width: 200px;
  border-radius: 50%;
}

.infotop button:hover {
  color: #93a8ac;
}

.infotop button:before {
  top: 100%;
  left: 100%;
  transition: all 0.7s;
}

.infotop button:hover:before {
  top: -30px;
  left: -30px;
}

.infotop button:active:before {
  background: #2b59c3;
  transition: background 0s;
}

.fade-in {
  animation: fade-in 0.5s ease-out both; /* Use animation instead of transition */
  opacity: 1;
}

@keyframes fade-in {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes wave {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.slide-out-left {
  -webkit-animation: slide-out-left 1s cubic-bezier(0.55, 0.085, 0.68, 0.53) both;
  animation: slide-out-left 1s cubic-bezier(0.55, 0.085, 0.68, 0.53) both;
}

@-webkit-keyframes slide-out-left {
  0% {
    -webkit-transform: translateX(0);
    transform: translateX(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: translateX(-1000px);
    transform: translateX(-1000px);
    opacity: 0;
  }
}
@keyframes slide-out-left {
  0% {
    -webkit-transform: translateX(0);
    transform: translateX(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: translateX(-1000px);
    transform: translateX(-1000px);
    opacity: 0;
  }
}
.slide-out-right {
  -webkit-animation: slide-out-right 1s cubic-bezier(0.55, 0.085, 0.68, 0.53) both;
  animation: slide-out-right 1s cubic-bezier(0.55, 0.085, 0.68, 0.53) both;
}

@-webkit-keyframes slide-out-right {
  0% {
    -webkit-transform: translateX(0);
    transform: translateX(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: translateX(1000px);
    transform: translateX(1000px);
    opacity: 0;
  }
}
@keyframes slide-out-right {
  0% {
    -webkit-transform: translateX(0);
    transform: translateX(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: translateX(1000px);
    transform: translateX(1000px);
    opacity: 0;
  }
}
</style>
