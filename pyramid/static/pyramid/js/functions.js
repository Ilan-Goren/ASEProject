import * as THREE from 'three';
import { pieces, colorMapping } from './defs.js';
import { 
  updateStatusMessage,
} from './helpers.js';

export var selected = null;
export var overlapExists = false;

/******************************************************************************************
                                  SELECTING AND MOVEMENT
******************************************************************************************/

/*
 * Handles mouse click events to select or deselect pieces in the 3D scene.
 * - Updates the `selected` variable based on the clicked object.
 * - Highlights the selected piece visually using emissive material properties.
 *
 * Args:
 *   event (MouseEvent): The mouse click event.
 *   piecesGroup (THREE.Group): The group containing all draggable pieces.
 *   raycaster (THREE.Raycaster): Used to calculate intersections with objects.
 *   mouse (THREE.Vector2): Stores the normalized mouse coordinates for raycasting.
 *   camera (THREE.Camera): The active camera used for raycasting.
 *
 * Notes:
 * - Normalizes mouse coordinates to the range [-1, 1] for compatibility with the raycaster.
 * - If a piece is clicked:
 *   - Sets the `selected` variable to the clicked object.
 *   - Updates the emissive material of the selected piece to indicate selection.
 * - If no piece is clicked:
 *   - Deselects the currently selected piece and resets its visual state.
 * - Emits console logs for debugging:
 *   - Logs the parent object of the selected piece.
 *   - Logs the position of the selected piece or "nothing selected" if deselected.
 * - Ensures that only valid pieces (within boundaries and without overlap) are highlighted.
 */

export function onClickHandler(event, piecesGroup, raycaster, mouse, camera) {
  // Calculate mouse position
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);

  // Check intersections with pieces in piecesGroup
  const intersects = raycaster.intersectObjects(piecesGroup, true);

  // If a piece is clicked, store it in selected variable
  if (intersects.length > 0) {
    if (selected && !selected.parent.partiallyInBounds){
      selected.material.emissive.set(0x000000);
      selected.material.emissiveIntensity = 0;
    }
    selected = intersects[0].object;
    console.log('selected piece:', selected.parent);

    selected.material.emissive.setHex(0xeeeeee);
    selected.material.emissiveIntensity = 0.5;
    console.log(selected.position)
  }
  else {
    // If no piece is clicked, set selected to null
    if (selected) {
      if (!overlapExists && !selected.parent.partiallyInBounds){
          selected.material.emissive.set(0x000000);
          selected.material.emissiveIntensity = 0;
      }
    selected = null;
    console.log('nothing selected');
  }
  }
}

/*
 * Handles keyboard input for moving the selected piece in the 3D scene.
 * - Moves the piece in the direction of the camera's orientation (forward, backward, left, right).
 * - Allows vertical movement when the shift key is pressed.
 * - Ensures movement steps are aligned to a grid and restricts movement below the plane.
 *
 * Args:
 *   event (KeyboardEvent): The keyboard event triggered by user input.
 *   camera (THREE.Camera): The active camera to determine movement direction.
 *   piecesGroup (THREE.Group): The group containing all pieces for boundary checks.
 *
 * Notes:
 * - Arrow keys are used for movement:
 *   - `ArrowUp` and `ArrowDown` move forward and backward, respectively.
 *   - `ArrowLeft` and `ArrowRight` move laterally (left and right).
 *   - Shift + `ArrowUp` or `ArrowDown` adjusts the vertical position.
 * - Movement is restricted to whole units in X and Z axes and a minimum Y value of 1.
 * - Calls:
 *   - `insideBoundariesHandler()` to detect pieces within bounds.
 *   - `highlightOverlappingPieces()` to detect overlaps.
 *   - `highlightPiecesPartiallyInsideBounds()` to detect incomplete placements.
 */

