import { apiFactory } from '@/api/apiFactory'

const applicationTypesApi = apiFactory.get('application-types')

const state = {
	applicationTypes: [],
}

const getters = {
	applicationTypes: ({ applicationTypes }) => applicationTypes,
}

const mutations = {
	SET_APPLICATION_TYPES(state, payload) {
		state.applicationTypes = payload
	},
}

const actions = {
	async loadApplicationTypes({ commit, dispatch }) {
		try {
			const { data } = await applicationTypesApi.getAll()
			commit('SET_APPLICATION_TYPES', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load owner types',
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