/**
 * Main application for the Shape Splitting Workbench.
 */

import { API } from './api.js';
import { Viewer } from './viewer.js';

class App {
    constructor() {
        this.viewer = null;
        this.shapesInfo = {};
        this.splittersInfo = {};

        this.init();
    }

    async init() {
        // Initialize viewer
        const canvas = document.getElementById('viewer');
        this.viewer = new Viewer(canvas);

        // Bind UI elements
        this.bindElements();

        // Load initial data
        await this.loadMetadata();

        // Bind event listeners
        this.bindEvents();

        // Generate default shape
        await this.generateShape();

        this.setStatus('Ready', 'success');
    }

    bindElements() {
        // Shape controls
        this.shapeSelect = document.getElementById('shape-select');
        this.shapeParams = document.getElementById('shape-params');
        this.generateBtn = document.getElementById('generate-btn');
        this.uploadInput = document.getElementById('upload-input');

        // Splitter controls
        this.splitterSelect = document.getElementById('splitter-select');
        this.splitterParams = document.getElementById('splitter-params');
        this.numPartsInput = document.getElementById('num-parts');
        this.numPartsValue = document.getElementById('num-parts-value');
        this.splitBtn = document.getElementById('split-btn');
        this.resetBtn = document.getElementById('reset-btn');

        // View controls
        this.explodedCheckbox = document.getElementById('exploded-view');
        this.explodeDistance = document.getElementById('explode-distance');
        this.wireframeCheckbox = document.getElementById('wireframe-view');
        this.showOriginalCheckbox = document.getElementById('show-original');

        // Export controls
        this.exportStlBtn = document.getElementById('export-stl-btn');
        this.exportGltfBtn = document.getElementById('export-gltf-btn');
        this.exportParts = document.getElementById('export-parts');

        // Status
        this.statusEl = document.getElementById('status');
    }

    async loadMetadata() {
        try {
            // Load shapes
            const shapesResponse = await API.getShapes();
            this.shapesInfo = shapesResponse.shapes;

            // Load splitters
            const splittersResponse = await API.getSplitters();
            this.splittersInfo = splittersResponse.splitters;

            // Update UI with loaded options
            this.updateShapeParams();
            this.updateSplitterParams();
        } catch (error) {
            this.setStatus(`Failed to load metadata: ${error.message}`, 'error');
        }
    }

    bindEvents() {
        // Shape events - auto-generate on selection change
        this.shapeSelect.addEventListener('change', () => {
            this.updateShapeParams();
            this.generateShape();
        });
        this.generateBtn.addEventListener('click', () => this.generateShape());
        this.uploadInput.addEventListener('change', (e) => this.uploadMesh(e));

        // Splitter events
        this.splitterSelect.addEventListener('change', () => this.updateSplitterParams());
        this.numPartsInput.addEventListener('input', () => {
            this.numPartsValue.textContent = this.numPartsInput.value;
        });
        this.splitBtn.addEventListener('click', () => this.splitMesh());
        this.resetBtn.addEventListener('click', () => this.resetToOriginal());

        // View events
        this.explodedCheckbox.addEventListener('change', () => {
            const exploded = this.explodedCheckbox.checked;
            this.explodeDistance.disabled = !exploded;
            this.viewer.setExploded(exploded);
        });
        this.explodeDistance.addEventListener('input', () => {
            this.viewer.setExplodeDistance(parseInt(this.explodeDistance.value));
        });
        this.wireframeCheckbox.addEventListener('change', () => {
            this.viewer.setWireframe(this.wireframeCheckbox.checked);
        });
        this.showOriginalCheckbox.addEventListener('change', () => {
            this.viewer.setShowOriginal(this.showOriginalCheckbox.checked);
        });

        // Export events
        this.exportStlBtn.addEventListener('click', () => this.exportMesh('stl'));
        this.exportGltfBtn.addEventListener('click', () => this.exportMesh('gltf'));
    }

    updateShapeParams() {
        const shapeType = this.shapeSelect.value;
        const shapeInfo = this.shapesInfo[shapeType];

        this.shapeParams.innerHTML = '';

        if (!shapeInfo || !shapeInfo.params) return;

        for (const [name, config] of Object.entries(shapeInfo.params)) {
            const div = document.createElement('div');
            div.className = 'param-input control-group';

            if (config.min !== undefined && config.max !== undefined) {
                // Range input
                div.innerHTML = `
                    <label for="shape-${name}">${name}:</label>
                    <input type="range" id="shape-${name}"
                           min="${config.min}" max="${config.max}"
                           step="${config.step || 1}" value="${config.default}">
                    <span id="shape-${name}-value">${config.default}</span>
                `;
                const input = div.querySelector('input');
                const valueSpan = div.querySelector('span');
                input.addEventListener('input', () => {
                    valueSpan.textContent = input.value;
                });
            } else {
                // Number input
                div.innerHTML = `
                    <label for="shape-${name}">${name}:</label>
                    <input type="number" id="shape-${name}" value="${config.default}">
                `;
            }

            this.shapeParams.appendChild(div);
        }
    }

