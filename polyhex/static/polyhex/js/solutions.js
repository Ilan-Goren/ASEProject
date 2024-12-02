import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'; // Import OrbitControls
import { 
  createTetrahedron, 
  buttonHandler,
  setEmissiveForSelected 
} from './functions.js';

const allPyramids = []
var selected = null;

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
camera.position.set(10, 30, -20);  // Initial camera position
camera.lookAt(0,0,0)

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

const forestWidth = Math.max(dataFromBackend.length, 150);
const forestDepth = Math.max(dataFromBackend.length, 150);

const numColumns = Math.ceil(Math.sqrt(numPyramids));
const numRows = Math.ceil(numPyramids / numColumns);

const spacingX = forestWidth / numColumns;
const spacingZ = forestDepth / numRows;

var loadingRadius = 150;
const loadedPyramids = new Map();

function updatePyramids() {
  const cameraFrustum = new THREE.Frustum();
  const cameraMatrix = new THREE.Matrix4();
  
  cameraMatrix.multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse);
  cameraFrustum.setFromProjectionMatrix(cameraMatrix);

  const cameraPosition = camera.position;

  dataFromBackend.forEach((solution, index) => {
      const columnIndex = index % numColumns;
      const rowIndex = Math.floor(index / numColumns);

      const x = (columnIndex * spacingX) - (forestWidth / 2);
      const z = (rowIndex * spacingZ) - (forestDepth / 2);
      const pyramidPosition = new THREE.Vector3(x, 1, z);

      const distance = pyramidPosition.distanceTo(cameraPosition);

      if (distance <= loadingRadius) {
          if (cameraFrustum.containsPoint(pyramidPosition)) {
              if (!loadedPyramids.has(index)) {
                  const pyramidGroup = createTetrahedron(solution);
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
    alert('Please choose a valid radius. (50 to 1000)');
  }
}

 /******************************************************************************************
                                     DISPLAY A PYRAMID
******************************************************************************************/
var overlayOpened = false;

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

function closeOverlay(){
  overlay.style.display = 'none';
  overlayOpened = false;
}

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