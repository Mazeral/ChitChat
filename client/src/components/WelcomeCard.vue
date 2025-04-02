<template>
  <div class="e-card-wrapper" :class="{ 'slide-out-left': shouldSlideOut }">
    <div class="e-card playing">
      <div class="wave"></div>
      <div class="wave"></div>
      <div class="wave"></div>
      <div class="infotop">
        <h1>Welcome To ChitChat!</h1>
        <button>button 1</button>
        <button>button 2</button>
      </div>
    </div>
  </div>
</template>

<script setup></script>

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
  --card-width: 350px;
  --card-height: 500px;

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
  background: linear-gradient(744deg, #00cc99, #6655ff 60%, #00cc99);
  opacity: 0.6;
  border-radius: 40%; /* This keeps the oval shape */
  /* Default animation state (non-playing) */
  animation: wave 55s infinite linear;
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
  z-index: 1; /* Ensure text is above waves */
}

.icon {
  /* Size relative to infotop font-size */
  width: 3em;
  /* Vertical positioning relative to infotop font-size */
  margin-top: -1em;
  padding-bottom: 1em;
  /* Prevent icon from shrinking too much if container gets narrow */
  max-width: 100%;
  height: auto; /* Maintain aspect ratio */
}

.name {
  position: relative; /* Keep relative positioning */
  top: 1em; /* Position relative to text above */
  /* Font size relative to infotop font-size */
  font-size: 0.7em; /* Was 14px, now relative to 20px */
  font-weight: 100;
  text-transform: lowercase;
  /* Prevent long names from breaking layout badly */
  word-wrap: break-word;
}

/* --- Keyframes --- */

@keyframes wave {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

button {
  --color: #00ccff;
  font-family: inherit;
  display: inline-block;
  width: 8em;
  height: 2.6em;
  line-height: 2.5em;
  margin: 20px;
  position: relative;
  cursor: pointer;
  overflow: hidden;
  border: 2px solid #00ccff;
  transition: color 0.5s;
  z-index: 1;
  font-size: 17px;
  font-weight: bold;
  text-shadow: horizontal-offset vertical-offset blur-radius color;
  border-radius: 6px;
  color: var(--color);
  background-color: transparent;
}

button:before {
  content: '';
  position: absolute;
  z-index: -1;
  background: var(--color);
  height: 150px;
  width: 200px;
  border-radius: 50%;
}

button:hover {
  color: #fff;
}

button:before {
  top: 100%;
  left: 100%;
  transition: all 0.7s;
}

button:hover:before {
  top: -30px;
  left: -30px;
}

button:active:before {
  background: #6655ff;
  transition: background 0s;
}

h1 {
  text-align: center;
  color: white;
  z-index: 2;
  opacity: 1;
  background-color: transparent;
}

.slide-out-left {
  -webkit-animation: slide-out-left 1s ease-in both;
  animation: slide-out-left 1s ease-in both;
}

/* ----------------------------------------------
 * Generated by Animista on 2025-4-2 7:6:57
 * Licensed under FreeBSD License.
 * See http://animista.net/license for more info. 
 * w: http://animista.net, t: @cssanimista
 * ---------------------------------------------- */

/**
 * ----------------------------------------
 * animation slide-out-left
 * ----------------------------------------
 */
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
</style>
