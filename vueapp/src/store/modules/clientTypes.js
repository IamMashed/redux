import { apiFactory } from '@/api/apiFactory'

const clientTypesApi = apiFactory.get('client-types')

const state = {
	clientTypes: [],
}

const getters = {
	clientTypes: ({ clientTypes }) => clientTypes,
}

const mutations = {
	SET_CLIENT_TYPES(state, payload) {
		state.clientTypes = payload
	},
}

const actions = {
	async loadClientTypes({ commit, dispatch }) {
		try {
			const { data } = await clientTypesApi.getAll()
			commit('SET_CLIENT_TYPES', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load client types',
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