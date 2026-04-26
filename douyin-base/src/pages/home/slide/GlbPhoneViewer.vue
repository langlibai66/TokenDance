<template>
  <div ref="hostRef" class="glb-phone-viewer"></div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import * as THREE from 'three'
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'

const props = defineProps<{
  src: string
  active?: boolean
}>()

const emit = defineEmits<{
  error: [error: unknown]
}>()

const hostRef = ref<HTMLDivElement | null>(null)

let scene: THREE.Scene | null = null
let camera: THREE.PerspectiveCamera | null = null
let renderer: THREE.WebGLRenderer | null = null
let pmremGenerator: THREE.PMREMGenerator | null = null
let modelRoot: THREE.Group | null = null
let resizeObserver: ResizeObserver | null = null
let animationFrame = 0
let disposed = false
let loadedModel: THREE.Object3D | null = null
let modelBounds:
  | {
      center: THREE.Vector3
      size: THREE.Vector3
    }
  | null = null
const clock = new THREE.Clock()
// Rotate 180deg from the default front-facing view so the phone back is shown first.
const baseRotation = Math.PI - 0.55

function resizeRenderer() {
  if (!hostRef.value || !renderer || !camera) return

  const width = Math.max(hostRef.value.clientWidth, 1)
  const height = Math.max(hostRef.value.clientHeight, 1)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2))
  renderer.setSize(width, height, false)
  camera.aspect = width / height
  camera.position.set(0, 0.08, camera.aspect < 0.82 ? 4.9 : 4.35)
  camera.updateProjectionMatrix()

  if (loadedModel) {
    frameModel(loadedModel)
  }
}

function setupScene() {
  const host = hostRef.value
  if (!host) return

  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(28, 1, 0.01, 100)
  camera.position.set(0, 0.1, 4.3)

  renderer = new THREE.WebGLRenderer({
    alpha: true,
    antialias: true,
    powerPreference: 'high-performance'
  })
  renderer.outputColorSpace = THREE.SRGBColorSpace
  renderer.toneMapping = THREE.ACESFilmicToneMapping
  renderer.toneMappingExposure = 1.05
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap

  pmremGenerator = new THREE.PMREMGenerator(renderer)
  scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture

  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x1b2230, 1.3)
  scene.add(hemiLight)

  const keyLight = new THREE.DirectionalLight(0xffffff, 3)
  keyLight.position.set(2.8, 3.5, 4.2)
  scene.add(keyLight)

  const rimLight = new THREE.DirectionalLight(0xa4d6ff, 1.1)
  rimLight.position.set(-3.2, 1.4, -2.2)
  scene.add(rimLight)

  modelRoot = new THREE.Group()
  scene.add(modelRoot)

  host.appendChild(renderer.domElement)
  resizeRenderer()

  resizeObserver = new ResizeObserver(resizeRenderer)
  resizeObserver.observe(host)
}

function disposeMaterial(material: THREE.Material) {
  const materialWithMaps = material as THREE.Material & Record<string, unknown>
  Object.values(materialWithMaps).forEach((value) => {
    if (value instanceof THREE.Texture) {
      value.dispose()
    }
  })
  material.dispose()
}

function disposeObject(root: THREE.Object3D) {
  root.traverse((object) => {
    const mesh = object as THREE.Mesh
    mesh.geometry?.dispose?.()

    if (Array.isArray(mesh.material)) {
      mesh.material.forEach(disposeMaterial)
      return
    }

    if (mesh.material) {
      disposeMaterial(mesh.material)
    }
  })
}

function normalizeModel(root: THREE.Object3D) {
  const bounds = new THREE.Box3().setFromObject(root)
  if (bounds.isEmpty()) return

  modelBounds = {
    size: bounds.getSize(new THREE.Vector3()),
    center: bounds.getCenter(new THREE.Vector3())
  }

  frameModel(root)
}

function frameModel(root: THREE.Object3D) {
  if (!modelRoot || !camera || !modelBounds) return

  const { size, center } = modelBounds
  const distance = camera.position.distanceTo(new THREE.Vector3(0, 0, 0))
  const fov = THREE.MathUtils.degToRad(camera.fov)
  const viewHeight = 2 * Math.tan(fov / 2) * distance
  const viewWidth = viewHeight * camera.aspect
  const fitHeight = viewHeight * 0.8
  const fitWidth = viewWidth * (camera.aspect < 0.82 ? 0.52 : 0.64)
  const scale = Math.min(
    size.x > 0 ? fitWidth / size.x : Infinity,
    size.y > 0 ? fitHeight / size.y : Infinity,
    size.z > 0 ? fitWidth / size.z : Infinity
  )

  root.scale.setScalar(scale)
  root.position.set(
    -center.x * scale,
    -center.y * scale - size.y * scale * 0.035,
    -center.z * scale
  )
  modelRoot.rotation.set(-0.12, baseRotation, 0.05)
}

async function loadModel() {
  if (!modelRoot) return

  try {
    const loader = new GLTFLoader()
    const gltf = await loader.loadAsync(props.src)
    if (disposed) {
      disposeObject(gltf.scene)
      return
    }

    modelRoot.add(gltf.scene)
    loadedModel = gltf.scene
    normalizeModel(gltf.scene)
  } catch (error) {
    if (!disposed) {
      emit('error', error)
    }
  }
}

function animate() {
  if (disposed || !renderer || !scene || !camera) return

  const elapsed = clock.getElapsedTime()
  if (modelRoot) {
    const speed = props.active === false ? 0.2 : 0.44
    modelRoot.rotation.y = baseRotation + elapsed * speed
  }

  renderer.render(scene, camera)
  animationFrame = requestAnimationFrame(animate)
}

function cleanup() {
  disposed = true

  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
  }

  resizeObserver?.disconnect()
  resizeObserver = null

  if (modelRoot) {
    disposeObject(modelRoot)
    scene?.remove(modelRoot)
    modelRoot = null
  }

  loadedModel = null
  modelBounds = null

  scene?.environment?.dispose?.()
  pmremGenerator?.dispose()
  pmremGenerator = null

  renderer?.dispose()
  renderer?.domElement.remove()
  renderer = null
  camera = null
  scene = null
}

onMounted(() => {
  setupScene()
  loadModel()
  animate()
})

onBeforeUnmount(cleanup)
</script>

<style scoped lang="less">
.glb-phone-viewer {
  width: 100%;
  height: 100%;

  canvas {
    display: block;
    width: 100%;
    height: 100%;
  }
}
</style>
