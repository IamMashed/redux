import axios from 'axios'
import { makeNull } from '../utils'

const api = axios.create({
	baseURL: process.env.VUE_APP_API,
	withCredentials: true,
})

/**
 * Make all data values nullable if empty
 */
api.interceptors.request.use(
	(config) => {
		if (config.data && !(config.data instanceof FormData))
			config.data = makeNull(config.data)
		return config
	},
)

export default api