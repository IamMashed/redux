import { apiFactory } from '@/api/apiFactory'
import { keyBy } from '@/utils'

const adjustmentsApi = apiFactory.get('adjustments')

const state = {
	adjustments: [],
}

const getters = {
	adjustments: ({ adjustments }) => adjustments,
	transAdjustments: ({ adjustments }) => {
		return keyBy(adjustments, 'key')
	},
}

const mutations = {
	SET_ADJUSTMENTS(state, payload) {
		state.adjustments = payload
	},
}

const actions = {
	async loadAdjustments({ commit, dispatch }) {
		try {
			const { data } = await adjustmentsApi.getAll()
			commit('SET_ADJUSTMENTS', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load adjustments',
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