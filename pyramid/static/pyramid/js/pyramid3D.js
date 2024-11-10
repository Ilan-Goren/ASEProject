import * as THREE from 'https://esm.sh/three@0.170.0';
import { OrbitControls } from 'https://esm.sh/three@0.170.0/examples/jsm/controls/OrbitControls.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('3d-container').appendChild(renderer.domElement);
renderer.setClearColor(0xeeeeee, 1);

const light = new THREE.PointLight(0xffffff, 1, 100);
light.position.set(10, 10, 10);
scene.add(light);
const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let selectedObject = null;
let isDragging = false;

function createSphere(x, y, z, color = 0x0077ff) {
    const geometry = new THREE.SphereGeometry(0.5, 32, 32);
    const material = new THREE.MeshStandardMaterial({ color });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(x, y, z);
    sphere.userData = { draggable: true };
    scene.add(sphere);
    return sphere;
}

function createPyramid(levels) {
    const spacing = 1;
    for (let level = 0; level < levels; level++) {
        const numSpheres = levels - level;
        const yOffset = level * spacing;
        for (let row = 0; row < numSpheres; row++) {
            for (let col = 0; col < numSpheres - row; col++) {
                const xOffset = (col - (numSpheres - row) / 2) * spacing;
                const zOffset = (row - numSpheres / 2) * spacing;
                createSphere(xOffset, yOffset, zOffset, Math.random() * 0xffffff);
            }
        }
    }
}

createPyramid(5);

camera.position.set(0, 5, 15);
camera.lookAt(0, 0, 0);

function onMouseDown(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children);
    if (intersects.length > 0 && intersects[0].object.userData.draggable) {
        selectedObject = intersects[0].object;
        isDragging = true;
    }
}

function onMouseMove(event) {
    if (isDragging && selectedObject) {
        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObject(scene, true);
        if (intersects.length > 0) {
            const point = intersects[0].point;
            selectedObject.position.set(point.x, point.y, point.z);
        }
    }
}

function onMouseUp() {
    isDragging = false;
    selectedObject = null;
}

window.addEventListener('mousedown', onMouseDown, false);
window.addEventListener('mousemove', onMouseMove, false);
window.addEventListener('mouseup', onMouseUp, false);

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();