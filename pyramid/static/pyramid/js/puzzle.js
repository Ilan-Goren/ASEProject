import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'; // Import OrbitControls
import { DragControls } from 'three/addons/controls/DragControls.js'; // Import DragControls
import { 
  extractDataFromPlane, 
  changeOrientationHandler,
  rotateHandler, 
  onClickHandler, 
  keyboardHandler, 
  selected, 
  createPieces, 
  detectPiecesOnPlane 
} from './functions.js';

// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xefefef);

// Ambient Light setup
const ambientLight = new THREE.AmbientLight(0x404040, 10);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.1);
directionalLight.position.set(5, 5, 5).normalize();
scene.add(directionalLight);

// SpotLight setup
const spotLight = new THREE.SpotLight(0xffffff, 1000);
spotLight.position.set(0, 20, 0);
spotLight.angle = Math.PI / 2;
spotLight.castShadow = true;
scene.add(spotLight);

// Mouse and Raycaster
const mouse = new THREE.Vector2();
const raycaster = new THREE.Raycaster();

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 200 );
camera.position.set(7, 20, 60);  // Initial camera position
camera.lookAt(0,0,0)

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

// Create a texture loader
const textureLoader = new THREE.TextureLoader();
const planeTextureUrl = document.getElementById('texture-url').textContent.trim();
const planeTexture = textureLoader.load(planeTextureUrl, () => {
  console.log("Texture Loaded");
});
planeTexture.wrapS = THREE.RepeatWrapping;
planeTexture.wrapT = THREE.RepeatWrapping;

// Create the main large plane with texture
const planeGeometryMain = new THREE.PlaneGeometry(1000, 1000);
const planeMaterialMain = new THREE.MeshStandardMaterial({
  map: planeTexture,
  side: THREE.FrontSide,
  roughness: 10,
});

const geometry = new THREE.ConeGeometry(15, 20, 4, 1, true);

const material = new THREE.MeshBasicMaterial({
  color: 0xffffff,
  wireframe: true,
});

const wireframePyramid = new THREE.Mesh(geometry, material);

wireframePyramid.rotation.y = Math.PI / 4;
scene.add(wireframePyramid);


const planeMain = new THREE.Mesh(planeGeometryMain, planeMaterialMain);
planeMain.rotation.x = -Math.PI / 2; // Rotate to lay flat
scene.add(planeMain);

// Create the small plane
const planeGeometry = new THREE.PlaneGeometry(10, 10);
const planeMaterial = new THREE.MeshStandardMaterial({
  color: 0x111111,
  side: THREE.DoubleSide,
  roughness: 1, 
  metalness: 0.3,
  emissive: 0x333333
});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.position.set(0, 0, 0);
plane.rotation.x = -Math.PI / 2;
scene.add(plane);

// Create the frame for the small plane
const frameThickness = 0.2;
const frameGeometry = new THREE.BoxGeometry(10 + frameThickness * 2, frameThickness, 10 + frameThickness * 2);
const frameMaterial = new THREE.MeshStandardMaterial({
  color: 0x555555, // Medium gray for the frame
  side: THREE.FrontSide,
  roughness: 0.5,
  metalness: 0.5,
  emissive: 0x222222
});
const frame = new THREE.Mesh(frameGeometry, frameMaterial);
frame.position.set(0, 0.1, 0); // Position slightly above the plane

// Add the frame to the scene
scene.add(frame);

const piecesGroup = createPieces();
piecesGroup.forEach(piece  => {
  scene.add(piece);
})

 /******************************************************************************************
                                        DRAG CONTROLS
******************************************************************************************/

// piecesGroup.forEach(piece => {
//   const dragControls = new DragControls(piece.children, camera, renderer.domElement);
//   dragControls.transformGroup = true;

//   let initialY = 1; // To store the initial Y position
//   dragControls.addEventListener('dragstart', (event) => {
//     controls.enabled = false;
//     const object = event.object;
//     initialY = object.position.y; // Store the Y position when the drag starts
//   });

//   dragControls.addEventListener('dragend', () => {
//     controls.enabled = true;
//   });

//   dragControls.addEventListener('drag', (event) => {
//     const object = event.object;

//     // Allow movement in X and Z axis
//     object.position.x = Math.round(object.position.x / 2) * 2;
//     object.position.z = Math.round(object.position.z / 2) * 2;
//     object.position.y = initialY; // Do not change Y on drag
//   });
// })

 /******************************************************************************************
                                    BUTTONS EVENT LISTENERS
******************************************************************************************/

const toggleButton = document.getElementById('tc');
toggleButton.addEventListener('click', ()=>{
  controls.enabled = !controls.enabled;
})

const resetButton = document.getElementById('reset-piece');
resetButton.addEventListener('click', ()=>{
  window.location.reload()
})

let isPieceFlat = true;
const changeOr = document.getElementById('change-orientation');
changeOr.addEventListener('click', () => {
  isPieceFlat = changeOrientationHandler(piecesGroup, isPieceFlat);
});



const rotateButton = document.getElementById('rotate');
rotateButton.addEventListener('click', () => rotateHandler(piecesGroup, isPieceFlat));

const getSolutionButton = document.getElementById('get_sol');
getSolutionButton.addEventListener('click', () => {
  const piecesOnPlane = detectPiecesOnPlane(piecesGroup);

  // Extract the data from the plane
  const [pyramid, piecesPlaced] = extractDataFromPlane(piecesOnPlane, 5);

  fetch("pyramid_partial_config_solutions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ pyramid: pyramid,
      piecesPlaced, piecesPlaced
     }) // Convert data to JSON string
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
});



document.addEventListener('keydown', (event) => keyboardHandler(event, camera, piecesGroup));

renderer.domElement.addEventListener('click', (event) => onClickHandler(
  event, piecesGroup, raycaster, mouse, camera
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
  renderer.render(scene, camera);
  requestAnimationFrame(renderLoop);

};

renderLoop();