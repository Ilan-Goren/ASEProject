import * as THREE from 'https://esm.sh/three@0.170.0';
import { OrbitControls } from 'https://esm.sh/three@0.170.0/examples/jsm/controls/OrbitControls.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf0f0f0);

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(7, 0, 10);  // Initial camera position
camera.lookAt(new THREE.Vector3(0, 0, 0));  // Looking at the center of the pyramid

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// OrbitControls setup
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;  // Smooth movement
controls.dampingFactor = 0.25;
controls.screenSpacePanning = false;
controls.maxPolarAngle = Math.PI / 2;  // Limit vertical movement to prevent flipping

// Function to parse the table data and return it as an array of layers
function parseTableData() {
  const layers = [];
  const tables = document.querySelectorAll('table');
  
  tables.forEach(table => {
    const rows = [];
    const cells = table.querySelectorAll('tr');
    
    cells.forEach(row => {
      const values = Array.from(row.querySelectorAll('td')).map(cell => parseInt(cell.textContent));
      rows.push(values);
    });

    layers.push(rows);
  });

  return layers;
}

// Function to create the pyramid based on parsed data
function createPyramid(layers) {
  const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });

  layers.forEach((layer, layerIndex) => {
    layer.forEach((row, rowIndex) => {
      row.forEach((value, colIndex) => {
        if (value === 1) {
          const sphereGeometry = new THREE.SphereGeometry(0.5, 16, 16);
          const sphere = new THREE.Mesh(sphereGeometry, material);
          // Position the spheres in the 3D space, adjusting them based on layer size
          sphere.position.set(colIndex - layer.length / 2, 5 -layerIndex, rowIndex - layer[0].length / 2);
          scene.add(sphere);
        }
      });
    });
  });
}



const layers = parseTableData();  // Parse the table data into layers
createPyramid(layers);            // Create the 3D pyramid

// Toggle button for enabling/disabling OrbitControls
const toggleButton = document.getElementById('tc')
document.body.appendChild(toggleButton);
toggleButton.style.position = 'absolute';
// toggleButton.style.top = '10px';
// toggleButton.style.left = '10px';

toggleButton.addEventListener('click', () => {
  controls.enabled = !controls.enabled;
});

// Handle window resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Render loop
const renderLoop = () => {
  controls.update();  // Update the controls in each frame for damping
  renderer.render(scene, camera);
  requestAnimationFrame(renderLoop);
};

renderLoop();