import api from './index'

const resource = '/properties'

export default {

	/**
	 * Search properties
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},

	/**
	 * Get specific property
	 * @param {Number} id property id
	 */
	get(id) {
		return api.get(`${resource}/${id}`)
	},

	/**
	 * Update specific property
	 * @param {Object} property property model
	 */
	update(property) {
		return api.put(`${resource}/${property.id}`, property)
	},

	/**
	 * Recalculate for one comp only
	 * @param {Object} payload cma payload object
	 */
	analyze(payload) {
		const { all_comps: [ property ]} = payload
		return api.post(`${resource}/${property.id}/single-cma`, payload)
	},

}