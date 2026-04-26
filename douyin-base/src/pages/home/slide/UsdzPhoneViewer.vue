<template>
  <div ref="hostRef" class="usdz-phone-viewer"></div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import * as THREE from 'three'
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js'
import { USDZLoader } from 'three-usdz-loader-esm'

type UsdzInstance = {
  update?: (seconds: number) => void
  clear?: () => void
  clean?: () => void
}

type WindowWithUsdzGlobals = Window & {
  envMap?: THREE.Texture
}

const props = defineProps<{
  src: string
  active?: boolean
}>()

const emit = defineEmits<{
  error: [error: unknown]
}>()

const USDZ_DEPENDENCIES_PATH = '/usdz-loader'

let sharedLoader: USDZLoader | null = null
let loadQueue = Promise.resolve()

function getSharedLoader() {
  if (!sharedLoader) {
    sharedLoader = new USDZLoader(USDZ_DEPENDENCIES_PATH)
  }
  return sharedLoader
}

function queueLoad(file: File, target: THREE.Group) {
  const loadTask = loadQueue.then(() => getSharedLoader().loadFile(file, target))
  loadQueue = loadTask.catch(() => undefined).then(() => undefined)
  return loadTask
}

const hostRef = ref<HTMLDivElement | null>(null)

let scene: THREE.Scene | null = null
let camera: THREE.PerspectiveCamera | null = null
let renderer: THREE.WebGLRenderer | null = null
let pmremGenerator: THREE.PMREMGenerator | null = null
let environmentMap: THREE.Texture | null = null
let modelRoot: THREE.Group | null = null
let modelContent: THREE.Group | null = null
let loadedInstance: UsdzInstance | null = null
let resizeObserver: ResizeObserver | null = null
let animationFrame = 0
let disposed = false
let baseRotation = -0.38
const clock = new THREE.Clock()

function assertRuntimeSupport() {
  if (typeof SharedArrayBuffer === 'undefined' || typeof Atomics === 'undefined') {
    throw new Error('USDZ loader requires SharedArrayBuffer and Atomics.')
  }
}

function resizeRenderer() {
  if (!hostRef.value || !renderer || !camera) return

  const width = Math.max(hostRef.value.clientWidth, 1)
  const height = Math.max(hostRef.value.clientHeight, 1)

  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2))
  renderer.setSize(width, height, false)
  camera.aspect = width / height
  camera.updateProjectionMatrix()
}

function setupScene() {
  const host = hostRef.value
  if (!host) return

  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(29, 1, 0.01, 100)
  camera.position.set(0, 0.18, 4.15)

  renderer = new THREE.WebGLRenderer({
    alpha: true,
    antialias: true,
    powerPreference: 'high-performance'
  })
  renderer.outputColorSpace = THREE.SRGBColorSpace
  renderer.toneMapping = THREE.ACESFilmicToneMapping
  renderer.toneMappingExposure = 1.08
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap

  pmremGenerator = new THREE.PMREMGenerator(renderer)
  environmentMap = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture
  scene.environment = environmentMap
  ;(window as WindowWithUsdzGlobals).envMap = environmentMap

  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x20232a, 1.35)
  scene.add(hemiLight)

  const keyLight = new THREE.DirectionalLight(0xffffff, 3.2)
  keyLight.position.set(2.6, 3.4, 4)
  keyLight.castShadow = true
  scene.add(keyLight)

  const rimLight = new THREE.DirectionalLight(0xbfd7ff, 1.25)
  rimLight.position.set(-3.2, 1.6, -2.4)
  scene.add(rimLight)

  modelRoot = new THREE.Group()
  modelContent = new THREE.Group()
  modelRoot.add(modelContent)
  scene.add(modelRoot)

  host.appendChild(renderer.domElement)
  resizeRenderer()

  resizeObserver = new ResizeObserver(resizeRenderer)
  resizeObserver.observe(host)
}

function normalizeModel() {
  if (!modelContent || !modelRoot) return

  modelContent.updateMatrixWorld(true)
  const bounds = new THREE.Box3().setFromObject(modelContent)
  if (bounds.isEmpty()) return

  const size = bounds.getSize(new THREE.Vector3())
  const center = bounds.getCenter(new THREE.Vector3())
  const maxSize = Math.max(size.x, size.y, size.z)
  const scale = maxSize > 0 ? 1.74 / maxSize : 1

  modelContent.scale.setScalar(scale)
  modelContent.position.set(-center.x * scale, -center.y * scale - 0.03, -center.z * scale)
  modelRoot.rotation.set(-0.08, baseRotation, 0.03)
}

function disposeObject3D(root: THREE.Object3D) {
  root.traverse((object) => {
    const mesh = object as THREE.Mesh
    mesh.geometry?.dispose?.()

    const materials = Array.isArray(mesh.material) ? mesh.material : mesh.material ? [mesh.material] : []
    materials.forEach((material) => {
      Object.values(material).forEach((value) => {
        if (value instanceof THREE.Texture) {
          value.dispose()
        }
      })
      ;(material as THREE.Material).dispose?.()
    })
  })
}

function animate() {
  if (disposed || !renderer || !scene || !camera) return

  const elapsed = clock.getElapsedTime()
  if (modelRoot) {
    const rotationSpeed = props.active === false ? 0.18 : 0.46
    modelRoot.rotation.y = baseRotation + elapsed * rotationSpeed
  }
  loadedInstance?.update?.(elapsed)
  renderer.render(scene, camera)
  animationFrame = requestAnimationFrame(animate)
}

async function loadModel() {
  if (!modelContent) return

  try {
    assertRuntimeSupport()

    const response = await fetch(props.src)
    if (!response.ok) {
      throw new Error(`Failed to fetch USDZ: ${response.status}`)
    }

    const blob = await response.blob()
    const fileName = decodeURIComponent(props.src.split('/').pop()?.split('?')[0] || 'phone.usdz')
    const file = new File([blob], fileName, { type: 'model/vnd.usdz+zip' })
    const instance = (await queueLoad(file, modelContent)) as UsdzInstance

    if (disposed) {
      instance.clear?.()
      instance.clean?.()
      return
    }

    loadedInstance = instance
    normalizeModel()
  } catch (error) {
    if (!disposed) {
      emit('error', error)
    }
  }
}

function cleanup() {
  disposed = true

  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
  }

  resizeObserver?.disconnect()
  resizeObserver = null

  if (modelContent) {
    disposeObject3D(modelContent)
  }
  loadedInstance?.clear?.()
  loadedInstance?.clean?.()
  loadedInstance = null

  environmentMap?.dispose()
  environmentMap = null
  pmremGenerator?.dispose()
  pmremGenerator = null

  renderer?.dispose()
  renderer?.domElement.remove()
  renderer = null
  scene = null
  camera = null
  modelRoot = null
  modelContent = null
}

onMounted(() => {
  setupScene()
  loadModel()
  animate()
})

onBeforeUnmount(cleanup)
</script>

<style scoped lang="less">
.usdz-phone-viewer {
  canvas {
    display: block;
    width: 100%;
    height: 100%;
  }
}
</style>
