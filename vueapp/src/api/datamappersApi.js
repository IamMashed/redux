import api from './index'

const resource = 'data-mappers'

export default {

	/**
	 * Get all Data Mappers
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},

	/**
	 * Load Data Mapper
	 * @param {String} name Data Mapper Name
	 */
	get(name = String) {
		return api.get(`${resource}/${name}`)
	},

	/**
	 * Create Data Mapper
	 * @param {Object} payload Data Mapper model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update Data Mapper
	 * @param {Object} payload Data Mapper model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.name}`, payload)
	},

}