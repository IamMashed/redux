import { apiFactory } from '@/api/apiFactory'

const applicationSourcesApi = apiFactory.get('application-sources')

const state = {
	applicationSources: [],
}

const getters = {
	applicationSources: ({ applicationSources }) => applicationSources,
}

const mutations = {
	SET_APPLICATION_SOURCES(state, payload) {
		state.applicationSources = payload
	},
}

const actions = {
	async loadApplicationSources({ commit, dispatch }) {
		try {
			const { data } = await applicationSourcesApi.getAll()
			commit('SET_APPLICATION_SOURCES', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load application sources',
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