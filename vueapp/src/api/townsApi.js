import api from './index'

const resource = 'counties'

export default {

	/**
	 * Get towns by county id
	 */
	getAll(countyid) {
		return api.get(`${resource}/${countyid}/townships`)
	},

}