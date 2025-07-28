import { apiFactory } from '@/api/apiFactory'

const rolesApi = apiFactory.get('roles')

const state = {
	roles: [],
}

const getters = {
	roles: ({ roles }) => roles,
}

const mutations = {
	SET_ROLES(state, payload) {
		state.roles = payload
	},
}

const actions = {
	async loadRoles({ commit, dispatch }) {
		try {
			const { data } = await rolesApi.getAll()
			commit('SET_ROLES', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load roles',
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