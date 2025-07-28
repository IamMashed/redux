import { apiFactory } from '@/api/apiFactory'

const usersApi = apiFactory.get('users')

const state = {
	users: [],
}

const getters = {
	users: ({ users }) => users,
}

const mutations = {
	SET_USERS(state, payload) {
		state.users = payload
	},
}

const actions = {
	async loadUsers({ commit, dispatch }) {
		try {
			const { data } = await usersApi.getAll()
			commit('SET_USERS', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load users',
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