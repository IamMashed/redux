import api from './index'

const resource = 'takeovers'

export default {

	/**
	 * Create takeover
	 * @param {Object} takeover takeover model
	 */
	create(takeover) {
		return api.post(`${resource}`, takeover)
	},

	/**
	 * Delete takeover
	 * @param {Object} takeover takeover model
	 */
	delete(takeover) {
		return api.delete(`${resource}/${takeover.id}`)
	},

}