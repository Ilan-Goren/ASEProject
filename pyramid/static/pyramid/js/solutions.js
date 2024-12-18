import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'; // Import OrbitControls
import { createPyramid, adjustPyramidSpacing, removeAllGroupsFromScene } from './functions.js';
import { setEmissiveForSelected } from './helpers.js';

const allPyramids = []
var selected = null;


/******************************************************************************************
                                    ENVIROMENT SETUP  
******************************************************************************************/

// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xefefef);

// Ambient Light setup
const ambientLight = new THREE.AmbientLight(0x404040, 5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(5, 5, 5).normalize();
scene.add(directionalLight);

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 400 );
camera.position.set(7, 20, 60);  // Initial camera position
camera.lookAt(0,0,0)

function resetCamera() {
  camera.position.set(7, 20, 60);
  camera.lookAt(0, 0, 0);
  controls.reset();
}

// Add a reset button in the HTML and attach event listener
const resetCameraButton = document.getElementById('reset-camera');
resetCameraButton.addEventListener('click', resetCamera);

// Mouse and Raycaster setup
const mouse = new THREE.Vector2();
const raycaster = new THREE.Raycaster();

// Renderer setup
const canvas = document.querySelector('canvas.threejs');
const renderer = new THREE.WebGLRenderer({ 
  antialias: true,
  canvas: canvas
 });
renderer.setSize(window.innerWidth, window.innerHeight);


// OrbitControls setup
const controls = new OrbitControls(camera, renderer.domElement);

controls.enableDamping = true;  // Smooth movement
controls.dampingFactor = 0.25;
controls.screenSpacePanning = false;
controls.maxPolarAngle = Math.PI / 2;

const textureLoader = new THREE.TextureLoader();

const planeTextureUrl = document.getElementById('texture-url').textContent.trim();

const planeTexture = textureLoader.load(planeTextureUrl);

planeTexture.wrapS = THREE.RepeatWrapping;
planeTexture.wrapT = THREE.RepeatWrapping;

// Create the main large plane with texture
const planeGeometryMain = new THREE.PlaneGeometry(2000, 2000);
const planeMaterialMain = new THREE.MeshStandardMaterial({
  map: planeTexture,     // Apply the texture map
  side: THREE.FrontSide, // Only show the front side
  roughness: 10,         // Slightly rough surface
});

const planeMain = new THREE.Mesh(planeGeometryMain, planeMaterialMain);
planeMain.rotation.x = -Math.PI / 2; // Rotate to lay flat
scene.add(planeMain);

/******************************************************************************************
                                     SELECTING PYRAMIDS
******************************************************************************************/

function onClickHandler(event) {

  // Get mouse position relative to the canvas
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);

  // Check intersections with pieces in piecesGroup
  const intersects = raycaster.intersectObjects(allPyramids, true);

  if (intersects.length > 0) {
    // if there is already a piece selected
    if (selected){
      setEmissiveForSelected(selected, false);
    }

    selected = intersects[0].object;
    console.log('selected piece:', selected.parent);

    setEmissiveForSelected(selected, true);
  }
  else {
    setEmissiveForSelected(selected, false);
    selected = null;
    console.log('nothing selected');
  }
}

 /******************************************************************************************
                                     DISPLAYING PYRAMIDS
******************************************************************************************/

const dataFromBackend = JSON.parse(document.getElementById('pyramid-data').textContent);

const numPyramids = dataFromBackend.length;

const baseDimension = Math.max(50, Math.sqrt(numPyramids) * 15);

const scaleFactor = Math.max(0.1, 10 / numPyramids);
const forestWidth = baseDimension + numPyramids * scaleFactor;
const forestDepth = baseDimension + numPyramids * scaleFactor;

const numColumns = Math.ceil(Math.sqrt(numPyramids));
const numRows = Math.ceil(numPyramids / numColumns);

const spacingX = forestWidth / numColumns;
const spacingZ = forestDepth / numRows;

var loadingRadius = 100;
const loadedPyramids = new Map();

const totalSolutions = dataFromBackend.length;

// Global variables to track pagination
let currentPageIndex = 0;
let solutionsPerPage = 9;
const maxSolutionsPerPage = totalSolutions;
const minSolutionsPerPage = 1;

