import api from './index'

const resource = 'inventory-rules'

export default {

	/**
	 * Load Inventory Rules
	 */
	getAll() {
		return api.get(`${resource}`)
	},

	/**
	 * Load Inventory Rules by parent id
	 * @param {Number} parentid Rule Set id
	 */
	getByParent(parentid) {
		return api.get(`rule-sets/${parentid}/${resource}`)
	},

	/**
	 * Load Inventory Rule
	 * @param {Number} id Inventory Rule id
	 */
	get(id = Number) {
		return api.get(`${resource}/${id}`)
	},

	/**
	 * Create Inventory Rule
	 * @param {Object} payload Inventory Rule model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update Inventory Rule
	 * @param {Object} payload Inventory Rule model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete Inventory Rule
	 * @param {Object} payload Inventory Rule model
	 */
	delete(payload) {
		return api.delete(`${resource}/${payload.id}`)
	},

}