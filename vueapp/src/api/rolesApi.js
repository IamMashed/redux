import api from './index'

const resource = 'roles'

export default {

	/**
	 * Get all roles
	 */
	getAll() {
		return api.get(`${resource}`)
	},

}