function updatePyramids() {
  const startIndex = currentPageIndex * solutionsPerPage;
  const endIndex = Math.min(startIndex + solutionsPerPage, dataFromBackend.length);
  const gridColumns = Math.ceil(Math.sqrt(solutionsPerPage));

  const cameraFrustum = new THREE.Frustum();
  const cameraMatrix = new THREE.Matrix4();

  cameraMatrix.multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse);
  cameraFrustum.setFromProjectionMatrix(cameraMatrix);

  const cameraPosition = camera.position;

  dataFromBackend.slice(startIndex, endIndex).forEach((solution, localIndex) => {
      const index = startIndex + localIndex;
      const columnIndex = localIndex % gridColumns;
      const rowIndex = Math.floor(localIndex / gridColumns);

      // Use same grid calculation as displayCurrentPage
      const x = (columnIndex - (gridColumns - 1) / 2) * spacingX;
      const z = (rowIndex - (gridColumns - 1) / 2) * spacingZ;

      const pyramidPosition = new THREE.Vector3(x, 1, z);

      const distance = pyramidPosition.distanceTo(cameraPosition);

      if (distance <= loadingRadius) {
          if (cameraFrustum.containsPoint(pyramidPosition)) {
              if (!loadedPyramids.has(index)) {
                  const pyramidGroup = createPyramid(solution);
                  allPyramids.push(pyramidGroup);
                  pyramidGroup.position.set(x, 1, z);
                  scene.add(pyramidGroup);
                  loadedPyramids.set(index, pyramidGroup);
              }
          }
      }

      if (distance > loadingRadius || !cameraFrustum.containsPoint(pyramidPosition)) {
          if (loadedPyramids.has(index)) {
              const pyramidToRemove = loadedPyramids.get(index);
              const indexToRemove = allPyramids.indexOf(pyramidToRemove);
              if (indexToRemove > -1) {
                allPyramids.splice(indexToRemove, 1);  // Remove the pyramid from the array
              }
              scene.remove(pyramidToRemove);
              loadedPyramids.delete(index);
          }
      }
  });
}

const changeRadiusButton = document.getElementById('applyChanges');
changeRadiusButton.addEventListener('click', changeRadius);

function changeRadius() {
  const inputElement = document.getElementById('radiusInput');
  const inputValue = inputElement.value;

  if (1000 >= inputValue && inputValue >= 50) {
    loadingRadius = inputValue;

  } else {
    alert('Please choose a valid radius.');
  }
}

 /******************************************************************************************
                                     DISPLAY A PYRAMID
******************************************************************************************/
var overlayOpened = false;
/*
 * Handles button interactions for changing the pyramid view in the overlay.
 *
 * Args:
 *   camera (THREE.Camera): The camera used for rendering the overlay scene.
 *   scene (THREE.Scene): The overlay scene where the pyramid is rendered.
 *   pyramidClone (THREE.Group): A clone of the pyramid group in the overlay scene.
 *   pyramidGroup (THREE.Group): The original pyramid group used for cloning.
 *   view (string): Determines the desired view ('h' for horizontal, 'v' for vertical, 'n' for normal).
 *
 * Functionality:
 * - Clones the original pyramid group to ensure the original structure remains unchanged.
 * - Removes all existing groups from the scene using `removeAllGroupsFromScene`.
 * - Adjusts pyramid spacing based on the specified view:
 *   - 'h': Adjust spacing for horizontal display.
 *   - 'v': Adjust spacing for vertical display.
 *   - 'n': Default view with no spacing adjustments.
 * - Adds the adjusted or cloned pyramid group back to the scene.
 * - Resets the pyramid's position to the origin (0, 0, 0).
 * - Sets the camera to look at the center of the pyramid for a proper view.
 */
function buttonHandler (camera, scene, pyramidClone, pyramidGroup, view){
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

const viewPyramidButton = document.getElementById('view-pyramid');
// Horizontal view
const hbutton = document.getElementById('h-view');
// Vertical view
const vbutton = document.getElementById('v-view');
// Normal view
const nbutton = document.getElementById('n-view');
// Overlay Section
const overlay = document.getElementById('overlay');
// Close Overlay button
const closeOverlayButton = document.getElementById('close-view');
// Overlay Canvas
const overlayCanvas = document.getElementById('overlay-canvas');

closeOverlayButton.addEventListener('click', closeOverlay)
viewPyramidButton.addEventListener('click', () => showOverlay(selected));

function showOverlay(selected) {
  if (selected){
    selected.parent.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.material.emissive.set(0x000000);
        child.material.emissiveIntensity = 0;
      }
    });
    
    let pyramidGroup = selected.parent
    overlay.style.display = 'block';
    overlayOpened = true;
    renderPyramidInOverlay(pyramidGroup);
  }
}
/**
 * Closes the overlay and updates the state to indicate it is no longer open.
 *
 * Functionality:
 * - Sets the overlay element's display style to 'none', effectively hiding it.
 * - Updates the `overlayOpened` flag to `false` to reflect the closed state.
 */
