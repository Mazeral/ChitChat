# ChitChat - Real-Time WebSocket Chat Application

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/badge/Vue.js-3.x-brightgreen?style=flat-square" alt="Vue.js Version">
  <img src="https://img.shields.io/badge/WebSockets-RealTime-red?style=flat-square" alt="WebSocket Support">
</p>

## Overview
ChitChat is a real-time chat application that allows users to:
- Create/join chat rooms
- Send messages with status tracking (sent/delivered)
- See real-time user presence updates
- Enjoy smooth UI animations and transitions
- Use on both desktop and mobile devices

The application uses a Vue.js frontend with WebSocket communication to a Python backend server.

## Features
✨ **Key Features** ✨
- Real-time messaging with WebSocket
- Room creation/joining system
- User presence notifications (join/leave)
- Message status indicators:
  - ⏳ Sending
  - ✅ Sent
  - ✅✅ Delivered
- Smooth CSS animations for UI transitions
- Responsive design for mobile devices
- Error handling and notifications
- Automatic room cleanup when empty

## Tech Stack
**Frontend:**
- Vue.js 3 (Composition API)
- WebSocket Client
- CSS Animations
- Responsive Design

**Backend:**
- Python 3.8+
- `websockets` library
- AsyncIO for concurrency
- In-memory room/message management

## Installation & Setup

### Backend Server
```bash
# Clone the repository
git clone https://github.com/your-repo/chitchat.git
cd chitchat/backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

### Frontend Application
```bash
# Navigate to frontend directory
cd chitchat/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## Usage
1. **Create a Room:**
   - Enter your name on the welcome screen
   - Click "Create A Room" to generate a unique room ID
   - Share the room ID with others

2. **Join a Room:**
   - Enter your name on the welcome screen
   - Click "Join A Room" and enter the room ID
   - Start chatting immediately

3. **Messaging:**
   - Type messages in the input box
   - Press Enter or click the send button
   - Track message status in real-time

4. **Mobile Support:**
   - The UI automatically adapts to mobile screens
   - Touch-friendly interface elements

## Project Structure
```
chitchat/
├── backend/
│   └── server.py      # WebSocket server with room management
├── frontend/
│   ├── src/
│   │   ├── assets/    # Background images and icons
│   │   ├── components/
│   │   │   ├── Chat.vue        # Chat interface component
│   │   │   └── WelcomeCard.vue # Entry/welcome screen
│   │   └── App.vue    # Main application component
│   └── package.json   # Frontend dependencies
└── README.md
```

## Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## Acknowledgments
- WebSocket protocol documentation
- Vue.js official documentation
- Animista.net for CSS animations
- SVGRepo for icons
