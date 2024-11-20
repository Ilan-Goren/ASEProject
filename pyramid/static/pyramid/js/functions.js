import * as THREE from 'three';
import * as BufferGeometryUtils from 'three/addons/utils/BufferGeometryUtils.js';
import { pieces, colorMapping } from './defs.js';
export var selected = null;


 /******************************************************************************************
                                  HANDLER FUNCTIONS
******************************************************************************************/

  export function onClickHandler(event, piecesGroup, raycaster, mouse, camera) {
    // Calculate mouse position
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
  
    // Check intersections with pieces in piecesGroup
    const intersects = raycaster.intersectObjects(piecesGroup.children, true);
  
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
    }
    else {
      // If no piece is clicked, set selected to null
      if (selected) {
        selected.material.emissive.set(0x000000); // Reset the previous piece highlight
        selected.material.emissiveIntensity = 0;
      }
      selected = null;
      console.log('nothing selected');
    }
  }

  export function keyboardHandler(event, camera){
    if (selected) {
      const moveAmount = 2;
      const prevPosition = selected.position.clone();
      const cameraDirection = new THREE.Vector3();
      camera.getWorldDirection(cameraDirection);
  
      cameraDirection.y = 0; // Ignore the Y component
      cameraDirection.normalize(); // Normalize the projected direction

      if (event.shiftKey) {
        switch (event.key) {
          case 'ArrowUp': // Move up
            selected.position.y += moveAmount;
            break;
          case 'ArrowDown': // Move down
            selected.position.y = Math.max(selected.position.y - moveAmount, 0); // Ensure Y doesn't go below 0
            break;
        }
      } else {
        switch (event.key) {
          case 'ArrowUp': // Move forward
            selected.position.addScaledVector(cameraDirection, moveAmount);
            break;
          case 'ArrowDown': // Move backward
            selected.position.addScaledVector(cameraDirection, -moveAmount);
            break;
          case 'ArrowLeft': // Move left
            const leftDirection = new THREE.Vector3().crossVectors(cameraDirection, new THREE.Vector3(0, 1, 0)).normalize();
            selected.position.addScaledVector(leftDirection, -moveAmount);
            break;
          case 'ArrowRight': // Move right
            const rightDirection = new THREE.Vector3().crossVectors(cameraDirection, new THREE.Vector3(0, 1, 0)).normalize();
            selected.position.addScaledVector(rightDirection, moveAmount);
            break;
        }
      }
  
      // Ensure Y position doesn't go negative
      selected.position.y = Math.max(selected.position.y, 0);
  
      // Increment by 2-units for X and Z axes
      selected.position.x = Math.round(selected.position.x / 2) * 2;
      selected.position.z = Math.round(selected.position.z / 2) * 2;
  
      // Check for overlap after movement
      if (checkOverlap(selected)) {
        // Revert to the previous position if there's an overlap
        selected.position.copy(prevPosition);
      }
    }
  }


 /******************************************************************************************
                                     MAIN FUNCTIONS
******************************************************************************************/

function checkOverlap(piece, piecesGroup) {
  const boundingBox = new THREE.Box3().setFromObject(piece);

  for (let i = 0; i < piecesGroup.children.length; i++) {
    const otherPiece = piecesGroup.children[i];
    if (otherPiece !== piece) {
      const otherBoundingBox = new THREE.Box3().setFromObject(otherPiece);

      // Calculate the overlap dimensions
      const overlapX = Math.max(0, Math.min(boundingBox.max.x, otherBoundingBox.max.x) - Math.max(boundingBox.min.x, otherBoundingBox.min.x));
      const overlapY = Math.max(0, Math.min(boundingBox.max.y, otherBoundingBox.max.y) - Math.max(boundingBox.min.y, otherBoundingBox.min.y));
      const overlapZ = Math.max(0, Math.min(boundingBox.max.z, otherBoundingBox.max.z) - Math.max(boundingBox.min.z, otherBoundingBox.min.z));

      if (overlapX > 0 && overlapY > 0 && overlapZ > 0) {
        return true;
      }
    }
  }
  return false;
}


// Function to parse the table data and return it as an array of layers
function parseTableData() {
  const layers = [];
  const tables = document.querySelectorAll('.pyramids table');
  
  tables.forEach(table => {
    const rows = [];
    const cells = table.querySelectorAll('tr');
    
    cells.forEach(row => {
      const values = Array.from(row.querySelectorAll('td')).map(cell => ({
        value: parseInt(cell.textContent),
        className: cell.className
      }));
      rows.push(values);
    });

    layers.push(rows);
  });

  return layers;
}

// Function to create the pyramid
export function createPyramid() {
  layers = parseTableData();
  layers.forEach((layer, layerIndex) => {
    layer.forEach((row, rowIndex) => {
      row.forEach((cell, colIndex) => {
        if (cell.value === 1) {
          const color = colorMapping[cell.className] || 0xffffff;
          const material = new THREE.MeshStandardMaterial({ color });
          const sphereGeometry = new THREE.SphereGeometry(1, 16, 16);
          const sphere = new THREE.Mesh(sphereGeometry, material);

          sphere.position.set(1 + colIndex * 2 - layer.length, 4.5 - layerIndex, 1 + rowIndex * 2 - layer[0].length);
          pyramidGroup.add(sphere);
        }
      });
    });
  });

  // Add the entire group to the scene
  scene.add(pyramidGroup);
}

export function detectPiecesOnPlane (piecesGroup) {
  const piecesOnPlane = [];
  // Iterate over pieces in the scene
  piecesGroup.children.forEach(piece => {
    if (-14 <= piece.position.z <= -8 || 56 <= piece.position.x <= 64) {
      piecesOnPlane.push({
        piece: piece,
        position: piece.position.clone()
      });
    }
  });

  console.log(piecesOnPlane);
  return piecesOnPlane;
};

export function createPieces(piecesGroup) {
  let offset = 0;

  Object.entries(pieces).forEach(([key, value]) => {
    const color = colorMapping[key] || 0xffffff;
    const material = new THREE.MeshStandardMaterial({ color });
    
    const geometries = value.map(pos => {
      const sphereGeometry = new THREE.SphereGeometry(1, 16, 16);
      sphereGeometry.translate(pos[0], pos[1], pos[2]); // Position each sphere
      return sphereGeometry;
    });

    // Merge all sphere geometries into one geometry
    const mergedGeometry = BufferGeometryUtils.mergeGeometries(geometries);

    const pieceMesh = new THREE.Mesh(mergedGeometry, material);
    pieceMesh.userData.name = `piece ${key}`

    // Position the piece and add to piecesGroup
    pieceMesh.position.setX(offset);
    pieceMesh.rotation.x += THREE.MathUtils.degToRad(90);
    piecesGroup.add(pieceMesh)
    offset += 10;
  });

  // Set initial position and rotation of piecesGroup
  piecesGroup.position.set(-60, 1, 10);
}