import api from './index'

const resource = 'single-cma'

export default {

	/**
	 * Get specific single CMA by property id
	 * @param {Number} id property id
	 * @param {Object} params get params
	 */
	get(id, params) {
		return api.get(`${resource}/${id}`, {
			params,
		})
	},

	/**
	 * Recalculate CMA based on data
	 * @param {Object} payload cma payload object
	 * @param {Object} params get params
	 */
	post(payload, params) {
		return api.post(`${resource}`, payload, {
			params,
		})
	},

	/**
	 * Load CMA Logs
	 * @param {Number} id property id
	 * @param {Object} payload cma payload object
	 * @param {Object} params get params
	 */
	log(id, payload, params) {
		return api.post(`${resource}/log`, payload, {
			params,
		})
	},

}