chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'openPopup') {
    chrome.windows.create({
      url: chrome.runtime.getURL('index.html'),
      type: 'popup',
      width: 400,
      height: 600
    }, (window) => {
      if (window && window.tabs && window.tabs[0] && window.tabs[0].id) {
        chrome.tabs.sendMessage(window.tabs[0].id, { action: 'setSelectedText', text: request.text });
      }
    });
  } else if (request.action === 'generateVideo') {
    generateVideo(request.text)
      .then(sendResponse);
    return true; // Indicates that the response is sent asynchronously
  }
});

const generateVideo = (text: string): Promise<{ s3VideoUrl: string } | { error: string }> => {
  return fetch('http://localhost:8000/generate_video', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text, style: "default" }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.s3VideoUrl) {
        console.log('Video URL:', data.s3VideoUrl);
        return { s3VideoUrl: data.s3VideoUrl };
      } else {
        throw new Error('Video URL not found in the response');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      return { error: 'Failed to generate video' };
    });
};

export { generateVideo };