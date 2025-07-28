import api from './index'

const resource = 'single-cma-workups'

export default {

	/**
	 * Get specific Single CMA Workup by id
	 * @param {Number} id property id
	 */
	get(id) {
		return api.get(`${resource}/${id}`)
	},

	/**
	 * Create Single CMA Workup by id
	 * @param {FormData} payload FormData with valid file and data
	 */
	create(payload) {
		return api.post(`${resource}`, payload, {
			headers: {
				'Content-Type': 'multipart/form-data',
			},
		})
	},

	/**
	 * Update Single CMA Workup by id
	 * @param {FormData} payload Single CMA Workup Model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete Single CMA Workup by id
	 * @param {Object} payload Single CMA Workup Model
	 */
	delete(id) {
		return api.delete(`${resource}/${id}`)
	},

}