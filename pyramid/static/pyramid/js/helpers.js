export function updateStatusMessage(message1='none', message2='none') {
    if (message1 != 'none'){
      let temp_message = document.getElementById('statusMessage1')
      temp_message.textContent = `${message1}`;
      setTimeout(() => {
        temp_message.textContent = '';
      }, 3000);
    }
  
    if (message2 != 'none'){
      document.getElementById('statusMessage2').textContent = `Number of pieces within bounds ${message2}`;
    }
  }

  export function setEmissiveForSelected(selected, state){
    if (selected) {
      if (state){
        selected.parent.children.forEach(sphere => {
          sphere.material.emissive.setHex(0xeeeeee);
          sphere.material.emissiveIntensity = 0.5;
    
        })
      }
      else {
        selected.parent.children.forEach(sphere => {
          sphere.material.emissive.set(0x000000);
          sphere.material.emissiveIntensity = 0;
        })
      }
    }
  }