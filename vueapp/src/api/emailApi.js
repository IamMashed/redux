import api from './index'

const resource = 'send-email'

export default {

	/**
	 * Send test email with html body
	 *
	 * @param {Object} payload
	 * @example
	 * {
	 *   "title": "The title of email",
	 *   "body": "The content of email",
	 *   "receiver": "email address"
	 * }
	 */
	sendEmail(payload) {
		return api.post(`${resource}`, payload)
	},
}