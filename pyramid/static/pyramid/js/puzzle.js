import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'; // Import OrbitControls
import { 
  extractDataFromPlane, 
  changeOrientationHandler,
  rotateHandler, 
  flipHandler, 
  onClickHandler, 
  keyboardHandler,
  createPieces, 
  insideBoundariesHandler
} from './functions.js';

/******************************************************************************************
                                       SETUP
******************************************************************************************/

/** 
 * Scene Setup
 * ===========
 * - A new scene is created to hold all 3D objects.
 * - The background color is set to a light gray.
 */
const scene = new THREE.Scene();  // new scene
scene.background = new THREE.Color(0xefefef); // set background for the scene

/** 
 * Ambient Light Setup
 * ===================
 * - Adds soft ambient lighting to the scene.
 * - The light color is medium gray (0x404040), and intensity is set to 10.
 */
const ambientLight = new THREE.AmbientLight(0x404040, 10);
scene.add(ambientLight);

/** 
 * Directional Light Setup
 * =======================
 * - A directional light simulates sunlight.
 * - Position is set to (5, 5, 5) and normalized.
 * - Light intensity is set to a low value of 0.1.
 */
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.1);
directionalLight.position.set(5, 5, 5).normalize();
scene.add(directionalLight);

/** 
 * SpotLight Setup
 * ===============
 * - Adds a spotlight with high intensity (1000).
 * - Positioned at (0, 20, 0) with an angle of 90 degrees.
 * - Shadow casting is enabled for realistic lighting effects.
 */
const spotLight = new THREE.SpotLight(0xffffff, 1000);
spotLight.position.set(0, 20, 0);
spotLight.angle = Math.PI / 2;
spotLight.castShadow = true;
scene.add(spotLight);

/** 
 * Mouse and Raycaster Setup
 * =========================
 * - Creates a 2D vector to track mouse position.
 * - Initializes a Raycaster for object interaction in the scene.
 */
const mouse = new THREE.Vector2();
const raycaster = new THREE.Raycaster();

/** 
 * Camera Setup
 * ============
 * - A Perspective Camera is created with a 75-degree field of view.
 * - Aspect ratio matches the browser window dimensions.
 * - Positioned at (7, 20, 60) and looking at the origin.
 */
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 200 );
camera.position.set(7, 20, 60);  // Initial camera position
camera.lookAt(0, 0, 0);

/** 
 * Renderer Setup
 * ==============
 * - A WebGL renderer is created with anti-aliasing enabled.
 * - The size of the renderer matches the browser window.
 * - Links the renderer to a canvas element with the class `threejs`.
 */
const canvas = document.querySelector('canvas.threejs');
const renderer = new THREE.WebGLRenderer({ 
  antialias: true,
  canvas: canvas
});
renderer.setSize(window.innerWidth, window.innerHeight);

/** 
 * OrbitControls Setup
 * ===================
 * - OrbitControls allow interactive camera movement.
 * - Smooth damping is enabled with a factor of 0.25.
 * - Limits vertical rotation to avoid viewing below the plane.
 */
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;  // Smooth movement
controls.dampingFactor = 0.25;
controls.screenSpacePanning = false;
controls.maxPolarAngle = Math.PI / 2; // Do not allow to see below the plane

/** 
 * Large Plane with Texture
 * ========================
 * - A texture loader is used to load an image as the plane texture.
 * - The plane is large (1000x1000) and uses a repeating texture.
 */
const textureLoader = new THREE.TextureLoader(); // Create a texture loader
const planeTextureUrl = document.getElementById('texture-url').textContent.trim();
const planeTexture = textureLoader.load(planeTextureUrl);
planeTexture.wrapS = THREE.RepeatWrapping;
planeTexture.wrapT = THREE.RepeatWrapping;

// Create the main large plane with texture
const planeGeometryMain = new THREE.PlaneGeometry(1000, 1000);
const planeMaterialMain = new THREE.MeshStandardMaterial({
  map: planeTexture,
  side: THREE.FrontSide,
  roughness: 10,
});
const planeMain = new THREE.Mesh(planeGeometryMain, planeMaterialMain);
planeMain.rotation.x = -Math.PI / 2; // Rotate to lay flat
scene.add(planeMain);

