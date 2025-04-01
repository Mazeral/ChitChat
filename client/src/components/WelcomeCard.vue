<template>
  <div class="e-card-wrapper">
    <div class="e-card playing">
      <div class="wave"></div>
      <div class="wave"></div>
      <div class="wave"></div>

      <div class="infotop">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="icon">
          <path
            fill="currentColor"
            d="M19.4133 4.89862L14.5863 2.17544C12.9911 1.27485 11.0089 1.27485 9.41368 2.17544L4.58674 4.89862C2.99153 5.7992 2 7.47596 2 9.2763V14.7235C2 16.5238 2.99153 18.2014 4.58674 19.1012L9.41368 21.8252C10.2079 22.2734 11.105 22.5 12.0046 22.5C12.6952 22.5 13.3874 22.3657 14.0349 22.0954C14.2204 22.018 14.4059 21.9273 14.5872 21.8252L19.4141 19.1012C19.9765 18.7831 20.4655 18.3728 20.8651 17.8825C21.597 16.9894 22 15.8671 22 14.7243V9.27713C22 7.47678 21.0085 5.7992 19.4133 4.89862ZM4.10784 14.7235V9.2763C4.10784 8.20928 4.6955 7.21559 5.64066 6.68166L10.4676 3.95848C10.9398 3.69152 11.4701 3.55804 11.9996 3.55804C12.5291 3.55804 13.0594 3.69152 13.5324 3.95848L18.3593 6.68166C19.3045 7.21476 19.8922 8.20928 19.8922 9.2763V9.75997C19.1426 9.60836 18.377 9.53091 17.6022 9.53091C14.7929 9.53091 12.1041 10.5501 10.0309 12.3999C8.36735 13.8847 7.21142 15.8012 6.68783 17.9081L5.63981 17.3165C4.69466 16.7834 4.10699 15.7897 4.10699 14.7235H4.10784ZM10.4676 20.0413L8.60933 18.9924C8.94996 17.0479 9.94402 15.2665 11.4515 13.921C13.1353 12.4181 15.3198 11.5908 17.6022 11.5908C18.3804 11.5908 19.1477 11.6864 19.8922 11.8742V14.7235C19.8922 15.2278 19.7589 15.7254 19.5119 16.1662C18.7615 15.3596 17.6806 14.8528 16.4783 14.8528C14.2136 14.8528 12.3781 16.6466 12.3781 18.8598C12.3781 19.3937 12.4861 19.9021 12.68 20.3676C11.9347 20.5316 11.1396 20.4203 10.4684 20.0413H10.4676Z"
          ></path></svg
        ><br />
        UI / EX Designer
        <br />
        <div class="name">MikeAndrewDesigner</div>
      </div>
    </div>
  </div>
</template>

<script setup>
// No script changes needed for this CSS-based solution
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
</style>
