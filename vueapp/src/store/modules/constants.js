import { apiFactory } from '@/api/apiFactory'
import { objectMap } from '@/utils'

const constantsApi = apiFactory.get('constants')

const state = {
	constants: {},
}

const getters = {
	constants: ({ constants }) => constants,
	transConstants: ({ constants }) => {
		return objectMap(constants, v => {
			return Object.entries(v).map(([key, value]) => ({
				key: Number(key),
				value,
			}))
		})
	},
}

const mutations = {
	SET_CONSTANTS(state, payload) {
		state.constants = payload
	},
}

const actions = {
	async loadConstants({ commit, dispatch }, county) {
		try {
			const { data } = await constantsApi.getAll(county)
			commit('SET_CONSTANTS', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load constants',
				color: 'error'
			}, { root: true })
		}
	},
}

export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations,
}