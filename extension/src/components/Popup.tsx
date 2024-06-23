import React, { useState } from 'react';

const Popup: React.FC = () => {
  const [inputText, setInputText] = useState<string>('');
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateVideo = () => {
    setIsLoading(true);
    setError(null);
    chrome.runtime.sendMessage({ action: 'generateVideo', text: inputText }, (response) => {
      setIsLoading(false);
      if (response.videoData) {
        const blob = new Blob([Uint8Array.from(atob(response.videoData), c => c.charCodeAt(0))], { type: 'video/mp4' });
        const url = URL.createObjectURL(blob);
        setVideoUrl(url);
      } else if (response.error) {
        setError(response.error);
      }
    });
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
        <video controls src={videoUrl} style={{ maxWidth: '100%', marginTop: '10px' }}>
          Your browser does not support the video tag.
        </video>
      )}
    </div>
  );
};

export default Popup;