<template>
  <div class="chat-container">
    <ul class="chat-messages">
      <li class="received">this text is for testing the chat property correctly</li>
      <li class="sent">this text is for a sent message</li>
      <li class="received">another received message</li>
      <li class="sent">this is another message I sent</li>
      <li class="received">this text is for testing the chat property correctly</li>
      <li class="received">this text is for testing the chat property correctly</li>
      <li class="received">this text is for testing the chat property correctly</li>
      <li class="received">this text is for testing the chat property correctly</li>
    </ul>
    <div class="messageBox">
      <input required="" placeholder="Message..." type="text" id="messageInput" />
      <button id="sendButton">
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

<script setup></script>

<style scoped>
.chat-container { /* New style for the parent */
  display: flex;
  flex-direction: column;
  align-items: center; /* This will center children horizontally */
}
.chat-messages {
width: 90%;
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 15px;
  margin: 0 auto;
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
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
  width: fit-content;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255,255,255,0.1);
  padding: 0 15px;
  border-radius: 10px;
  border: 1px solid white;
}

.messageBox:focus-within {
  border: 1px solid #00ccff;
}
#messageInput {
  width: 200px;
  height: 100%;
  background-color: transparent;
  outline: none;
  border: none;
  padding-left: 10px;
  color: white;
}
#messageInput::placeholder{
	color: white;
	
}
#messageInput:focus ~ #sendButton svg path,
#messageInput:valid ~ #sendButton svg path {
  fill: #6655ff;
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
}
#sendButton svg {
  height: 18px;
  transition: all 0.3s;
}
#sendButton svg path {
  transition: all 0.3s;
}
#sendButton:hover svg path {
  fill: #6655ff;
  stroke: white;
}
</style>
