/**
 * Three.js WebGL viewer for the Shape Splitting Workbench.
 */

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Sleek white/grey tones for mesh parts
const PART_COLORS = [
    0xffffff, // white
    0xe8e8e8, // light grey
    0xd0d0d0, // medium grey
    0xf5f5f5, // off-white
    0xcccccc, // grey
    0xdddddd, // silver
    0xeeeeee, // pale grey
    0xc0c0c0, // darker grey
];

export class Viewer {
    constructor(canvas) {
        this.canvas = canvas;
        this.meshes = [];
        this.originalMesh = null;
        this.exploded = true;
        this.explodeDistance = 30;
        this.showWireframe = true;
        this.showOriginal = false;

        this.init();
    }

    init() {
        // Scene
        this.scene = new THREE.Scene();

        // Camera
        const aspect = this.canvas.clientWidth / this.canvas.clientHeight;
        this.camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 10000);
        this.camera.position.set(150, 150, 150);

        // Renderer
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true,
            alpha: true,
        });
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);

        // Controls
        this.controls = new OrbitControls(this.camera, this.canvas);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;

        // Simple lighting - one main light plus ambient
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        const mainLight = new THREE.DirectionalLight(0xffffff, 0.8);
        mainLight.position.set(100, 150, 100);
        this.scene.add(mainLight);

        // Grid helper - subtle dark
        const gridHelper = new THREE.GridHelper(200, 20, 0x444444, 0x333333);
        this.scene.add(gridHelper);

        // Axes helper - subtle
        const axesHelper = new THREE.AxesHelper(30);
        this.scene.add(axesHelper);

        // Handle resize
        window.addEventListener('resize', () => this.onResize());

        // Start animation loop
        this.animate();
    }

    onResize() {
        const width = this.canvas.clientWidth;
        const height = this.canvas.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }

    /**
     * Create a Three.js mesh from mesh data.
     * @param {Object} meshData - Mesh data with vertices, normals, indices
     * @param {number} color - Hex color
     * @returns {THREE.Mesh}
     */
    createMeshFromData(meshData, color) {
        const geometry = new THREE.BufferGeometry();

        // Set vertices
        const vertices = new Float32Array(meshData.vertices);
        geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));

        // Set normals
        if (meshData.normals && meshData.normals.length > 0) {
            const normals = new Float32Array(meshData.normals);
            geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
        }

        // Set indices
        if (meshData.indices && meshData.indices.length > 0) {
            const indices = new Uint32Array(meshData.indices);
            geometry.setIndex(new THREE.BufferAttribute(indices, 1));
        }

        // Compute normals if not provided
        if (!meshData.normals || meshData.normals.length === 0) {
            geometry.computeVertexNormals();
        }

        // Clean matte material
        const material = new THREE.MeshStandardMaterial({
            color: color,
            metalness: 0.0,
            roughness: 0.6,
            side: THREE.DoubleSide,
        });

        const mesh = new THREE.Mesh(geometry, material);

        // Add wireframe - visible dark lines
        const wireframeMaterial = new THREE.LineBasicMaterial({
            color: 0x222222,
            linewidth: 1,
            transparent: true,
            opacity: 0.6,
        });
        const wireframeGeometry = new THREE.WireframeGeometry(geometry);
        const wireframe = new THREE.LineSegments(wireframeGeometry, wireframeMaterial);
        wireframe.visible = this.showWireframe;
        mesh.add(wireframe);
        mesh.userData.wireframe = wireframe;

        return mesh;
    }

    /**
     * Load mesh data from the API response.
     * @param {Object} data - API response with mesh or parts data
     */
    loadMesh(data) {
        this.clearMeshes();

        if (data.parts && data.parts.length > 0) {
            // Multiple parts
            data.parts.forEach((partData, index) => {
                const color = PART_COLORS[index % PART_COLORS.length];
                const mesh = this.createMeshFromData(partData, color);
                mesh.userData.partIndex = index;
                mesh.userData.originalPosition = mesh.position.clone();
                mesh.userData.centroid = new THREE.Vector3(
                    partData.centroid[0],
                    partData.centroid[1],
                    partData.centroid[2]
                );
                this.meshes.push(mesh);
                this.scene.add(mesh);
            });

            // Store original for ghost display
            if (this.showOriginal && data.parts.length > 1) {
                this.createOriginalGhost(data);
            }
        } else if (data.vertices) {
            // Single mesh
            const mesh = this.createMeshFromData(data, PART_COLORS[0]);
            mesh.userData.partIndex = 0;
            mesh.userData.originalPosition = mesh.position.clone();
            this.meshes.push(mesh);
            this.scene.add(mesh);
        }

        // Fit camera to scene
        this.fitCameraToScene();

        // Apply current explode state
        if (this.exploded) {
            this.setExploded(true);
        }
    }

    /**
     * Create a ghost mesh showing the original shape.
     * @param {Object} data - Mesh data
     */
    createOriginalGhost(data) {
        if (this.originalMesh) {
            this.scene.remove(this.originalMesh);
            this.originalMesh = null;
        }

        // Combine all parts into one ghost mesh
        const combinedGeometry = new THREE.BufferGeometry();
        const allVertices = [];
        const allIndices = [];
        let indexOffset = 0;

        data.parts.forEach(part => {
            // Add vertices
            for (let i = 0; i < part.vertices.length; i += 3) {
                allVertices.push(part.vertices[i], part.vertices[i + 1], part.vertices[i + 2]);
            }
            // Add indices with offset
            if (part.indices) {
                for (let i = 0; i < part.indices.length; i++) {
                    allIndices.push(part.indices[i] + indexOffset);
                }
            }
            indexOffset += part.vertices.length / 3;
        });

        combinedGeometry.setAttribute(
            'position',
            new THREE.BufferAttribute(new Float32Array(allVertices), 3)
        );

        if (allIndices.length > 0) {
            combinedGeometry.setIndex(allIndices);
        }

        // Use EdgesGeometry for clean outline (only shows sharp edges)
        const edgesGeometry = new THREE.EdgesGeometry(combinedGeometry, 15);
        const edgesMaterial = new THREE.LineBasicMaterial({
            color: 0x666666,
            transparent: true,
            opacity: 0.5,
        });

        this.originalMesh = new THREE.LineSegments(edgesGeometry, edgesMaterial);
        this.originalMesh.visible = this.showOriginal;
        this.scene.add(this.originalMesh);
    }

    /**
     * Clear all meshes from the scene.
     */
    clearMeshes() {
        this.meshes.forEach(mesh => {
            this.scene.remove(mesh);
            if (mesh.geometry) mesh.geometry.dispose();
            if (mesh.material) mesh.material.dispose();
        });
        this.meshes = [];

        if (this.originalMesh) {
            this.scene.remove(this.originalMesh);
            if (this.originalMesh.geometry) this.originalMesh.geometry.dispose();
            if (this.originalMesh.material) this.originalMesh.material.dispose();
            this.originalMesh = null;
        }
    }

    /**
     * Fit camera to encompass all meshes.
     */
    fitCameraToScene() {
        if (this.meshes.length === 0) return;

        const box = new THREE.Box3();
        this.meshes.forEach(mesh => box.expandByObject(mesh));

        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);

        const fov = this.camera.fov * (Math.PI / 180);
        const cameraDistance = maxDim / (2 * Math.tan(fov / 2)) * 1.5;

        this.camera.position.set(
            center.x + cameraDistance * 0.7,
            center.y + cameraDistance * 0.7,
            center.z + cameraDistance * 0.7
        );
        this.controls.target.copy(center);
        this.controls.update();
    }

    /**
     * Set exploded view mode.
     * @param {boolean} exploded - Whether to show exploded view
     */
    setExploded(exploded) {
        this.exploded = exploded;

        if (this.meshes.length <= 1) return;

        // Calculate overall centroid
        const overallCentroid = new THREE.Vector3();
        this.meshes.forEach(mesh => {
            overallCentroid.add(mesh.userData.centroid || new THREE.Vector3());
        });
        overallCentroid.divideScalar(this.meshes.length);

        this.meshes.forEach(mesh => {
            if (exploded) {
                // Move away from centroid
                const direction = new THREE.Vector3()
                    .subVectors(mesh.userData.centroid || new THREE.Vector3(), overallCentroid)
                    .normalize();
                mesh.position.copy(direction.multiplyScalar(this.explodeDistance));
            } else {
                // Reset to original position
                mesh.position.set(0, 0, 0);
            }
        });
    }

    /**
     * Set explode distance.
     * @param {number} distance - Distance to explode parts
     */
    setExplodeDistance(distance) {
        this.explodeDistance = distance;
        if (this.exploded) {
            this.setExploded(true);
        }
    }

    /**
     * Toggle wireframe display.
     * @param {boolean} show - Whether to show wireframe
     */
    setWireframe(show) {
        this.showWireframe = show;
        this.meshes.forEach(mesh => {
            if (mesh.userData.wireframe) {
                mesh.userData.wireframe.visible = show;
            }
        });
    }

    /**
     * Toggle original mesh ghost display.
     * @param {boolean} show - Whether to show original
     */
    setShowOriginal(show) {
        this.showOriginal = show;
        if (this.originalMesh) {
            this.originalMesh.visible = show;
        }
    }

    /**
     * Get number of parts currently displayed.
     * @returns {number}
     */
    getPartCount() {
        return this.meshes.length;
    }
}

// Export for non-module scripts
window.Viewer = Viewer;
