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

/* 
 * Creates and positions groups of pieces in a circular arrangement.
 *
 * Returns:
 *   Array<THREE.Group>: An array of piece groups, each containing spheres that make up the pieces.
 */
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

/* 
 * Checks if the pieces in a group are within the defined boundaries.
 *
 * Arguments:
 *   piecesGroup (Array<THREE.Group>): The group of pieces to evaluate for boundary placement.
 *
 * Returns:
 *   Array|boolean: Returns an array containing pieces with their positions if at least one group is fully within bounds; 
 *                  otherwise, returns false.
 */
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

/* 
 * Extracts data from the input and updates the pyramid structure, ensuring placement is valid and checking for errors.
 *
 * Arguments:
 *   input (Array): An array of objects containing piece names and positions to be placed in the pyramid.
 *   piecesGroup (Array<THREE.Group>): An array of piece groups that will be validated during placement.
 *
 * Returns:
 *   boolean: Returns true if the data is successfully extracted and the pyramid structure is updated, false otherwise.
 */
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

/* 
 * Creates a 3D pyramid based on the provided data.
 *
 * Arguments:
 *   data (Array): A 3D array representing the pyramid's layers, rows, and columns. Each value corresponds to a piece identifier 
 *                 (non-zero values are valid pieces).
 *
 * Returns:
 *   THREE.Group: A group containing all the spheres that make up the pyramid.
 */
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

/* 
 * Adjusts the spacing between layers in a pyramid group.
 *
 * Arguments:
 *   pyramidGroup (THREE.Group): The group of spheres that form the pyramid.
 *   orientation (string, optional): The orientation of the spacing, either 'vertical' or 'horizontal'. Defaults to 'vertical'.
 *
 * Returns:
 *   THREE.Group: A new group with the adjusted pyramid layers.
 */
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

/* 
 * Removes all groups from the scene.
 *
 * Arguments:
 *   scene (THREE.Scene): The scene from which all groups will be removed.
 */
export function removeAllGroupsFromScene(scene) {
  scene.children.forEach(child => {
      if (child instanceof THREE.Group) {
          scene.remove(child);
      }
  });
}

/* 
 * Rotates an object around a specified axis using a quaternion.
 *
 * Arguments:
 *   object (THREE.Object3D): The object to rotate. It must have a `quaternion` property.
 *   axis (string): The axis of rotation ('x', 'y', or 'z').
 *   angle (number): The rotation angle in degrees.
 */
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

/* 
 * Adjusts the position of a piece group to ensure it is properly aligned after rotation.
 *
 * Arguments:
 *   pieceGroup (THREE.Group): The group of objects whose position needs to be adjusted.
 */
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

/* 
 * This function checks if there are any overlapping spheres between the given piece group and the other groups.
 *
 * Arguments:
 *   pieceGroup (THREE.Group): The group of spheres to check for overlap.
 *   piecesGroup (Array<THREE.Group>): The array containing all groups to compare with.
 *   tolerance (number, optional): The distance within which two spheres are considered overlapping. Defaults to 1.9.
 *
 * Returns:
 *   boolean: Returns true if an overlap is detected, otherwise false.
 */
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