import React, { useState } from 'react';
import './Popup.css';

const Popup: React.FC = () => {
  const [inputText, setInputText] = useState<string>('');
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateVideo = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    event.preventDefault();
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
      generateVideo(inputText);
    }
  };

  return (
    <div className="popup-container">
      <div className="form-container">
        <h1>VidBite</h1>
        <form className="ai_inputWr">
          <span className="ai_placeholder">Online </span>
          <input
            type="text"
            name="promptInput"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter your text here"
          />
          <button onClick={handleGenerateVideo} disabled={isLoading || !inputText}>
            Generate
            <svg width="22" height="22" viewBox="0 0 20 20" fill="red" xmlns="http://www.w3.org/2000/svg">
              <path d="M14.1274 1.01957V1.01957C14.4612 3.69008 16.5647 5.79356 19.2352 6.12736V6.12736V6.12736C16.5647 6.46118 14.4612 8.56466 14.1274 11.2352V11.2352V11.2352C13.7936 8.56471 11.6901 6.46117 9.01968 6.12733V6.12733V6.12733C11.6901 5.79355 13.7936 3.69001 14.1274 1.01957V1.01957Z" fill="white"></path>
              <path d="M4.5689 6.01362V6.01362C4.80125 7.87244 6.2654 9.33656 8.12422 9.5689V9.5689V9.5689C6.2654 9.80126 4.80125 11.2654 4.56889 13.1242V13.1242V13.1242C4.33655 11.2654 2.87245 9.80126 1.01368 9.56889H1.01368V9.56889C2.87245 9.33656 4.33655 7.87239 4.5689 6.01362V6.01362Z" fill="white"></path>
              <path d="M9.67949 13.0102V13.0102C9.85394 14.4058 10.9532 15.5051 12.3488 15.6795V15.6795V15.6795C10.9532 15.854 9.85394 16.9533 9.67949 18.3489V18.3489V18.3489C9.50504 16.9533 8.4058 15.854 7.01023 15.6795V15.6795V15.6795C8.4058 15.5051 9.50505 14.4058 9.67949 13.0102V13.0102Z" fill="white"></path>
            </svg>
          </button>
        </form>
        {isLoading && <p>Generating video...</p>}
        {error && <p>Error: {error}</p>}
        {videoUrl && (
          <div>
            <video controls src={videoUrl} style={{ maxWidth: '100%', marginTop: '10px' }}>
              Your browser does not support the video tag.
            </video>
          </div>
        )}
      </div>
    </div>
  );
};

export default Popup;