export function keyboardHandler(event, camera, piecesGroup) {
  if (selected) {
    
    const moveAmount = 1; 
    const movingObject = selected.parent;

    const cameraDirection = new THREE.Vector3();
    camera.getWorldDirection(cameraDirection);
    cameraDirection.y = 0;
    cameraDirection.normalize();

    if (event.shiftKey) {
      switch (event.key) {
        case 'ArrowUp': // Move up
          movingObject.position.y += (moveAmount + 1);
          break;
        case 'ArrowDown': // Move down
          movingObject.position.y -= (moveAmount + 1); // Ensure Y doesn't go below 0
          break;
      }
    } else {
      switch (event.key) {
        case 'ArrowUp': // Move forward
          movingObject.position.addScaledVector(cameraDirection, moveAmount);
          break;
        case 'ArrowDown': // Move backward
          movingObject.position.addScaledVector(cameraDirection, -moveAmount);
          break;
        case 'ArrowLeft': // Move left
          const leftDirection = new THREE.Vector3().crossVectors(cameraDirection, new THREE.Vector3(0, 1, 0)).normalize();
          movingObject.position.addScaledVector(leftDirection, -moveAmount);
          break;
        case 'ArrowRight': // Move right
          const rightDirection = new THREE.Vector3().crossVectors(cameraDirection, new THREE.Vector3(0, 1, 0)).normalize();
          movingObject.position.addScaledVector(rightDirection, moveAmount);
          break;
      }
    }
    /* Handle movement to be 2 units in x and z axis. 
    However restrict movement beyond point 0 (under plane) */
    
    movingObject.position.x = Math.round(movingObject.position.x);
    movingObject.position.y = Math.max(movingObject.position.y, 1);
    movingObject.position.z = Math.round(movingObject.position.z);

    insideBoundariesHandler(piecesGroup);
    highlightOverlappingPieces(selected, piecesGroup);
    highlightPiecesPartiallyInsideBounds(selected);
  }
}

 /******************************************************************************************
                                     MAIN FUNCTIONS
******************************************************************************************/

// Creates and positions groups of pieces in a circular arrangement.
//
// Returns:
//   Array<THREE.Group>: An array of piece groups, each containing spheres.
//
// Notes:
// - Each piece group is created from the `pieces` object, with positions defined for spheres.
// - Materials are assigned dynamically based on `colorMapping` or default to white.
// - Groups are evenly distributed in a circle of a defined radius and rotated around the x-axis by 90 degrees.
// - The `partiallyInBounds` property is initialized as false for each group.
// - Groups are stored in the `piecesGroup` array.
export function createPieces() {
  const piecesGroup = [];
  const radius = 18;                               // Radius of the circle
  const numPieces = Object.entries(pieces).length; // Number of pieces to place
  const angleStep = (2 * Math.PI) / numPieces;     // Angle between each piece

  let angle = 0; // initial angle

  Object.entries(pieces).forEach(([key, value]) => {
    const color = colorMapping[key] || 0xffffff;
    const material = new THREE.MeshPhysicalMaterial({ 
      color: color,          
      metalness: 0.1,       
      roughness: 0.4,         
      emissiveIntensity: 0.8,  
      clearcoat: 0.5,           
      clearcoatRoughness: 1.0,
    });

    // Create a group and name the group
    const pieceGroup = new THREE.Group();
    pieceGroup.name = key;

    // Create spheres
    value.forEach(pos => {
      const sphereGeometry = new THREE.SphereGeometry(1, 16, 16);
      const sphereMesh = new THREE.Mesh(sphereGeometry, material);
      sphereMesh.position.set(pos[0], pos[1], pos[2]);

      // Store the original position
      sphereMesh.userData.originalPosition = sphereMesh.position.clone();

      pieceGroup.add(sphereMesh); // Add sphere to this piece's group
    });

    // Position the group in a circle
    const x = Math.round(radius * Math.cos(angle));
    const z = Math.round(radius * Math.sin(angle));
    pieceGroup.position.set(x, 1, z);
    rotateWithQuaternion(pieceGroup, 'x', 90)

    pieceGroup.updateMatrix();
    // Add the piece to piecesGroup

    pieceGroup.partiallyInBounds = false;
    piecesGroup.push(pieceGroup);

    // Increment the angle for the next piece placement
    angle += angleStep;
  });

  return piecesGroup;
}

