// these needs to be accessed inside more than one function so we'll declare them first
let container;
let camera;
let controls;
let renderer;
let scene;
let model;
// let dragControls;
let models = [];

// let myFilePath;

// mixers
const mixers = [];
const clock = new THREE.Clock();

function init() {
   container = document.querySelector('#scene-container');

   createScene();
   createCamera();
   createControls();
   loadModel();
   createLights();
   createRenderer();

   // setAnimationLoop() method for WebXR
   renderer.setAnimationLoop(() => {
      render();
   });
   // /
}

function createScene() {
   scene = new THREE.Scene();
   scene.background = new THREE.Color(0x8FBCD4);
}
function createCamera() {
   camera = new THREE.PerspectiveCamera(35, container.clientWidth / container.clientHeight, 1, 3000);
   camera.position.set( 50, 100, 100);
   // camera.position.set(0, 0, 300);
}
function createControls() {
   controls = new THREE.OrbitControls(camera, container);

   // dragControls = new THREE.DragControls(camera, container);
   // dragControls.addEventListener('dragstart', function (event) {
   //    console.log('drag start');
   //    controls.enabled = false;
   // });
   // dragControls.addEventListener('drag', function (event) {
   //    console.log('drag');
   // });
   // dragControls.addEventListener('dragend', function (event) {
   //    console.log('drag end');
   //    controls.enabled = true;
   // });
}

// _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

function createLights() {
   const hemisphereLight = new THREE.HemisphereLight(0xddeeff, 0x202020, 5.0);
   const mainLight = new THREE.DirectionalLight(0xFFFFFF, 5.0);
   mainLight.position.set(10, 10, 10);
   scene.add(hemisphereLight, mainLight);
}

// _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
function loadModel() {
   const loader = new THREE.GLTFLoader();

   const onLoad = (gltfResult, position) => {
      model = gltfResult.scene.children[0];

      model.position.copy(position);

      scene.add(model);
      models.push(model);
   };

   const onProgress = () => { console.log('Models are on the way...'); };
   //
   const onError = (errorMessage) => { console.log(errorMessage); };

   const parrotPosition = new THREE.Vector3(0, 0, 0);
   loader.load('computer.glb', gltfResult => onLoad(gltfResult, parrotPosition), onProgress, onError);
}


// _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

function createRenderer() {
   renderer = new THREE.WebGLRenderer({ antialias: true, container });
   renderer.setSize(container.clientWidth, container.clientHeight);
   renderer.setPixelRatio(window.devicePixelRatio);
   container.appendChild(renderer.domElement);
}

function render() {
   renderer.render(scene, camera);
}

function onWindowResize() {
   // set the aspect ratio to match the new browser window aspect ratio
   camera.aspect = container.clientWidth / container.clientHeight;
   // update the camera's frustrum
   camera.updateProjectionMatrix();
   // update the size of the renderer and the canvas
   renderer.setSize(container.clientWidth, container.clientHeight);
}
window.addEventListener('resize', onWindowResize);

init();
