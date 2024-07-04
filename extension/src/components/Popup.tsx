import React, { useState } from 'react';

const Popup: React.FC = () => {
  const [inputText, setInputText] = useState<string>('');
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateVideo = () => {
    setIsLoading(true);
    setError(null);
    setVideoUrl(null);
  
    const generateVideo = (text: string) => {
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
          setVideoUrl(data.s3VideoUrl);
          console.log('Video URL:', data.s3VideoUrl);
        } else {
          throw new Error('Video URL not found in the response');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setError('Failed to generate video');
      })
      .finally(() => {
        setIsLoading(false);
      });
    };
  
    if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.sendMessage) {
      // Chrome extension logic
      chrome.runtime.sendMessage({ action: 'generateVideo', text: inputText }, (response) => {
        setIsLoading(false);
        if (response.s3VideoUrl) {
          setVideoUrl(response.s3VideoUrl);
          console.log('Video URL:', response.s3VideoUrl);
        } else if (response.error) {
          setError(response.error);
        }
      });
    } else {
      // React development server logic
      generateVideo(inputText);
    }
  };

  return (
    <div>
      <h1>Text-to-Manim Video Generator</h1>
      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Enter your text here"
        rows={4}
        cols={50}
      />
      <button onClick={handleGenerateVideo} disabled={isLoading || !inputText}>
        Generate Video
      </button>
      {isLoading && <p>Generating video...</p>}
      {error && <p>Error: {error}</p>}
      {videoUrl && (
        <div>
          <p>Video URL: {videoUrl}</p>
          <video controls src={videoUrl} style={{ maxWidth: '100%', marginTop: '10px' }}>
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
};

export default Popup;