// Handles checking if pieces in a group are within defined boundaries.
//
// Args:
//   piecesGroup (Array<THREE.Group>): The group of pieces to evaluate.
//
// Returns:
//   Array|boolean: Returns an array of pieces with their positions if at least one group is fully in bounds; otherwise, returns false.
//
// Notes:
// - Updates the `partiallyInBounds` property of each group to indicate whether it is partially within bounds.
// - Calculates dynamic boundaries based on the vertical position of each group.
// - Updates a status message based on the count of correctly placed pieces.
export function insideBoundariesHandler(piecesGroup) {
  const piecesCorrectlyPlaced = [];
  const piecesInBounds = [];

  // looping over each piece
  piecesGroup.forEach(pieceGroup => {
    pieceGroup.updateMatrixWorld(true); // Ensure the world matrix is updated

    const y_pos = pieceGroup.position.y
    let boundryPoint = 5 - Math.round((y_pos - 1) / 2) - 1

    // Define the boundaries of the plane
    const boundaryBox = new THREE.Box3(
      new THREE.Vector3(-boundryPoint, -Infinity, -boundryPoint),
      new THREE.Vector3(boundryPoint, Infinity, boundryPoint)
    );

    const groupBoundingBox = new THREE.Box3().setFromObject(pieceGroup);

    if (groupBoundingBox.intersectsBox(boundaryBox)) {
      let spheresGroup = []
      // Check if all spheres in the group have positions within the boundary
      const allInBounds = pieceGroup.children.every(sphere => {
        const spherePosition = new THREE.Vector3();
        sphere.getWorldPosition(spherePosition);

        const y_pos = spherePosition.y
        let boundryPoint = 5 - Math.round((y_pos - 1) / 2) - 1
        console.log(boundryPoint);
        console.log(spherePosition);
        const boundaryBox = new THREE.Box3(
          new THREE.Vector3(-boundryPoint - 0.1, -Infinity, -boundryPoint - 0.1),
          new THREE.Vector3(boundryPoint + 0.1, Infinity, boundryPoint + 0.1)
        );
          spheresGroup.push({
            piece: pieceGroup.name,
            position: spherePosition
        })

        return boundaryBox.containsPoint(spherePosition); // Validate position
      });

      if (allInBounds) {
        pieceGroup.partiallyInBounds = false;

        piecesCorrectlyPlaced.push(pieceGroup);
        piecesInBounds.push(spheresGroup);
      }
      else {
        pieceGroup.partiallyInBounds = true;
      }
    }
    else {
      pieceGroup.partiallyInBounds = false;
    }
  });
  updateStatusMessage('none', piecesCorrectlyPlaced.length);
  return piecesCorrectlyPlaced.length > 0 ? piecesInBounds : false;
}

// Extracts data from the input and updates the pyramid structure, validating placement and checking for errors.
//
// Args:
//   input (Array): Array of objects containing piece names and positions to be placed in the pyramid.
//   piecesGroup (Array<THREE.Group>): The array of piece groups to validate.
//
// Returns:
//   boolean: Returns true if the data was successfully extracted and processed, false otherwise.
//
// Notes:
// - Checks for overlaps between pieces and partially placed pieces, showing alerts if issues are found.
// - Constructs a pyramid structure (3D array) based on the given input and piece positions.
// - Updates hidden form fields with the serialized pyramid structure and the list of placed pieces.
export function extractDataFromPlane(input, piecesGroup) {
  if (overlapExists){
    alert('Overlapping exists, fix it first to get accurate solutions.')
    return false
  }

  piecesGroup.forEach(piece => {
    if (piece.partiallyInBounds){
      alert('One or more pieces are placed incorrectly.')
      return false
    }
  })
  
  const piecesAlreadyPlaced = [];

  const layers = 5
  let pyramid = Array.from({ length: layers }, (_, z) =>
    Array.from({ length: layers - z }, () =>
      Array(layers - z).fill(0)
    )
  );
  input.forEach(layer => {
    layer.forEach(item => {
      const { piece, position } = item;

      const layerIndex = Math.round(position.y / 2) - 1;
      const rowIndex = Math.round((position.x + layers - 1 - layerIndex) / 2);
      const colIndex = Math.round((position.z + layers - 1 - layerIndex) / 2);

      if (
        pyramid[layerIndex] &&
        pyramid[layerIndex][rowIndex] &&
        pyramid[layerIndex][rowIndex][colIndex] !== undefined
      ) {
        pyramid[layerIndex][rowIndex][colIndex] = piece;
        piecesAlreadyPlaced.push(piece);
      }
    });
  });

  const pyramidJSON = JSON.stringify(pyramid);
  const piecesPlacedJSON = JSON.stringify(piecesAlreadyPlaced);

  document.getElementById('pyramidField').value = pyramidJSON;
  document.getElementById('piecesPlacedField').value = piecesPlacedJSON;

  return true;
}