    updateSplitterParams() {
        const splitterType = this.splitterSelect.value;
        const splitterInfo = this.splittersInfo[splitterType];

        this.splitterParams.innerHTML = '';

        if (!splitterInfo || !splitterInfo.params) return;

        for (const [name, config] of Object.entries(splitterInfo.params)) {
            const div = document.createElement('div');
            div.className = 'param-input control-group';

            if (config.type === 'bool') {
                div.innerHTML = `
                    <label>
                        <input type="checkbox" id="split-${name}"
                               ${config.default ? 'checked' : ''}>
                        ${config.description || name}
                    </label>
                `;
            } else if (config.type === 'select') {
                const options = config.options.map(opt =>
                    `<option value="${opt}" ${opt === config.default ? 'selected' : ''}>${opt}</option>`
                ).join('');
                div.innerHTML = `
                    <label for="split-${name}">${config.description || name}:</label>
                    <select id="split-${name}">${options}</select>
                `;
            } else if (config.min !== undefined && config.max !== undefined) {
                div.innerHTML = `
                    <label for="split-${name}">${config.description || name}:</label>
                    <input type="range" id="split-${name}"
                           min="${config.min}" max="${config.max}"
                           step="${config.step || 1}" value="${config.default}">
                    <span id="split-${name}-value">${config.default}</span>
                `;
                const input = div.querySelector('input');
                const valueSpan = div.querySelector('span');
                input.addEventListener('input', () => {
                    valueSpan.textContent = input.value;
                });
            } else {
                div.innerHTML = `
                    <label for="split-${name}">${config.description || name}:</label>
                    <input type="number" id="split-${name}" value="${config.default}">
                `;
            }

            this.splitterParams.appendChild(div);
        }
    }

    getShapeParams() {
        const shapeType = this.shapeSelect.value;
        const shapeInfo = this.shapesInfo[shapeType];
        const params = {};

        if (!shapeInfo || !shapeInfo.params) return params;

        for (const name of Object.keys(shapeInfo.params)) {
            const input = document.getElementById(`shape-${name}`);
            if (input) {
                params[name] = parseFloat(input.value);
            }
        }

        return params;
    }

    getSplitterParams() {
        const splitterType = this.splitterSelect.value;
        const splitterInfo = this.splittersInfo[splitterType];
        const params = {};

        if (!splitterInfo || !splitterInfo.params) return params;

        for (const [name, config] of Object.entries(splitterInfo.params)) {
            const input = document.getElementById(`split-${name}`);
            if (input) {
                if (config.type === 'bool') {
                    params[name] = input.checked;
                } else if (config.type === 'int') {
                    params[name] = parseInt(input.value);
                } else {
                    params[name] = parseFloat(input.value);
                }
            }
        }

        return params;
    }

    async generateShape() {
        const shapeType = this.shapeSelect.value;
        const params = this.getShapeParams();

        this.setStatus('Generating shape...', 'loading');
        this.setLoading(true);

        try {
            const response = await API.generateShape(shapeType, params);
            this.viewer.loadMesh(response.mesh);
            this.updateExportParts();
            this.setStatus(`Generated ${shapeType}`, 'success');
        } catch (error) {
            this.setStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    async uploadMesh(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.setStatus(`Uploading ${file.name}...`, 'loading');
        this.setLoading(true);

        try {
            const response = await API.uploadMesh(file);
            this.viewer.loadMesh(response.mesh);
            this.updateExportParts();
            this.setStatus(`Uploaded ${file.name}`, 'success');
        } catch (error) {
            this.setStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
            this.uploadInput.value = '';
        }
    }

    async splitMesh() {
        const strategy = this.splitterSelect.value;
        const numParts = parseInt(this.numPartsInput.value);
        const params = this.getSplitterParams();
        const shapeType = this.shapeSelect.value;
        const shapeParams = this.getShapeParams();

        this.setStatus(`Splitting with ${strategy}...`, 'loading');
        this.setLoading(true);

        try {
            const response = await API.splitMesh(strategy, numParts, params, shapeType, shapeParams);
            this.viewer.loadMesh(response.mesh);
            this.updateExportParts();
            this.setStatus(`Split into ${response.num_parts} parts`, 'success');
        } catch (error) {
            this.setStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    async resetToOriginal() {
        // Reset to unsplit shape by regenerating
        this.setStatus('Resetting...', 'loading');
        this.setLoading(true);

        try {
            await this.generateShape();
            // Reset view controls
            this.explodedCheckbox.checked = false;
            this.explodeDistance.disabled = true;
            this.viewer.setExploded(false);
            this.setStatus('Reset complete', 'success');
        } catch (error) {
            this.setStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    async exportMesh(format) {
        this.setStatus(`Exporting ${format.toUpperCase()}...`, 'loading');

        try {
            const blob = await API.exportMesh(format);
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `mesh.${format}`;
            a.click();
            URL.revokeObjectURL(url);
            this.setStatus(`Exported ${format.toUpperCase()}`, 'success');
        } catch (error) {
            this.setStatus(`Error: ${error.message}`, 'error');
        }
    }

    async exportPart(index) {
        this.setStatus(`Exporting part ${index + 1}...`, 'loading');

        try {
            const blob = await API.exportMesh('stl', index);
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `part_${index + 1}.stl`;
            a.click();
            URL.revokeObjectURL(url);
            this.setStatus(`Exported part ${index + 1}`, 'success');
        } catch (error) {
            this.setStatus(`Error: ${error.message}`, 'error');
        }
    }

    updateExportParts() {
        const partCount = this.viewer.getPartCount();
        this.exportParts.innerHTML = '';

        if (partCount > 1) {
            for (let i = 0; i < partCount; i++) {
                const btn = document.createElement('button');
                btn.textContent = `Export Part ${i + 1}`;
                btn.addEventListener('click', () => this.exportPart(i));
                this.exportParts.appendChild(btn);
            }
        }
    }

    setStatus(message, type = '') {
        this.statusEl.textContent = message;
        this.statusEl.className = type;
    }

    setLoading(loading) {
        this.generateBtn.disabled = loading;
        this.splitBtn.disabled = loading;
        this.resetBtn.disabled = loading;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});
