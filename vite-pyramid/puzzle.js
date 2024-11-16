import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'; // Import OrbitControls
import { DragControls } from 'three/addons/controls/DragControls.js'; // Import DragControls
import { onClickHandler, keyboardHandler, selected, createPieces } from './functions.js';
import { pieces, colorMapping } from './defs.js';

// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xefefef);

// Ambient Light setup
const ambientLight = new THREE.AmbientLight(0xfefefe, 0.5);
scene.add(ambientLight);

// SpotLight setup
const spotLight = new THREE.SpotLight(0xffffff, 1000);
spotLight.position.set(10, 20, 10);
spotLight.angle = Math.PI / 6;
spotLight.castShadow = true;
scene.add(spotLight);

// Mouse and Raycaster
const mouse = new THREE.Vector2();
const raycaster = new THREE.Raycaster();

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(7, 20, 60);  // Initial camera position
camera.lookAt(0,0,0)

// Renderer setup
const canvas = document.querySelector('canvas.threejs');
const renderer = new THREE.WebGLRenderer({ 
  antialias: true,
  canvas: canvas
 });
renderer.setSize(window.innerWidth, window.innerHeight);

// Grid and Axes Helpers setup
const axesHelper = new THREE.AxesHelper(10);
const gridHelper = new THREE.GridHelper(200, 100, 0x000000, 0xffffff);
scene.add(axesHelper);
scene.add(gridHelper);

// OrbitControls setup
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;  // Smooth movement
controls.dampingFactor = 0.25;
controls.screenSpacePanning = false;

// Plane setup
const planeGeometry = new THREE.PlaneGeometry(10, 10);
const planeMaterial = new THREE.MeshStandardMaterial({ color: 0xcccccc, side: THREE.DoubleSide });
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.position.set(0, 0, 0);
plane.rotation.x = -Math.PI / 2; // Rotate to make it horizontal
scene.add(plane); // Add to the scene

// Create a groups
const piecesGroup = new THREE.Group();

createPieces(piecesGroup);
scene.add(piecesGroup);


const dragControls = new DragControls(piecesGroup.children, camera, renderer.domElement);
let initialY = 0; // To store the initial Y position
dragControls.addEventListener('dragstart', (event) => {
  controls.enabled = false;
  const object = event.object;
  initialY = object.position.y; // Store the Y position when the drag starts
});

dragControls.addEventListener('dragend', () => {
  controls.enabled = true;
});

dragControls.addEventListener('drag', (event) => {
  const object = event.object;

  // Allow movement in X and Z axis
  object.position.x = Math.round(object.position.x / 2) * 2;
  object.position.z = Math.round(object.position.z / 2) * 2;
  object.position.y = initialY; // Do not change Y on drag
});

 /******************************************************************************************
                                        BUTTONS HANDLERS
******************************************************************************************/

const toggleButton = document.getElementById('tc');
toggleButton.addEventListener('click', ()=>{
  controls.enabled = !controls.enabled;
})

const resetButton = document.getElementById('reset-piece');
resetButton.addEventListener('click', ()=>{
  if (selected){
    selected.rotation.set(0,0,0);
    selected.rotateX(THREE.MathUtils.degToRad(90));
  }
})

const rotate = document.getElementById('rotate');
rotate.addEventListener('click', ()=>{
  if (selected){
    selected.rotateZ(THREE.MathUtils.degToRad(90));
  }
})

let isPieceFlat = true;
const changeOr = document.getElementById('change-orientation');
changeOr.addEventListener('click', ()=>{
  if (selected){
    if (isPieceFlat){
      selected.rotation.set(0, 0, 0);
      selected.rotateY(THREE.MathUtils.degToRad(-45));
      isPieceFlat = false;
    }
    else {
      selected.rotation.set(0, 0, 0);
      selected.rotateX(THREE.MathUtils.degToRad(90));
      isPieceFlat = true;
    }
  }
})


document.addEventListener('keydown', (event) => keyboardHandler(event, camera));

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