// Creates a 3D pyramid based on the given data.
//
// Args:
//   data (Array): A 3D array representing the layers, rows, and columns of the pyramid where each value corresponds
//                 to a piece identifier (non-zero values are valid pieces).
//
// Returns:
//   THREE.Group: A group containing all the spheres that form the pyramid.
//
// Notes:
// - Iterates through the data to create spheres for each valid piece, placing them in the correct 3D position.
// - The color of each sphere is determined by a color mapping based on the piece identifier.
// - Adds each sphere to the `pyramidGroup` which is returned as the final 3D structure.
export function createPyramid(data) {
  const pyramidGroup = new THREE.Group()
  data.forEach((layer, layerIndex) => {
      layer.forEach((row, rowIndex) => {
          row.forEach((cellValue, colIndex) => {
              if (cellValue > 0) {
                  const color = colorMapping[cellValue.toString()];
                  const material = new THREE.MeshPhysicalMaterial({ 
                    color: color,          
                    metalness: 0.1,       
                    roughness: 0.4,         
                    emissiveIntensity: 0.8,  
                    clearcoat: 0.5,           
                    clearcoatRoughness: 1.0,
                  });
                  const sphereGeometry = new THREE.SphereGeometry(1, 16, 16);
                  const sphere = new THREE.Mesh(sphereGeometry, material);

                  const x = colIndex * 2 - row.length;
                  const y = layerIndex * 2;
                  const z = rowIndex * 2 - layer[0].length;

                  sphere.position.set(x, y, z);

                  // Add the sphere to the pyramid group
                  pyramidGroup.add(sphere);
              }
          });
      });
  });
  return pyramidGroup
}


 /******************************************************************************************
                                     HELPER FUNCTIONS
******************************************************************************************/

// Adjusts the spacing between layers in a pyramid group.
// 
// Args:
//   pyramidGroup (THREE.Group): The group of spheres representing the pyramid.
//   orientation (string, optional): The spacing orientation, either 'vertical' or 'horizontal'. Defaults to 'vertical'.
// 
// Returns:
//   THREE.Group: A clone of the adjusted pyramid group.
export function adjustPyramidSpacing(pyramidGroup, orientation = 'vertical') {
  pyramidGroup.children.forEach((sphere) => {
      const { x, y, z } = sphere.position;
      if (orientation === 'vertical') {
          sphere.position.set(x, y + Math.floor(y / 2) * 2, z);
      } else if (orientation === 'horizontal') {
        const diagonalLayer = Math.floor((x + z));
        sphere.position.set(
            x / 4 + diagonalLayer * 4,
            y ,
            z + diagonalLayer);
        }
  });
  return pyramidGroup.clone()
}

// Removes all groups from the scene.
//
// Args:
//   scene (THREE.Scene): The scene from which to remove all groups.
export function removeAllGroupsFromScene(scene) {
  scene.children.forEach(child => {
      if (child instanceof THREE.Group) {
          scene.remove(child);
      }
  });
}

// Rotates an object around a specified axis using a quaternion.
//
// Args:
//   object (THREE.Object3D): The object to rotate. Must have a `quaternion` property.
//   axis (string): The axis of rotation ('x', 'y', or 'z').
//   angle (number): The rotation angle in degrees.
//
// Modifies:
//   The `object.quaternion` property to apply the rotation.
//   The `object.rotationTracker` property to track the cumulative rotation for each axis.
function rotateWithQuaternion(object, axis, angle) {
  if (!object.rotationTracker) {
    object.rotationTracker = { x: 0, y: 0, z: 0 };
  }
  angle = THREE.MathUtils.degToRad(angle);
  const quaternion = new THREE.Quaternion();

  // Determine the axis of rotation and apply the rotation
  if (axis === 'x') {
    quaternion.setFromAxisAngle(new THREE.Vector3(1, 0, 0).normalize(), angle);
    object.rotationTracker.x += THREE.MathUtils.radToDeg(angle);
  } else if (axis === 'y') {
    quaternion.setFromAxisAngle(new THREE.Vector3(0, 1, 0).normalize(), angle);
    object.rotationTracker.y += THREE.MathUtils.radToDeg(angle);
  } else if (axis === 'z') {
    quaternion.setFromAxisAngle(new THREE.Vector3(0, 0, 1).normalize(), angle);
    object.rotationTracker.z += THREE.MathUtils.radToDeg(angle);
  }

  object.quaternion.multiply(quaternion);
  object.quaternion.normalize();

  // Reset the tracker and quaternion for any 360-degree rotations
  ['x', 'y', 'z'].forEach((axis) => {
    if (object.rotationTracker[axis] >= 360 || object.rotationTracker[axis] <= -360) {
      object.rotationTracker[axis] %= 360; // Reset tracker to within -360 to 360 range
    }
  });
}

