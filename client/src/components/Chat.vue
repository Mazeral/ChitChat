<template>
  <div class="chat-container">
    <button class="leave-button noselect" @click.prevent="leave">
      <span class="text">Leave</span>
      <span class="icon">
        <svg
          fill="#ffffff"
          version="1.1"
          id="Capa_1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="-49.25 -49.25 591.00 591.00"
          xml:space="preserve"
          stroke="#ffffff"
        >
          <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g
            id="SVGRepo_tracerCarrier"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke="#CCCCCC"
            stroke-width="9.85"
          ></g>
          <g id="SVGRepo_iconCarrier">
            <g>
              <path
                d="M184.646,0v21.72H99.704v433.358h31.403V53.123h53.539V492.5l208.15-37.422v-61.235V37.5L184.646,0z M222.938,263.129 c-6.997,0-12.67-7.381-12.67-16.486c0-9.104,5.673-16.485,12.67-16.485s12.67,7.381,12.67,16.485 C235.608,255.748,229.935,263.129,222.938,263.129z"
              ></path>
            </g>
          </g>
        </svg>
      </span>
    </button>

    <ul class="chat-messages">
      <li class="received slide-in-left">
        <div class="username">User A</div>
        <div class="message-content">this text is for testing the chat property correctly</div>
      </li>
      <li class="sent slide-in-right">
        <div class="username">You</div>
        <div class="message-content">this text is for a sent message</div>
      </li>
      <li class="received slide-in-left">
        <div class="username">User B</div>
        <div class="message-content">another received message</div>
      </li>
      <li class="sent slide-in-right">
        <div class="username">You</div>
        <div class="message-content">this is another message I sent</div>
      </li>
      <li class="received slide-in-left">
        <div class="username">User C</div>
        <div class="message-content">this text is for testing the chat property correctly</div>
      </li>
      <li class="received slide-in-left">
        <div class="username">User A</div>
        <div class="message-content">this text is for testing the chat property correctly</div>
      </li>
      <li class="received slide-in-left">
        <div class="username">User D</div>
        <div class="message-content">this text is for testing the chat property correctly</div>
      </li>
      <li class="received slide-in-left">
        <div class="username">User B</div>
        <div class="message-content">this text is for testing the chat property correctly</div>
      </li>
      <li
        v-for="message in messages"
        :key="message.id"
        :class="[
          { received: message.type === 'received', sent: message.type === 'sent' },
          message.type === 'received' ? 'slide-in-left' : 'slide-in-right',
        ]"
      >
        <div class="username">{{ message.userName }}</div>
        <div class="message-content">{{ message.content }}</div>
      </li>
    </ul>
    <div class="messageBox">
      <input
        required=""
        placeholder="Message..."
        type="text"
        id="messageInput"
		v-model="messageInput"
        @keyup.enter="triggerSendMessage"
      />
      <button id="sendButton" @click="triggerSendMessage">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 664 663">
          <path
            fill="none"
            d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
          ></path>
          <path
            stroke-linejoin="round"
            stroke-linecap="round"
            stroke-width="33.67"
            stroke="#f5f5f5"
            d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
          ></path>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, defineProps, watch, nextTick, onMounted, onUpdated } from 'vue'

const emit = defineEmits(['leave-room', 'send-message'])
const props = defineProps({
  userName: String,
  messages: Array, // Receive messages from App.vue
  roomId: String,
})
const messageInput = ref('')
const messageList = ref([])

// To know if the required data is there
onMounted(() => {
  // console.log('Chat component mounted. User:', props.userName, 'Room:', props.roomId);
  scrollToBottom() // Scroll down on initial mount
})

// Scrolling to bottom with each new message
onUpdated(() => {
  scrollToBottom()
})

const scrollToBottom = () => {
  nextTick(() => {
    // Ensure DOM is updated before scrolling
    if (messageList.value) {
      messageList.value.scrollTop = messageList.value.scrollHeight
    }
  })
}

const triggerSendMessage = () => {
  console.log('triggerSendMessage function called');
  const content = messageInput.value.trim()
  console.log(content)
  if (content) {
    console.log('Emitting send-message with content:', content); // Add this line
    emit('send-message', content) // Emit only the message content
    messageInput.value = ''
  }
}

const leave = () => {
  emit('leave-room', props.roomId)
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 90%;
  margin: 20px auto; /* Centers horizontally and adds vertical spacing */
  position: relative;
  min-height: calc(100vh - 140px); /* Ensures container can scroll */
}

.chat-messages {
  /* --- MODIFIED --- */
  width: 100%; /* Make messages list take full width of chat-container */
  box-sizing: border-box; /* Include padding in width calculation */
  /* --- END MODIFIED --- */
  list-style: none;
  padding: 0;
  margin: 0;
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 15px;
  /* margin: 0 auto; Removed this */
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  margin-bottom: 15px; /* Added space between messages and input box */
  height: 400px; /* Example fixed height, adjust or make dynamic */
  overflow-y: auto; /* Add scroll for overflow */
  min-height: 400px;
  height: 60vh; /* Makes messages area responsive */
}

