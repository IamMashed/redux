import { apiFactory } from '@/api/apiFactory'
import { keyBy } from '@/utils'

const obsolescencesRulesApi = apiFactory.get('obsolescences-rules')

const state = {
	obsolescences: {},
}

const getters = {
	obsolescences: ({ obsolescences }) => obsolescences,
	transObsolescences: ({ obsolescences }) => {
		return Object.values(obsolescences)
	},
}

const mutations = {
	SET_OBSOLESCENCES(state, payload) {
		state.obsolescences = payload
	},
}

const actions = {
	async loadObsolescences({ commit, dispatch }, county) {
		try {
			const { data } = await obsolescencesRulesApi.getAll({ county })
			commit('SET_OBSOLESCENCES', keyBy(Object.values(data), 'code'))
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load obsolescences',
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