function closeOverlay(){
  overlay.style.display = 'none';
  overlayOpened = false;
}

/*
 * Renders a pyramid structure in an overlay canvas with interactive controls.
 *
 * Args:
 *   pyramidGroup (THREE.Group): The group containing the pyramid structure to be rendered.
 *
 * Features:
 * - Creates an independent `THREE.Scene` for the overlay.
 * - Sets up a new camera and renderer for the overlay display.
 * - Adds lighting, including ambient and directional lights, to enhance visibility.
 * - Utilizes `OrbitControls` for user interaction with the 3D overlay (rotation, zooming, etc.).
 * - Clones the provided `pyramidGroup` to avoid modifying the original group.
 * - Adds event listeners for button interactions (`hbutton`, `nbutton`, `vbutton`) to trigger specific handlers.
 * - Ensures smooth rendering via `requestAnimationFrame` when the overlay is open.
 */

function renderPyramidInOverlay(pyramidGroup) {
  const overlayScene = new THREE.Scene();
  overlayScene.background = new THREE.Color(0xefefef);
  
  const overlayCamera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  
  const overlayRenderer = new THREE.WebGLRenderer({
    canvas: overlayCanvas,
    antialias: true
  });

  overlayRenderer.setSize(window.innerWidth, window.innerHeight);

  // Set up lighting
  const overlayLight = new THREE.AmbientLight(0x404040, 5);
  overlayScene.add(overlayLight);
  
  const overlayDirectionalLight = new THREE.DirectionalLight(0xffffff, 2);
  overlayScene.add(overlayDirectionalLight);

  // OrbitControls setup
  const controls = new OrbitControls(overlayCamera, overlayRenderer.domElement);

  controls.enableDamping = true;  // Smooth movement
  controls.dampingFactor = 0.25;
  controls.screenSpacePanning = false;

  // Camera setup
  overlayCamera.position.set(0, 10, 40);
  overlayCamera.lookAt(0, 0, 0);

  // Clone the pyramid group and add it to the scene
  let pyramidClone = pyramidGroup.clone();
  pyramidClone.position.set(0, 0, 0);
  overlayScene.add(pyramidClone);


  hbutton.addEventListener('click', () => {
    buttonHandler(overlayCamera, overlayScene, pyramidClone, pyramidGroup, 'h')
})

  nbutton.addEventListener('click', () => {
    buttonHandler(overlayCamera, overlayScene, pyramidClone, pyramidGroup, 'n')
    })
  
  vbutton.addEventListener('click', () => {
    buttonHandler(overlayCamera, overlayScene, pyramidClone, pyramidGroup, 'v')
  })

  // Render the pyramid
  function animate() {
      if (!overlayOpened) return;
      requestAnimationFrame(animate);
      controls.update();
      overlayRenderer.render(overlayScene, overlayCamera);
  }
    animate();
}

 /******************************************************************************************
                                     MAIN
******************************************************************************************/

renderer.domElement.addEventListener('click', (event) => onClickHandler(
  event
));

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
  
// Render loop
const renderLoop = () => {
  controls.update();
  updatePyramids();
  renderer.render(scene, camera);
  requestAnimationFrame(renderLoop);
};

renderLoop();

function createBoundingBox() {
  // Calculate grid dimensions as a square
  const gridColumns = Math.ceil(Math.sqrt(solutionsPerPage));
  const gridRows = gridColumns;

  const gridWidth = spacingX * gridColumns;
  const gridDepth = spacingZ * gridRows;

  const edges = new THREE.EdgesGeometry(
    new THREE.BoxGeometry(gridWidth, 10, gridDepth)
  );

  const boundingBoxLines = new THREE.LineSegments(
    edges,
    new THREE.LineBasicMaterial({
      color: 0x00ff00,
      linewidth: 2
    })
  );

  boundingBoxLines.position.set(0, 0.5, 0);  // Center of the grid
  scene.add(boundingBoxLines);
  return boundingBoxLines;
}

function updatePageInfo() {
  const pageInfoElement = document.getElementById('page-info');
  const totalPages = Math.ceil(totalSolutions / solutionsPerPage);
  pageInfoElement.textContent = `Page ${currentPageIndex + 1} of ${totalPages}`;
}

