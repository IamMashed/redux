import api from './index'

const resource = 'tags'

export default {

	/**
	 * Get all tags
	 */
	getAll() {
		return api.get(`${resource}`)
	},

	/**
	 * Create tag
	 * @param {Object} tag tag model
	 */
	create(tag) {
		return api.post(`${resource}`, tag)
	},

	/**
	 * Update tag
	 * @param {Object} tag tag model
	 */
	update(tag) {
		return api.put(`${resource}/${tag.id}`, tag)
	},

	/**
	 * Delete tag
	 * @param {Object} tag tag model
	 */
	delete(tag) {
		return api.delete(`${resource}/${tag.id}`)
	},

}