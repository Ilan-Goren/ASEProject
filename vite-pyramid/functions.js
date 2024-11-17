import * as THREE from 'three';
import * as BufferGeometryUtils from 'three/addons/utils/BufferGeometryUtils.js';
import { pieces, colorMapping } from './defs.js';
export var selected = null;
export var global_pieces = {};

 /******************************************************************************************
                                  HANDLER FUNCTIONS
******************************************************************************************/

  export function onClickHandler(event, piecesGroup, raycaster, mouse, camera) {
    // Calculate mouse position
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
  
    // Check intersections with pieces in piecesGroup
    const intersects = raycaster.intersectObjects(piecesGroup, true);
  
    // If a piece is clicked, store it in selected variable
    if (intersects.length > 0) {
      if (selected){
        selected.material.emissive.set(0x000000);
        selected.material.emissiveIntensity = 0;
      }
      selected = intersects[0].object;
      console.log('selected piece:', selected);
  
      selected.material.emissive.setHex(0xeeeeee);
      selected.material.emissiveIntensity = 0.5;
      console.log(selected.position)
    }
    else {
      // If no piece is clicked, set selected to null
      if (selected) {
        selected.material.emissive.set(0x000000); // Reset the previous piece highlight
        selected.material.emissiveIntensity = 0;
        
      }
      selected = null;
      console.log('nothing selected');
      const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0); // Horizontal plane at y = 0
      const point = new THREE.Vector3();
      raycaster.ray.intersectPlane(plane, point);
      console.log('Click position on plane:', point);
    }
  }

  export function keyboardHandler(event, camera, piecesGroup) {
    if (selected) {
      const moveAmount = 2;
      let targetGroup = null;

      piecesGroup.forEach(group => {
        if (group.children.includes(selected)) {
          targetGroup = group;
        }
      });

      const movingObject = targetGroup;
  
      const cameraDirection = new THREE.Vector3();
      camera.getWorldDirection(cameraDirection);
      cameraDirection.y = 0;
      cameraDirection.normalize();

      if (false) {
        // overlap to be implemented
        
      }
      else {
  
      if (event.shiftKey) {
        switch (event.key) {
          case 'ArrowUp': // Move up
            movingObject.position.y += moveAmount;
            break;
          case 'ArrowDown': // Move down
            movingObject.position.y = Math.max(movingObject.position.y - moveAmount, 0); // Ensure Y doesn't go below 0
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
      // Ensure Y position doesn't go negative
      movingObject.position.y = Math.max(movingObject.position.y, 0);
  
      // Snap to a 2-unit grid on X and Z axes
      movingObject.position.x = Math.round(movingObject.position.x / 2) * 2;
      movingObject.position.z = Math.round(movingObject.position.z / 2) * 2;
    }
  }
  }


 /******************************************************************************************
                                     MAIN FUNCTIONS
******************************************************************************************/

// function checkOverlap(pieceGroup, piecesGroup) {
//   // Iterate over all groups in piecesGroup
//   for (let i = 0; i < piecesGroup.length; i++) {
//     const otherGroup = piecesGroup[i];

//     // Skip the same group
//     if (otherGroup === pieceGroup) continue;

//     // Compare each child in pieceGroup with each child in otherGroup
//     for (let pieceChild of pieceGroup.children) {
//       const pieceBoundingBox = new THREE.Box3().setFromObject(pieceChild);

//       for (let otherChild of otherGroup.children) {
//         const otherBoundingBox = new THREE.Box3().setFromObject(otherChild);

//         // Check for overlap in all dimensions
//         if (
//           pieceBoundingBox.min.x < otherBoundingBox.max.x &&
//           pieceBoundingBox.max.x > otherBoundingBox.min.x &&
//           pieceBoundingBox.min.y < otherBoundingBox.max.y &&
//           pieceBoundingBox.max.y > otherBoundingBox.min.y &&
//           pieceBoundingBox.min.z < otherBoundingBox.max.z &&
//           pieceBoundingBox.max.z > otherBoundingBox.min.z
//         ) {
//           return true; // Overlap detected
//         }
//       }
//     }
//   }

//   return false; // No overlap detected
// }

export function detectPiecesOnPlane(piecesGroup) {
  const piecesOnPlane = [];

  // Define the plane boundaries
  const planeMinX = -5;
  const planeMaxX = 5;
  const planeMinZ = -5;
  const planeMaxZ = 5;

  piecesGroup.forEach(pieceGroup => {
    pieceGroup.updateMatrixWorld(true);

    // Calculate the bounding box for the entire group after rotation
    const boundingBox = new THREE.Box3().setFromObject(pieceGroup);

    pieceGroup = pieceGroup.clone()
    pieceGroup.rotation.x -= THREE.MathUtils.degToRad(90);
    
    if (
      boundingBox.min.x >= planeMinX &&
      boundingBox.max.x <= planeMaxX &&
      boundingBox.min.z >= planeMinZ &&
      boundingBox.max.z <= planeMaxZ
    ) {
      piecesOnPlane.push({
        piece: pieceGroup,
        position: pieceGroup.position.clone(),
      });
    }
  });

  return piecesOnPlane.length > 0 ? piecesOnPlane : false;
}

export function rotateHandler(){
    if (selected) {
      // Rotate the selected piece
      selected.rotateZ(THREE.MathUtils.degToRad(90));
      selected.updateMatrixWorld(true);  
  
      // Update the bounding box
      const boundingBox = new THREE.Box3().setFromObject(selected);
      selected.boundingBox = boundingBox;
    } else {
      console.log('No piece selected for rotation');
    }
}


export function createPieces() {
  const piecesGroup = [];
  const radius = 18; // Radius of the circle
  const numPieces = Object.entries(pieces).length; // Number of pieces to place
  const angleStep = (2 * Math.PI) / numPieces; // Angle between each piece

  let angle = 0; // initial angle

  Object.entries(pieces).forEach(([key, value]) => {
    const color = colorMapping[key] || 0xffffff;
    const material = new THREE.MeshStandardMaterial({ color });

    // Create a group and name the group
    const pieceGroup = new THREE.Group();
    pieceGroup.name = `piece${key}`;

    // Create spheres
    value.forEach(pos => {
      const sphereGeometry = new THREE.SphereGeometry(1, 16, 16);
      const sphereMesh = new THREE.Mesh(sphereGeometry, material);
      sphereMesh.position.set(pos[0], pos[1], pos[2]);
      pieceGroup.add(sphereMesh); // Add sphere to this piece's group
    });

    // Position the group in a circle
    const x = radius * Math.cos(angle); // Calculate X
    const z = radius * Math.sin(angle); // Calculate Z
    pieceGroup.position.set(x, 1, z); // Position around the plane

    // Rotate the piece group
    pieceGroup.rotation.x += THREE.MathUtils.degToRad(90);

    // Add the piece to piecesGroup
    piecesGroup.push(pieceGroup);

    // Increment the angle
    angle += angleStep;
  });

  return piecesGroup;
}