function displayCurrentPage() {
// Clear existing pyramids
  loadedPyramids.forEach((pyramidGroup) => {
    scene.remove(pyramidGroup);
  });
  loadedPyramids.clear();
  allPyramids.length = 0;

  // Calculate grid dimensions as a square
  const gridColumns = Math.ceil(Math.sqrt(solutionsPerPage));
  const gridRows = gridColumns;

  // Calculate start and end indices
  const startIndex = currentPageIndex * solutionsPerPage;
  const endIndex = Math.min(startIndex + solutionsPerPage, totalSolutions);

  for (let i = startIndex; i < endIndex; i++) {
    const solution = dataFromBackend[i];
    const localIndex = i - startIndex;

    const columnIndex = localIndex % gridColumns;
    const rowIndex = Math.floor(localIndex / gridColumns);

    // Adjust spacing to create a square grid
    const x = (columnIndex - (gridColumns - 1) / 2) * spacingX;
    const z = (rowIndex - (gridRows - 1) / 2) * spacingZ;

    const pyramidGroup = createPyramid(solution);
    allPyramids.push(pyramidGroup);
    pyramidGroup.position.set(x, 1, z);
    scene.add(pyramidGroup);
    loadedPyramids.set(i, pyramidGroup);
  }

  // Update pagination and page info
  updatePaginationButtons();
  updatePageInfo();

  // Update or create bounding box
  updateBoundingBox();
}

function updatePaginationButtons() {
  const prevPageButton = document.getElementById('prev-page');
  const nextPageButton = document.getElementById('next-page');

  prevPageButton.disabled = (currentPageIndex === 0);
  nextPageButton.disabled = ((currentPageIndex + 1) * solutionsPerPage >= totalSolutions);
}

// Add event listeners for pagination
document.getElementById('prev-page').addEventListener('click', () => {
  if (currentPageIndex > 0) {
    currentPageIndex--;
    displayCurrentPage();
  }
});

document.getElementById('next-page').addEventListener('click', () => {
  if ((currentPageIndex + 1) * solutionsPerPage < totalSolutions) {
    currentPageIndex++;
    displayCurrentPage();
  }
});

function updatePageSize() {
  const pageSizeInput = document.getElementById('page-size-input');
  const newPageSize = parseInt(pageSizeInput.value, 10);

  if (newPageSize >= minSolutionsPerPage && newPageSize <= maxSolutionsPerPage) {
    solutionsPerPage = newPageSize;
    currentPageIndex = 0;  // Reset to first page

    // Reload current page with new size
    displayCurrentPage();

    // Update the page size message
    updatePageSizeMessage();

  } else {
    alert(`Please enter a page size between ${minSolutionsPerPage} and ${maxSolutionsPerPage}.`);
  }


}

function updateBoundingBox() {
  // Calculate grid dimensions as a square
  const gridColumns = Math.ceil(Math.sqrt(solutionsPerPage));
  const gridRows = gridColumns;

  const gridWidth = spacingX * gridColumns;
  const gridDepth = spacingZ * gridRows;

  // If bounding box doesn't exist, create it
  if (!window.existingBoundingBox) {
    const edges = new THREE.EdgesGeometry(
      new THREE.BoxGeometry(gridWidth, 10, gridDepth)
    );

    window.existingBoundingBox = new THREE.LineSegments(
      edges,
      new THREE.LineBasicMaterial({
        color: 0x00ff00,
        linewidth: 2
      })
    );
    window.existingBoundingBox.position.set(0, 0.5, 0);  // Center of the grid
    scene.add(window.existingBoundingBox);
  } else {
    // Resize existing bounding box
    const newGeometry = new THREE.EdgesGeometry(
      new THREE.BoxGeometry(gridWidth, 10, gridDepth)
    );

    // Dispose of old geometry
    window.existingBoundingBox.geometry.dispose();

    // Replace with new geometry
    window.existingBoundingBox.geometry = newGeometry;
  }
}

function updatePageSizeMessage() {
  const pageSizeMessage = document.getElementById('pageStatusMessage');
  if (pageSizeMessage) {
    pageSizeMessage.textContent = `Specify page size (1-${totalSolutions}):`;
  }
}

// Add event listener for page size apply button
document.getElementById('page-size-apply').addEventListener('click', updatePageSize);


function debounce(func, delay) {
  let timeoutId;
  return function() {
    const context = this;
    const args = arguments;
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(context, args);
    }, delay);
  };
}

// Apply to resize event
const debouncedResize = debounce(() => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}, 250);

window.addEventListener('resize', debouncedResize);


// Initial page load
displayCurrentPage();

updatePageSizeMessage();