// Adjusts the position of a piece group to ensure it aligns correctly after rotation.
//
// Args:
//   pieceGroup (THREE.Group): The group of objects whose position needs adjustment.
//
// Notes:
// - Checks the bounding box of the group and aligns the bottom of the group (`min.y`) to the plane defined at `planeY` (default is 0).
// - Offsets the group's vertical position (`y`) to correct any misalignment.
// - Rounds the horizontal positions (`x` and `z`) to ensure they are integers, maintaining grid alignment.
export function fixPositionAfterRotation(pieceGroup) {
  const boundingBox = new THREE.Box3().setFromObject(pieceGroup);
  const planeY = 0;

  if (boundingBox.min.y < planeY ) {
    const offsetY = Math.abs(boundingBox.min.y - planeY);
    pieceGroup.position.y += offsetY;
    pieceGroup.position.x = Math.round(pieceGroup.position.x)
    pieceGroup.position.z = Math.round(pieceGroup.position.z)
  }
  
  else if (boundingBox.min.y > planeY) {
    const offsetY = Math.abs(planeY - boundingBox.min.y);
    pieceGroup.position.y -= offsetY;
    pieceGroup.position.x = Math.round(pieceGroup.position.x)
    pieceGroup.position.z= Math.round(pieceGroup.position.z)
  }
}

// Checks for overlapping spheres between a given piece group and other groups.
//
// Args:
//   pieceGroup (THREE.Group): The group to check for overlaps.
//   piecesGroup (Array<THREE.Group>): The array of all groups to compare against.
//   tolerance (number, optional): The distance within which two spheres are considered overlapping. Defaults to 1.9.
//
// Returns:
//   boolean: True if an overlap is detected; otherwise, false.
//
// Notes:
// - Iterates over all other groups in `piecesGroup` and skips the comparison with the same group.
// - Compares the world positions of each sphere in `pieceGroup` with each sphere in the other groups.
// - Uses `distanceTo` to calculate the distance between spheres and checks against the `tolerance` value.
export function checkOverlap(pieceGroup, piecesGroup, tolerance = 1.9) {
  // iterate over all groups in piecesGroup
  for (let i = 0; i < piecesGroup.length; i++) {
    const otherGroup = piecesGroup[i];

    // skip the same piece
    if (otherGroup === pieceGroup) continue;

    // compare positions of each sphere in pieceGroup with each sphere in otherGroup
    for (let pieceChild of pieceGroup.children) {
      const piecePosition = new THREE.Vector3();
      pieceChild.getWorldPosition(piecePosition); // get world position of pieceChild for comparison

      for (let otherChild of otherGroup.children) {
        const otherPosition = new THREE.Vector3();
        otherChild.getWorldPosition(otherPosition); // get world position of otherChild for comparison

        // check if the positions are within tolerance
        if (piecePosition.distanceTo(otherPosition) < tolerance) {
          return true; // overlap detected
        }
      }
    }
  }

  return false; // no overlap detected
}

/* 
 * Highlights overlapping pieces when a piece is moved and updates the status message accordingly.
 *
 * Args:
 *   selected (THREE.Mesh): The selected piece (mesh) that was moved.
 *   piecesGroup (Array<THREE.Group>): The array of all piece groups to check for overlap.
 *
 * Notes:
 * - Checks if the selected piece overlaps with any other piece using the `checkOverlap` function.
 * - If an overlap is detected, the selected piece's emissive color is changed to red, and a status message is updated.
 * - If no overlap is detected, the emissive color is reset to its original state.
 * - The `overlapExists` flag is updated based on the overlap check.
 */
