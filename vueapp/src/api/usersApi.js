import api from './index'

const resource = 'users'

export default {

	/**
	 * Get all users
	 */
	getAll() {
		return api.get(`${resource}`)
	},

	/**
	 * Load User
	 * @param {Number} id User id
	 */
	get(id = Number) {
		return api.get(`${resource}/${id}`)
	},

	/**
	 * Create User
	 * @param {Object} payload User model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update User
	 * @param {Object} payload User model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete User
	 * @param {Object} payload User model
	 */
	delete(payload) {
		return api.delete(`${resource}/${payload.id}`)
	},

}