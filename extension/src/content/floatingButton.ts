export function createFloatingButton(selectedText: string) {
    console.log('Creating floating button');
    removeFloatingButton();
    const button = document.createElement('div');
    button.id = 'vidbite-floating-button';
    button.textContent = 'V';
    button.style.cssText = `
      position: absolute;
      background-color: #6d28d9;
      color: white;
      width: 15px;
      height: 15px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 10000;
      font-size: 7px;
      font-weight: bold;
      box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    `;
    
    const selection = window.getSelection();
    if (selection && selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      
      button.style.left = `${rect.right + window.scrollX + 5}px`;
      button.style.top = `${rect.top + window.scrollY - 15}px`;
    }
  
    button.onclick = () => {
      if (chrome.runtime?.id) {
        chrome.runtime.sendMessage({ action: 'openPopup', text: selectedText });
      } else {
        console.warn('Chrome runtime is not available. Extension might be reloading.');
      }
    };
    document.body.appendChild(button);
    console.log('Floating button created');
  }
  export function removeFloatingButton() {
    const existingButton = document.getElementById('vidbite-floating-button');
    if (existingButton) {
      existingButton.remove();
    }
  }