/** 
 * Wireframe Pyramid Frame
 * =======================
 * - A wireframe pyramid is created using a cone geometry.
 * - Positioned to align with the plane and adds visual guidance.
 */
const geometry = new THREE.ConeGeometry(15, 20, 4, 1, true);
const material = new THREE.MeshBasicMaterial({
  color: 0xffffff, // color of the frame (white)
  wireframe: true,
});
const wireframePyramid = new THREE.Mesh(geometry, material);
wireframePyramid.rotation.y = Math.PI / 4; // adjust rotation to the plane
scene.add(wireframePyramid); // add frame to the scene

/** 
 * Small Plane
 * ===========
 * - A small plane (10x10) is created for interaction or placement.
 * - Uses a double-sided material with slight emissive lighting.
 */
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

/** 
 * Frame for Small Plane
 * =====================
 * - A rectangular frame surrounds the small plane.
 * - Positioned slightly above the plane for better visibility.
 */
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
scene.add(frame); // Add the frame to the scene

const piecesGroup = createPieces();
piecesGroup.forEach(piece  => {
  scene.add(piece);
});


/******************************************************************************************
                                   EVENT LISTENERS
******************************************************************************************/
/**
 * Reset Button
 * Reloads the page to reset everything to the original placement.
 */
const resetButton = document.getElementById('reset-piece');
resetButton.addEventListener('click', () => {
  window.location.reload();
});

/**
 * Change Orientation Button
 * Toggles the orientation of a piece between flat and upright.
 * Tracks the current orientation using the `isPieceFlat` flag.
 * Calls the `changeOrientationHandler` function to update orientation.
 */
let isPieceFlat = true;
const changeOr = document.getElementById('change-orientation');
changeOr.addEventListener('click', () => {
  isPieceFlat = changeOrientationHandler(piecesGroup, isPieceFlat);
});

/**
 * Rotate Button
 * Rotates a piece by 90 degrees in the scene.
 * Calls the `rotateHandler` function with the current orientation.
 */
const rotateButton = document.getElementById('rotate');
rotateButton.addEventListener('click', () => rotateHandler(piecesGroup, isPieceFlat));

/**
 * Flip Button
 * Flips a piece in the scene.
 * Calls the `flipHandler` function to handle flipping logic.
 */
const flipButton = document.getElementById('flip');
flipButton.addEventListener('click', () => flipHandler(piecesGroup, isPieceFlat));

/**
 * Get Solution Button
 * Extracts data from the pyramid and populates it into an HTML tag.
 * Uses `insideBoundariesHandler` to identify pieces on the plane.
 * Passes the data to `extractDataFromPlane` for processing.
 */
const getSolutionButton = document.getElementById('get_sol');
getSolutionButton.addEventListener('click', () => {
  const piecesOnPlane = insideBoundariesHandler(piecesGroup);
  extractDataFromPlane(piecesOnPlane, piecesGroup);
});

/**
 * Keypress Handler
 * Listens for keydown events.
 * Calls the `keyboardHandler` function with the event, camera, and pieces group.
 */
document.addEventListener('keydown', (event) => keyboardHandler(event, camera, piecesGroup));

/**
 * Mouse Click Handler
 * Listens for click events on the renderer's DOM element.
 * Calls `onClickHandler` to handle interactions with objects in the scene.
 */
renderer.domElement.addEventListener('click', (event) => 
  onClickHandler(event, piecesGroup, raycaster, mouse, camera)
);

/**
 * Window Resize Handler
 * Adjusts the camera's aspect ratio and updates the projection matrix.
 * Resizes the renderer to match the new window dimensions.
 */
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

/******************************************************************************************
                                    RENDER LOOP
******************************************************************************************/

// Render loop
const renderLoop = () => {
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(renderLoop);

};

renderLoop();