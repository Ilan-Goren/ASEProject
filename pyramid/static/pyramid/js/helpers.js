/* 
 * Updates the status messages displayed on the UI.
 * - If `message1` is provided, it updates the first status message, displaying it for 3 seconds before clearing.
 * - If `message2` is provided, it updates the second status message to show the number of pieces within bounds.
 *
 * Args:
 *   message1 (string): The first status message. Defaults to 'none' if not provided.
 *   message2 (string): The second status message. Defaults to 'none' if not provided.
 *
 * Notes:
 * - `message1` is shown for 3 seconds and then cleared.
 * - `message2` displays the count of pieces within bounds.
 */
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

/* 
 * Sets the emissive material properties for the selected piece based on the given state.
 * If `state` is true, the emissive color is set to a light gray with low intensity. 
 * If `state` is false, the emissive color is set to black, and the intensity is zero.
 *
 * Args:
 *   selected (THREE.Object3D): The currently selected piece object in the scene.
 *   state (boolean): Determines whether to activate or deactivate the emissive effect.
 *
 * Notes:
 * - Affects all spheres (children) of the selected piece.
 */
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