/**
 * API client for the Shape Splitting Workbench backend.
 */

// Use localhost for local dev, /api/ for Vercel production
const API_BASE = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : '/api';

export const API = {
    /**
     * List available primitive shapes.
     * @returns {Promise<Object>} Shape definitions
     */
    async getShapes() {
        const response = await fetch(`${API_BASE}/shapes`);
        if (!response.ok) throw new Error('Failed to fetch shapes');
        return response.json();
    },

    /**
     * Generate a primitive shape.
     * @param {string} type - Shape type (kite, diamond, sphere, etc.)
     * @param {Object} params - Shape parameters
     * @returns {Promise<Object>} Generated mesh data
     */
    async generateShape(type, params = {}) {
        const response = await fetch(`${API_BASE}/shapes/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ shape_type: type, params }),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate shape');
        }
        return response.json();
    },

    /**
     * List available splitting algorithms.
     * @returns {Promise<Object>} Splitter definitions
     */
    async getSplitters() {
        const response = await fetch(`${API_BASE}/splitters`);
        if (!response.ok) throw new Error('Failed to fetch splitters');
        return response.json();
    },

    /**
     * Split the current mesh.
     * @param {string} strategy - Splitting algorithm name
     * @param {number} numParts - Number of parts to split into
     * @param {Object} params - Algorithm-specific parameters
     * @param {string} shapeType - Current shape type (for serverless regeneration)
     * @param {Object} shapeParams - Current shape params (for serverless regeneration)
     * @returns {Promise<Object>} Split mesh data
     */
    async splitMesh(strategy, numParts, params = {}, shapeType = 'diamond', shapeParams = {}) {
        const body = {
            strategy,
            num_parts: numParts,
            params,
            shape_type: shapeType,
            shape_params: shapeParams,
        };

        const response = await fetch(`${API_BASE}/split`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to split mesh');
        }
        return response.json();
    },

    /**
     * Upload a custom mesh file.
     * @param {File} file - Mesh file (STL, OBJ, etc.)
     * @returns {Promise<Object>} Uploaded mesh data
     */
    async uploadMesh(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to upload mesh');
        }
        return response.json();
    },

    /**
     * Export mesh(es) in specified format.
     * @param {string} format - Export format (stl, gltf)
     * @param {number|null} partIndex - Specific part index or null for all
     * @returns {Promise<Blob>} Exported file data
     */
    async exportMesh(format, partIndex = null) {
        const response = await fetch(`${API_BASE}/export`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                format,
                part_index: partIndex,
            }),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to export mesh');
        }
        return response.blob();
    },

    /**
     * Get current mesh state.
     * @returns {Promise<Object>} Current mesh state
     */
    async getCurrentState() {
        const response = await fetch(`${API_BASE}/current`);
        if (!response.ok) throw new Error('Failed to get current state');
        return response.json();
    },
};

// Export for non-module scripts
window.API = API;