export function highlightOverlappingPieces(selected, piecesGroup){
  if (selected){
    if (checkOverlap(selected.parent, piecesGroup)){
      overlapExists = true;
      updateStatusMessage('Overlap', 'none');
      selected.material.emissive.setHex(0xFF0000);
      selected.material.emissiveIntensity = 20;
    }
    else{
      overlapExists = false
      if (selected){
        selected.material.emissive.setHex(0xeeeeee);
        selected.material.emissiveIntensity = 0.5;
      }
      else{
        selected.material.emissive.set(0x000000);
        selected.material.emissiveIntensity = 0;
      }
    }
  }
}

/* 
 * Highlights pieces that are partially inside the defined boundaries when selected.
 * Resets the highlight when the piece is correctly placed or there is no overlap.
 *
 * Args:
 *   selected (THREE.Mesh): The selected piece (mesh) to check for boundary placement.
 *
 * Notes:
 * - If the piece's parent group is partially inside the boundaries, it highlights the piece with a red emissive color.
 * - If the piece is correctly placed or no overlap exists, the emissive color is reset to its original state.
 * - The `overlapExists` flag is used to ensure the piece is highlighted correctly when there is no overlap.
 */
export function highlightPiecesPartiallyInsideBounds(selected){
  if (selected.parent.partiallyInBounds){
    selected.material.emissive.setHex(0xFF0000);
    selected.material.emissiveIntensity = 20;
  }
  else if (!overlapExists) {
    if (selected){
      selected.material.emissive.setHex(0xeeeeee);
      selected.material.emissiveIntensity = 0.5;
    }
    else{
      selected.material.emissive.set(0x000000);
      selected.material.emissiveIntensity = 0;
    }
  }
}

/* 
 * Changes the orientation of the selected piece in the 3D scene based on whether it is flat or not.
 * Rotates the selected piece and updates its position accordingly.
 *
 * Args:
 *   piecesGroup (Array): Group of pieces to check for boundary placement.
 *   isPieceFlat (boolean): Indicates whether the piece is currently flat or not.
 *
 * Returns:
 *   boolean: The updated orientation state of the piece (flat or not).
 *
 * Notes:
 * - Rotates the selected piece around both the X and Y axes based on the orientation state.
 * - If the piece is flat, it applies a -90 degree rotation along the X axis and a -45 degree rotation along the Y axis.
 * - If the piece is not flat, it applies a 90 degree rotation along the X axis and a 45 degree rotation along the Y axis.
 * - After rotation, the position is fixed, boundaries are checked, overlapping pieces are highlighted, and pieces partially inside the boundaries are highlighted.
 * - If no piece is selected, a status message is shown.
 */
export function changeOrientationHandler(piecesGroup, isPieceFlat) {
  if (selected) {

    // Apply the transformation to each child object of the selected parent group
    selected.parent.children.forEach((child) => {
      const pos = child.position;
      if(isPieceFlat) {

        child.originalPosition = child.position.clone();
        child.plane = 1;

        const newX = (pos.x - pos.y) / 2;
        const newY = (pos.x - pos.y) / 2;
        const newZ = (-pos.x - pos.y) ;


        pos.set(newX, newY, newZ);

      } else {
        const originalPos = child.userData.originalPosition;
        child.position.copy(originalPos); // Restore position
      }
    });

    fixPositionAfterRotation(selected.parent);
    insideBoundariesHandler(piecesGroup);
    highlightOverlappingPieces(selected, piecesGroup);
    highlightPiecesPartiallyInsideBounds(selected);

    isPieceFlat = !isPieceFlat; // Toggle orientation state
  } else {
    updateStatusMessage('No piece selected!');
  }
  return isPieceFlat;
}

