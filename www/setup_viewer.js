// Check if the device is mobile so that the mobile CSS can be loaded.
const mobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
if (mobileDevice) {
  const head = document.getElementsByTagName('head')[0];
  const mobileCss = document.createElement('link');
  mobileCss.setAttribute('rel', 'stylesheet');
  mobileCss.setAttribute('type', 'text/css');
  mobileCss.setAttribute('href', 'https://www.cyberbotics.com/wwi/R2023b/css/wwi_mobile.css');
  head.appendChild(mobileCss);
}

/**
 * Automatically connect to the WebSocket on page load.
 * The Webots view is set to use the "x3d" streaming mode.
 */
function autoConnect() {
  const defaultThumbnail = 'https://cyberbotics.com/wwi/R2023b/images/loading/default_thumbnail.png';
  const streamingMode = "x3d"; // Streaming mode set to "x3d" as requested.
  const webotsView = document.getElementsByTagName('webots-view')[0];

  // Set event handlers (if needed, you can customize these further)
  webotsView.onready = onConnect;
  webotsView.ondisconnect = onDisconnect;

  // Connect to the WebSocket (adjust the URL if necessary)
  webotsView.connect("ws://localhost:1234", streamingMode, false, mobileDevice, -1, defaultThumbnail);
}

function onConnect() {
  console.log("Webots view connected.");
  // You may add further actions on connect here.
}

function onDisconnect() {
  console.log("Webots view disconnected.");
  // You may add further actions on disconnect here.
}

// Set up the page once it loads.
window.addEventListener('load', function() {
  // Automatically connect the Webots view.
  autoConnect();

  // Set up the "Send" button behavior.
  const sendButton = document.getElementById('sendButton');
  const bigInput = document.getElementById('bigInput');

  sendButton.onclick = function() {
    const text = bigInput.value;
    console.log("Send button clicked with text:", text);
  
    // Send a POST request to the /api/sendCommand endpoint with the instruction.
    fetch("/api/sendCommand", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ instruction: text })
    })
    .then(response => response.json())
    .then(data => {
      console.log("Response from server:", data);
      // You can handle the response further here.
    })
    .catch(error => {
      console.error("Error:", error);
    });
  };
});