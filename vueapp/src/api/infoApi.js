import api from './index'

export default {

	/**
	 * Get case info
	 */
	caseInfo() {
		return api.get('case-info')
	},

}