.chat-messages li {
  color: #333;
  padding: 12px 16px;
  border-radius: 18px;
  width: fit-content;
  max-width: 80%;
  word-break: break-word;
  position: relative;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-messages li.received {
  background-color: #f0f0f0;
  border-top-left-radius: 0;
}

.chat-messages li.sent {
  background-color: #dcf8c6;
  align-self: flex-end;
  border-top-right-radius: 0;
}

.messageBox {
  /* --- MODIFIED --- */
  width: 100%; /* Make input box span the full width of chat-container */
  box-sizing: border-box; /* Include padding in width calculation */
  /* --- END MODIFIED --- */
  height: 40px;
  display: flex;
  align-items: center;
  /* justify-content: center; Removed this */
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0 5px 0 15px; /* Adjusted padding */
  border-radius: 10px;
  border: 1px solid white;
  font-size: 30px;
}

.messageBox:focus-within {
  border: 1px solid #93a8ac;
}
#messageInput {
  /* --- MODIFIED --- */
  /* width: 200px; Removed fixed width */
  flex-grow: 1; /* Allow input to take available space */
  /* --- END MODIFIED --- */
  height: 100%;
  background-color: transparent;
  outline: none;
  border: none;
  padding-left: 10px;
  color: white;
  font-size: 20px;
}
#messageInput::placeholder {
  color: white;
}
#messageInput:focus ~ #sendButton svg path,
#messageInput:valid ~ #sendButton svg path {
  fill: #2b59c3;
  stroke: white;
}

#sendButton {
  width: fit-content;
  height: 100%;
  background-color: transparent;
  outline: none;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  padding: 0 10px; /* Added padding */
}
#sendButton svg {
  height: 18px;
  transition: all 0.3s;
}
#sendButton svg path {
  transition: all 0.3s;
}
#sendButton:hover svg path {
  fill: #2b59c3;
  stroke: white;
}

.leave-button {
  /* --- MODIFIED --- */
  position: absolute; /* Position relative to chat-container */
  top: -60px; /* Move above the container (negative height + margin) */
  right: 0; /* Align right edge with chat-container's right edge */
  /* margin-bottom: 10px; Removed margin, position handled by top/right */
  z-index: 10; /* Ensure it's above other elements if needed */
  /* --- END MODIFIED --- */
  width: 150px;
  height: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  background: #ff0000;
  border: none;
  border-radius: 5px;
  margin-top: 20px;
}

/* --- Rest of the leave-button styles remain the same --- */
.leave-button,
.leave-button span {
  transition: 200ms;
}

.leave-button .text {
  transform: translateX(35px);
  color: white;
  font-weight: bold;
}

.leave-button .icon {
  position: absolute;
  border-left: 1px solid #f5f5f5;
  transform: translateX(110px);
  height: 40px;
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.leave-button svg {
  width: 20px;
  fill: #eee;
}

.leave-button:hover {
  background: #ff4747;
  border-left: 1px solid #f5f5f5;
}

.leave-button:hover .text {
  color: transparent;
}

.leave-button:hover .icon {
  width: 150px;
  border-left: none;
  transform: translateX(0);
}

.leave-button:focus {
  outline: none;
}

.leave-button:active .icon svg {
  transform: scale(0.8);
}
/* Removed the .exit class as the wrapper div was removed */

.username {
  font-weight: bold;
  opacity: 0.8;
  font-style: italic;
}
.slide-in-right {
  -webkit-animation: slide-in-right 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  animation: slide-in-right 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}

/* ----------------------------------------------
 * Generated by Animista on 2025-4-4 7:30:48
 * Licensed under FreeBSD License.
 * See http://animista.net/license for more info. 
 * w: http://animista.net, t: @cssanimista
 * ---------------------------------------------- */

/**
 * ----------------------------------------
 * animation slide-in-right
 * ----------------------------------------
 */
@-webkit-keyframes slide-in-right {
  0% {
    -webkit-transform: translateX(1000px);
    transform: translateX(1000px);
    opacity: 0;
  }
  100% {
    -webkit-transform: translateX(0);
    transform: translateX(0);
    opacity: 1;
  }
}
@keyframes slide-in-right {
  0% {
    -webkit-transform: translateX(1000px);
    transform: translateX(1000px);
    opacity: 0;
  }
  100% {
    -webkit-transform: translateX(0);
    transform: translateX(0);
    opacity: 1;
  }
}
.slide-in-left {
  -webkit-animation: slide-in-left 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  animation: slide-in-left 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}

/* ----------------------------------------------
 * Generated by Animista on 2025-4-4 7:31:8
 * Licensed under FreeBSD License.
 * See http://animista.net/license for more info. 
 * w: http://animista.net, t: @cssanimista
 * ---------------------------------------------- */

/**
 * ----------------------------------------
 * animation slide-in-left
 * ----------------------------------------
 */
@-webkit-keyframes slide-in-left {
  0% {
    -webkit-transform: translateX(-1000px);
    transform: translateX(-1000px);
    opacity: 0;
  }
  100% {
    -webkit-transform: translateX(0);
    transform: translateX(0);
    opacity: 1;
  }
}
@keyframes slide-in-left {
  0% {
    -webkit-transform: translateX(-1000px);
    transform: translateX(-1000px);
    opacity: 0;
  }
  100% {
    -webkit-transform: translateX(0);
    transform: translateX(0);
    opacity: 1;
  }
}
/* Global scrollbar styles */
.chat-messages::-webkit-scrollbar {
  width: 8px; /* Width of the scrollbar */
}

.chat-messages::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.1); /* Color of the track */
  border-radius: 10px; /* Rounded corners for the track */
}

.chat-messages::-webkit-scrollbar-thumb {
  background-color: #888; /* Color of the thumb */
  border-radius: 10px; /* Rounded corners for the thumb */
  border: 2px solid transparent; /* Add some padding/spacing */
  background-clip: padding-box; /* Make the border part of the padding */
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background-color: #555; /* Color of the thumb on hover */
}

/* Firefox global scrollbar styles */
.chat-messages {
  scrollbar-width: thin; /* Can be auto, thin, or none */
  scrollbar-color: #888 rgba(0, 0, 0, 0.1); /* thumb color track color */
}
</style>
