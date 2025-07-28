import api from './index'

const resource = '/properties'

export default {

	/**
	 * Get all photos for specific peoprties
	 * @param {Number} propertyid
	 */
	getAll(propertyid) {
		return api.get(`${resource}/${propertyid}/photos`)
	},

	/**
	 * Upload photo to server
	 * @param {Number} propertyid
	 * @param {FormData} payload FormData with valid file
	 */
	create(propertyid, payload) {
		return api.post(`${resource}/${propertyid}/photos`, payload, {
			headers: {
				'Content-Type': 'multipart/form-data',
			},
		})
	},

	/**
	 * Update property photo
	 * @param {Object} payload property photo model
	 */
	update(propertyid, payload) {
		return api.put(`${resource}/${propertyid}/photos/${payload.id}`, payload)
	},

	/**
	 * Delete photo
	 * @param {Number} propertyid
	 * @param {FormData} photoid
	 */
	delete(propertyid, photoid) {
		return api.delete(`${resource}/${propertyid}/photos/${photoid}`)
	},
}