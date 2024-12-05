import * as THREE from 'three';
import { colorMapping } from './defs.js';

export var selected = null;
export var overlapExists = false;

/* 
 * Creates a tetrahedron-shaped group of spheres based on the provided data.
 * 
 * Args:
 *   data (Array): A 3D array representing the layers, rows, and columns of the tetrahedron, where each value corresponds 
 *                 to a piece identifier (non-zero values are valid pieces).
 * 
 * Returns:
 *   THREE.Group: A group containing all the spheres that form the tetrahedron.
 */
export function createTetrahedron(data) {
  const tetrahedronGroup = new THREE.Group();
  const layerCount = data.length;
  
  const spacing = 2;
  const height = layerCount * (spacing - 0.5);

  data.forEach((layer, layerIndex) => {
    const layerHeight = (layerIndex / (layerCount - 1)) * height;
    
    layer.forEach((row, rowIndex) => {
      const rowLength = row.length;

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

          const x = (colIndex - rowLength / 2) * (spacing);
          const y = layerHeight;
          const z = (rowIndex - (layer.length / 2)) * (spacing - 0.4) - (layerHeight/8);

          sphere.position.set(x, y, z);
          tetrahedronGroup.add(sphere);
        }
      });
    });
  });

  return tetrahedronGroup;
}

/* 
 * Adjusts the spacing between layers in a pyramid group based on the specified orientation.
 * 
 * Args:
 *   pyramidGroup (THREE.Group): The group of spheres representing the pyramid.
 *   orientation (string, optional): The spacing orientation, either 'vertical' or 'horizontal'. Defaults to 'vertical'.
 *
 * Returns:
 *   THREE.Group: A clone of the adjusted pyramid group.
 */
export function adjustPyramidSpacing(pyramidGroup, orientation = 'vertical') {
  pyramidGroup.children.forEach((sphere) => {
      const { x, y, z } = sphere.position;
      if (orientation === 'vertical') {
          sphere.position.set(x, y + (y) * 2, z);
      } else if (orientation === 'horizontal') {
        const diagonalLayer = (x + z / 4);
        sphere.position.set(
            x + diagonalLayer,
            y ,
            z + diagonalLayer);
        }
  });
  return pyramidGroup.clone()
}

/* 
 * Removes all groups from the scene.
 * 
 * Args:
 *   scene (THREE.Scene): The scene from which to remove all groups.
 */
export function removeAllGroupsFromScene(scene) {
  scene.children.forEach(child => {
      if (child instanceof THREE.Group) {
          scene.remove(child);
      }
  });
}

/* 
 * Sets the emissive properties for the selected piece group based on the state.
 *
 * Args:
 *   selected (THREE.Group): The selected piece group whose spheres will have their emissive properties modified.
 *   state (boolean): Determines whether to enable or disable the emissive effect. 
 *                    - If true, sets the emissive color to a light gray with a moderate intensity.
 *                    - If false, resets the emissive color to black and intensity to 0.
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

/* 
 * Handles button actions to adjust the view of the pyramid in the scene.
 *
 * Args:
 *   camera (THREE.Camera): The camera object that will be used to update the view.
 *   scene (THREE.Scene): The scene where the pyramid is rendered.
 *   pyramidClone (THREE.Group): The cloned pyramid group to be added to the scene.
 *   pyramidGroup (THREE.Group): The original pyramid group from which the clone is created.
 *   view (string): The current view mode, which can be 'h' for horizontal, 'v' for vertical, or 'n' for normal.
 */
export function buttonHandler (camera, scene, pyramidClone, pyramidGroup, view){
  var pyramidClone = pyramidGroup.clone();
  
  switch (view){
    case 'h':
      removeAllGroupsFromScene(scene);
      adjustPyramidSpacing(pyramidClone, 'horizontal');
      scene.add(pyramidClone)
      view = 'h';
      break;
    case 'v':
      removeAllGroupsFromScene(scene);
      adjustPyramidSpacing(pyramidClone, 'vertical');
      scene.add(pyramidClone)
      view = 'h';
      break;
    case 'n':
      removeAllGroupsFromScene(scene);
      scene.add(pyramidClone);
      view = 'n';
      break;
  }
    
    pyramidClone.position.set(0, 0, 0);
    camera.lookAt(0, 0, 0);
}