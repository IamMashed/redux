import { apiFactory } from '@/api/apiFactory'

const authApi = apiFactory.get('auth')
const PTRC = 'ptrcinternal.redux.tax'
const REDUX = 'reduxinternal.redux.tax'
// const PTRC = '127.0.0.1:5000'

const state = {
	user: {},
}

const getters = {
	user: ({ user }) => user,
	userRole: ({ user }) => user.user_role,
	isLoggedIn: ({ user }) => !!user.user_id,
	isAdmin: ({ user }) => user.user_role === 'admin',
	isMember: ({ user }) => user.user_role === 'member',
	isViewer: ({ user }) => user.user_role === 'viewer',
	isGuest: ({ user }) => user.user_role === 'guest',
	isPTRC: ({ user }) => user.domain === PTRC,
	isREDUX: ({ user }) => user.domain === REDUX,
}

const mutations = {
	SET_USER(state, payload) {
		state.user = payload
	},
}

const actions = {
	async loadUser({ commit, dispatch }) {
		try {
			const { data } = await authApi.user()
			commit('SET_USER', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load user data',
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