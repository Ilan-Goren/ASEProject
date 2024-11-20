import * as THREE from 'three';
import { pieces, colorMapping } from './defs.js';
export var selected = null;
export var overlapExists = false;

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
    console.log('selected piece:', selected.parent);

    selected.material.emissive.setHex(0xeeeeee);
    selected.material.emissiveIntensity = 0.5;
    console.log(selected.position)
  }
  else {
    // If no piece is clicked, set selected to null
    if (selected) {
      if (overlapExists){
        selected.material.emissive.setHex(0xFF0000);
        selected.material.emissiveIntensity = 10;
      }
      else{
        selected.material.emissive.set(0x000000); // Reset the previous piece highlight
        selected.material.emissiveIntensity = 0;
      }
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
    const movingObject = selected.parent;
    const prevPosition = movingObject.position.clone();

    const cameraDirection = new THREE.Vector3();
    camera.getWorldDirection(cameraDirection);
    cameraDirection.y = 0;
    cameraDirection.normalize();

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

      
    /* Handle movement to be 2 units in x and z axis. 
    However restrict movement beyond point 0 (under plane) */
    
    movingObject.position.x = Math.round(movingObject.position.x / 2) * 2;
    movingObject.position.y = Math.max(movingObject.position.y, 0);
    movingObject.position.z = Math.round(movingObject.position.z / 2) * 2;

    overlapHandler(selected, piecesGroup)
  }
}

/* Function to use after movement of a piece to handle overlapping  */
function overlapHandler(selected, piecesGroup){
  if (selected){
    if (checkOverlap(selected.parent, piecesGroup)){
      overlapExists = true;
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

export function rotateHandler(piecesGroup) {
  if (selected) {
    rotateWithQuaternion(selected.parent, 'z', 90);
    fixPositionAfterRotation(selected.parent);

    overlapHandler(selected, piecesGroup);

    console.log(`ROTATIONS: ${THREE.MathUtils.radToDeg(selected.parent.rotation.x)} ${THREE.MathUtils.radToDeg(selected.parent.rotation.y)} ${THREE.MathUtils.radToDeg(selected.parent.rotation.z)}`);
  } else {
    console.log('No piece selected for rotation');
  }
}

 /******************************************************************************************
                                     MAIN FUNCTIONS
******************************************************************************************/

function checkOverlap(pieceGroup, piecesGroup, tolerance = 1.9) {
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

export function fixPositionAfterRotation(pieceGroup) {
    const boundingBox = new THREE.Box3().setFromObject(pieceGroup);
    const planeY = 0;

    if (boundingBox.min.y < planeY ) {
      const offsetY = Math.abs(boundingBox.min.y - planeY);
      pieceGroup.position.y += offsetY;
    }

    else if (boundingBox.min.y > planeY) {
      const offsetY = Math.abs(planeY - boundingBox.min.y);
      pieceGroup.position.y -= offsetY;
    }
}

export function createPieces() {
  const piecesGroup = [];
  const radius = 18;                               // Radius of the circle
  const numPieces = Object.entries(pieces).length; // Number of pieces to place
  const angleStep = (2 * Math.PI) / numPieces;     // Angle between each piece

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
    const x = radius * Math.cos(angle);
    const z = radius * Math.sin(angle);
    pieceGroup.position.set(x, 1, z);

    rotateWithQuaternion(pieceGroup, 'x', 90)

    pieceGroup.updateMatrix();

    // Add the piece to piecesGroup
    piecesGroup.push(pieceGroup);

    // Increment the angle for the next piece placement
    angle += angleStep;
  });

  return piecesGroup;
}


function rotateWithQuaternion(object, axis, angle) {
  // Create a quaternion representing the rotation
  const quaternion = new THREE.Quaternion();
  angle = THREE.MathUtils.degToRad(angle);

  // Set quaternion based on the axis and angle
  if (axis === 'x') {
    quaternion.setFromAxisAngle(new THREE.Vector3(1, 0, 0).normalize(), angle);
  }
  else if (axis === 'y') {
    quaternion.setFromAxisAngle(new THREE.Vector3(0, 1, 0).normalize(), angle);
  }
  else if (axis === 'z') {
    quaternion.setFromAxisAngle(new THREE.Vector3(0, 0, 1).normalize(), angle);
  }

  object.quaternion.multiply(quaternion);
}


export function detectPiecesOnPlane(piecesGroup) {
  const piecesInBounds = [];

  // Define the boundaries of the plane
  const boundaryBox = new THREE.Box3(
    new THREE.Vector3(-5, -Infinity, -5),
    new THREE.Vector3(5, Infinity, 5)
  );

  // looping over each piece
  piecesGroup.forEach(pieceGroup => {
    pieceGroup.updateMatrixWorld(true); // Ensure the world matrix is updated

    const groupBoundingBox = new THREE.Box3().setFromObject(pieceGroup);

    if (groupBoundingBox.intersectsBox(boundaryBox)) {
      // Check if all spheres in the group have positions within the boundary
      const allInBounds = pieceGroup.children.every(sphere => {
        const spherePosition = new THREE.Vector3();
        sphere.getWorldPosition(spherePosition);
        return boundaryBox.containsPoint(spherePosition); // Validate position
      });

      if (allInBounds) {
        piecesInBounds.push({
          piece: pieceGroup,
          position: pieceGroup.position.clone(),
        });
      }
    }
  });

  return piecesInBounds.length > 0 ? piecesInBounds : false; // Return pieces within bounds or false
}