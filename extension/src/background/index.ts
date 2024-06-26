const generateVideo = (text: string): Promise<{ videoPath: string } | { error: string }> => {
  return fetch('http://localhost:8000/generate_video', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text, style: "default" }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.videoPath) {
        console.log('in background script Video path:', data.videoPath);
        return { videoPath: data.videoPath };
      } else {
        throw new Error('Video path not found in the response');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      return { error: 'Failed to generate video' };
    });
};

if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.onMessage) {
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'generateVideo') {
      generateVideo(request.text)
        .then(sendResponse);
      return true; // Indicates that the response is sent asynchronously
    }
  });
}

export { generateVideo };