export function uprightOrientationRotationHandler(piecesGroup) {
    if (selected) {

      // Apply the transformation to each child object of the selected parent group
      selected.parent.children.forEach((child) => {
        const pos = child.position;
        const originalPos = child.userData.originalPosition;
        let newX = originalPos.x;
        let newY = originalPos.z;
        let newZ = originalPos.z;
        switch(child.plane) {
          case 1:
            newX = (originalPos.x - originalPos.y) / 2;
            newY = (originalPos.x - originalPos.y) / 2;
            newZ = (originalPos.x + originalPos.y) ;
            child.plane = 2;
            break;
          case 2:
            newX = (originalPos.x + originalPos.y) / 2;
            newY = (originalPos.x + originalPos.y) / 2;
            newZ = (originalPos.x - originalPos.y) ;
            child.plane = 3;
            // code block
            break;
          case 3:
            newX = (originalPos.x - originalPos.y) / 2;
            newY = (originalPos.x - originalPos.y) / 2;
            newZ = (-originalPos.x - originalPos.y) ;
            child.plane = 1;
            break;
          case 4:
            newX = (originalPos.x + originalPos.y) / 2;
            newY = (originalPos.x + originalPos.y) / 2;
            newZ = (-originalPos.x + originalPos.y) ;
            child.plane = 4;
            break;
        }

          pos.set(newX, newY, newZ);

      });

      fixPositionAfterRotation(selected.parent);
      insideBoundariesHandler(piecesGroup);
      highlightOverlappingPieces(selected, piecesGroup);
      highlightPiecesPartiallyInsideBounds(selected);

  } else {
    updateStatusMessage('No piece selected!');
  }
}

/* 
 * Rotates the selected piece around the Z-axis or Y-axis depending on its current orientation.
 * It also checks for boundary constraints, overlapping pieces, and pieces partially inside boundaries.
 *
 * Args:
 *   piecesGroup (Array): Group of pieces to check for boundary placement.
 *   isPieceFlat (boolean): Indicates whether the piece is currently flat or not.
 *
 * Notes:
 * - Rotates the selected piece by 90 degrees around either the Z-axis (if flat) or Y-axis (if not flat).
 * - After rotating, the position is fixed, boundaries are checked, overlapping pieces are highlighted, and pieces partially inside the boundaries are highlighted.
 * - A status message is displayed indicating the success or failure of the rotation operation.
 * - Rotation values are logged in degrees.
 * - If no piece is selected, a status message is shown indicating that no piece is selected.
 */
export function rotateHandler(piecesGroup, isPieceFlat) {
  if (selected) {
    if (isPieceFlat){
      rotateWithQuaternion(selected.parent, 'z', 90);
    }
    else {
      uprightOrientationRotationHandler(piecesGroup)
      //rotateWithQuaternion(selected.parent, 'y', 90);
    }
    fixPositionAfterRotation(selected.parent);

    insideBoundariesHandler(piecesGroup);
    
    highlightOverlappingPieces(selected, piecesGroup);

    highlightPiecesPartiallyInsideBounds(selected);

    updateStatusMessage('Piece Rotated Successfully!')
    
  } else {
    updateStatusMessage('No piece selected!');
  }
}

/* 
 * Flips the selected piece around the Y-axis, and updates its position accordingly.
 * It also checks for boundary constraints, overlapping pieces, and pieces partially inside boundaries.
 *
 * Args:
 *   piecesGroup (Array): Group of pieces to check for boundary placement.
 *   isPieceFlat (boolean): Indicates whether the piece is currently flat or not.
 *
 * Notes:
 * - Rotates the selected piece by 180 degrees along the Y-axis, regardless of its current orientation.
 * - After flipping, the position is fixed, boundaries are checked, overlapping pieces are highlighted, and pieces partially inside the boundaries are highlighted.
 * - A status message is displayed indicating the success or failure of the flip operation.
 * - If no piece is selected, a status message is shown indicating that no piece is selected.
 */
export function flipHandler(piecesGroup, isPieceFlat) {
  if (selected) {
    if (isPieceFlat){
      rotateWithQuaternion(selected.parent, 'y', 180);
    }
    else {
      rotateWithQuaternion(selected.parent, 'y', 180);
    }
    fixPositionAfterRotation(selected.parent);

    insideBoundariesHandler(piecesGroup);
    
    highlightOverlappingPieces(selected, piecesGroup);
    highlightPiecesPartiallyInsideBounds(selected);

    updateStatusMessage('Piece Flipped Successfully!')

  } else {
    updateStatusMessage('No piece selected!');
  }
}