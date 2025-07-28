import api from './index'

const resource = 'rule-sets'

export default {

	/**
	 * Load Rule Sets
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},

	/**
	 * Load Rule Set
	 * @param {Number} id Rule set id
	 */
	get(id = Number) {
		return api.get(`${resource}/${id}`)
	},

	/**
	 * Create Rule set
	 * @param {Object} payload Rule set model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update Rule set
	 * @param {Object} payload Rule set model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete Rule set
	 * @param {Object} payload Rule set model
	 */
	delete(payload) {
		return api.delete(`${resource}/${payload.id}`)
	},

}