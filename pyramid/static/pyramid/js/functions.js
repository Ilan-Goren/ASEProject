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
    if (selected && !selected.parent.halfIn){
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
      if (!overlapExists && !selected.parent.halfIn){
          selected.material.emissive.set(0x000000);
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
}

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
          movingObject.position.y = Math.max(movingObject.position.y - (moveAmount + 1), 0); // Ensure Y doesn't go below 0
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
    overlapHandler(selected, piecesGroup);
    partiallyInsideBoudariesHandler(selected);
    
  }
}

/* Function to use after movement of a piece to handle overlapping  */
function overlapHandler(selected, piecesGroup){
  if (selected){
    if (checkOverlap(selected.parent, piecesGroup)){
      overlapExists = true;
      updateStatusMessage('True', 'none');
      selected.material.emissive.setHex(0xFF0000);
      selected.material.emissiveIntensity = 20;
    }
    else{
      updateStatusMessage('False', 'none');
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

function partiallyInsideBoudariesHandler(selected){
  if (selected.parent.halfIn){
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

export function rotateHandler(piecesGroup, isPieceFlat) {
  if (selected) {
    if (isPieceFlat){
      rotateWithQuaternion(selected.parent, 'z', 90);
    }
    else {
      rotateWithQuaternion(selected.parent, 'y', 90);
    }
    fixPositionAfterRotation(selected.parent);

    insideBoundariesHandler(piecesGroup);
    
    overlapHandler(selected, piecesGroup);
    partiallyInsideBoudariesHandler(selected);

    console.log(`ROTATIONS: ${THREE.MathUtils.radToDeg(selected.parent.rotation.x)} ${THREE.MathUtils.radToDeg(selected.parent.rotation.y)} ${THREE.MathUtils.radToDeg(selected.parent.rotation.z)}`);
  } else {
    console.log('No piece selected for rotation');
  }
}

export function changeOrientationHandler(piecesGroup, isPieceFlat) {
  if (selected) {
    const rotationAngleX = isPieceFlat ? -90 : 90;
    const rotationAngleY = isPieceFlat ? -45 : 45;
    if (isPieceFlat){
      selected.parent.rotateX(THREE.MathUtils.degToRad(rotationAngleX));
      selected.parent.rotateY(THREE.MathUtils.degToRad(rotationAngleY));
    }
    else {
      selected.parent.rotateY(THREE.MathUtils.degToRad(rotationAngleY));
      selected.parent.rotateX(THREE.MathUtils.degToRad(rotationAngleX));
    }
    
    fixPositionAfterRotation(selected.parent)
    insideBoundariesHandler(piecesGroup);
    overlapHandler(selected, piecesGroup);
    partiallyInsideBoudariesHandler(selected);
    isPieceFlat = !isPieceFlat;
  }
  return isPieceFlat;
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
    pieceGroup.name = key;

    // Create spheres
    value.forEach(pos => {
      const sphereGeometry = new THREE.SphereGeometry(1, 16, 16);
      const sphereMesh = new THREE.Mesh(sphereGeometry, material);
      sphereMesh.position.set(pos[0], pos[1], pos[2]);
      pieceGroup.add(sphereMesh); // Add sphere to this piece's group
    });

    // Position the group in a circle
    const x = Math.round(radius * Math.cos(angle));
    const z = Math.round(radius * Math.sin(angle));
    pieceGroup.position.set(x, 1, z);
    rotateWithQuaternion(pieceGroup, 'x', 90)

    pieceGroup.updateMatrix();
    // Add the piece to piecesGroup

    pieceGroup.halfIn = false;
    piecesGroup.push(pieceGroup);

    // Increment the angle for the next piece placement
    angle += angleStep;
  });

  return piecesGroup;
}


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
      let spheresGroup = []
      // Check if all spheres in the group have positions within the boundary
      const allInBounds = pieceGroup.children.every(sphere => {
        const spherePosition = new THREE.Vector3();
        sphere.getWorldPosition(spherePosition);

        spheresGroup.push({
          piece: pieceGroup.name,
          position: spherePosition
      })
        return boundaryBox.containsPoint(spherePosition); // Validate position
      });

      if (allInBounds) {
        piecesInBounds.push(spheresGroup);
      }
    }
  });

  return piecesInBounds.length > 0 ? piecesInBounds : false; // Return pieces within bounds or false
}


export function insideBoundariesHandler(piecesGroup) {
  const piecesCorrectlyPlaced = [];

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

      // Check if all spheres in the group have positions within the boundary
      const allInBounds = pieceGroup.children.every(sphere => {
        const spherePosition = new THREE.Vector3();
        sphere.getWorldPosition(spherePosition);

        const y_pos = spherePosition.y
        let boundryPoint = 5 - Math.round((y_pos - 1) / 2) - 1
        console.log(boundryPoint);
        console.log(spherePosition)
        const boundaryBox = new THREE.Box3(
          new THREE.Vector3(-boundryPoint - 0.1, -Infinity, -boundryPoint - 0.1),
          new THREE.Vector3(boundryPoint + 0.1, Infinity, boundryPoint + 0.1)
        );

        return boundaryBox.containsPoint(spherePosition); // Validate position
      });

      if (allInBounds) {
        pieceGroup.halfIn = false;

        pieceGroup.children.forEach(child => {
          const spherePosition = new THREE.Vector3();
          child.getWorldPosition(spherePosition);
          console.log(spherePosition);
        })

        piecesCorrectlyPlaced.push(pieceGroup);
      }
      else {
        pieceGroup.halfIn = true;
      }
    }
    else {
      pieceGroup.halfIn = false;
    }
  });
  updateStatusMessage(false, piecesCorrectlyPlaced.length);


  return piecesCorrectlyPlaced.length > 0 ? piecesCorrectlyPlaced : false;
}

function updateStatusMessage(message1='none', message2='none') {
  if (message1 != 'none'){
    document.getElementById('statusMessage1').textContent = `Overlap status: ${message1}`;
  }
  if (message2 != 'none'){
    document.getElementById('statusMessage2').textContent = `Number of pieces within bounds ${message2}`;
  }
}


export function extractDataFromPlane(input, piecesGroup) {
  if (overlapExists){
    return false
  }

  piecesGroup.forEach(piece => {
    if (piece.halfIn){
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

  return [pyramid, piecesAlreadyPlaced];
}