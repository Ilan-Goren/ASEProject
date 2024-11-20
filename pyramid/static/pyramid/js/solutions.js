import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'; // Import OrbitControls
import { pieces, colorMapping } from './defs.js';

// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xefefef);

// Ambient Light setup
const ambientLight = new THREE.AmbientLight(0x404040, 30);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(5, 5, 5).normalize();
scene.add(directionalLight);

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 400 );
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

const textureLoader = new THREE.TextureLoader();

const planeTextureUrl = document.getElementById('texture-url').textContent.trim();

const planeTexture = textureLoader.load(planeTextureUrl, () => {
  console.log("Texture Loaded");
});

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

const dataFromBackend = JSON.parse(document.getElementById('pyramid-data').textContent);

// Function to create a pyramid
function createPyramid(data, pyramidGroup) {
    data.forEach((layer, layerIndex) => {
        layer.forEach((row, rowIndex) => {
            row.forEach((cellValue, colIndex) => {
                if (cellValue > 0) {
                    const color = colorMapping[cellValue.toString()];
                    const material = new THREE.MeshStandardMaterial({ color });
                    const sphereGeometry = new THREE.SphereGeometry(1, 16, 16);
                    const sphere = new THREE.Mesh(sphereGeometry, material);

                    const x = colIndex * 2 - row.length;
                    const y = layerIndex * 2;
                    const z = rowIndex * 2 - layer[0].length;

                    sphere.position.set(x, y, z);

                    // Add the sphere to the pyramid group
                    pyramidGroup.add(sphere);
                }
            });
        });
    });
}

const forestWidth = 300;
const forestDepth = 300;

const placedPositions = [];

const numPyramids = dataFromBackend.length;
const numColumns = Math.ceil(Math.sqrt(numPyramids));
const numRows = Math.ceil(numPyramids / numColumns);

const spacingX = forestWidth / numColumns;
const spacingZ = forestDepth / numRows;

dataFromBackend.forEach((solution, index) => {
    const pyramidGroup = new THREE.Group();
    createPyramid(solution, pyramidGroup);

    const columnIndex = index % numColumns;
    const rowIndex = Math.floor(index / numColumns);

    const x = (columnIndex * spacingX) - (forestWidth / 2);
    const z = (rowIndex * spacingZ) - (forestDepth / 2);

    placedPositions.push({ x, z });

    pyramidGroup.position.set(x, 1, z);
    scene.add(pyramidGroup);
});


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