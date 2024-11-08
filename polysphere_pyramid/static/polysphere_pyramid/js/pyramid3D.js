// Import Three.js
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Create the scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('3d-container').appendChild(renderer.domElement);

// Lighting for better visualization
const light = new THREE.PointLight(0xffffff, 1, 100);
light.position.set(10, 10, 10);
scene.add(light);

// Add OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.rotateSpeed = 0.5;

// Function to create a sphere at a given position
// Function to create a sphere at a given position
function createSphere(x, y, z, color = 0x0077ff) {
    const radius = 0.5; // Adjusted radius for the spheres
    const geometry = new THREE.SphereGeometry(radius, 32, 32); // Radius, width segments, height segments
    const material = new THREE.MeshStandardMaterial({ color });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(x, y, z);
    scene.add(sphere);
}

// Create a level 5 pyramid of spheres
function createPyramid(levels) {
    const radius = 0.5; // Same as the sphere's radius
    const spacing = radius * 2; // Set spacing to the diameter of the spheres

    for (let level = 0; level < levels; level++) {
        const numSpheres = levels - level; // Number of spheres at the current level
        const yOffset = level * spacing; // Vertical offset for each level (upward)

        for (let row = 0; row < numSpheres; row++) {
            for (let col = 0; col < numSpheres - row; col++) {
                const xOffset = (col - (numSpheres - row) / 2) * spacing;
                const zOffset = (row - numSpheres / 2) * spacing;
                createSphere(xOffset, yOffset, zOffset, Math.random() * 0xffffff); // Random color for each sphere
            }
        }
    }
}

// Call the function to create a level 5 pyramid
createPyramid(100);

// Set the camera position and render the scene
camera.position.z = 15; // Adjusted camera position for better viewing angle
camera.position.y = 5;  // Set the camera higher to look down at the pyramid
camera.lookAt(0, 0, 0); // Make sure the camera is looking at the center of the scene

function animate() {
    requestAnimationFrame(animate);
    controls.update(); // Update controls for smooth movement
    renderer.render(scene, camera);
}
animate();