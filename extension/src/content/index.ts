import { createFloatingButton, removeFloatingButton } from './floatingButton';

function handleMouseUp() {
  if (chrome.runtime?.id) {
    const selectedText = window.getSelection()?.toString().trim();
    if (selectedText && selectedText.length > 0) {
      console.log('Text selected:', selectedText);
      createFloatingButton(selectedText);
    } else {
      removeFloatingButton();
    }
  }
}

function setupListeners() {
  document.addEventListener('mouseup', handleMouseUp);
}

function removeListeners() {
  document.removeEventListener('mouseup', handleMouseUp);
}

function init() {
  setupListeners();
  console.log('VidBite content script initialized');
}

init();

if (chrome.runtime?.id) {
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getSelectedText') {
      const selectedText = window.getSelection()?.toString().trim();
      sendResponse({ text: selectedText });
    }
  });
} else {
  console.warn('Chrome runtime is not available. Extension might be reloading.');
  removeListeners();
}