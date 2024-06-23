chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'generateVideo') {
      fetch('http://localhost:8000/generate_video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: request.text, style: "default" }),
      })
        .then(response => response.arrayBuffer())
        .then(buffer => {
          const base64 = btoa(String.fromCharCode.apply(null, Array.from(new Uint8Array(buffer))));
          sendResponse({ videoData: base64 });
        })
        .catch(error => {
          console.error('Error:', error);
          sendResponse({ error: 'Failed to generate video' });
        });
      return true; // Indicates that the response is sent asynchronously
    }
  });
  
  export {}; // Add this line to make the file a module