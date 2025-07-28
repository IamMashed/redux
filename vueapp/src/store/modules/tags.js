import Vue from 'vue'
import { apiFactory } from '@/api/apiFactory'

const tagsApi = apiFactory.get('tags')

const state = {
	tags: [],
}

const getters = {
	tags: ({ tags }) => tags,
}

const mutations = {
	SET_TAGS(state, payload) {
		state.tags = payload
	},
}

const actions = {
	async loadTags({ commit, dispatch }) {
		try {
			const { data } = await tagsApi.getAll()
			commit('SET_TAGS', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load tags',
				color: 'error'
			}, { root: true })
		}
	},
	addTag({ commit, getters }) {
		const tag = { name: 'New Tag' }
		const tags = getters['tags']
		commit('SET_TAGS', [ tag, ...tags ])
	},
	async createTag({ commit, dispatch, getters }, tag) {
		const tags = getters['tags']
		try {
			const { data } = await tagsApi.create(tag)
			Vue.set(tags, 0, data)
			commit('SET_TAGS', tags)
			dispatch('notify', {
				text: 'Tag created',
				color: 'success'
			}, { root: true })
		} catch (error) {
			Vue.delete(tags, 0)
			dispatch('notify', {
				text: 'Can not create the tag',
				color: 'error'
			}, { root: true })
		}
	},
	async updateTag({ commit, dispatch, getters }, tag) {
		try {
			const { data } = await tagsApi.update(tag)
			const tags = getters['tags']
			const index = tags.findIndex(item => item.id === data.id)
			Vue.set(tags, index, data)
			commit('SET_TAGS', tags)
			dispatch('notify', {
				text: 'Tag updated',
				color: 'success'
			}, { root: true })
		} catch (error) {
			dispatch('notify', {
				text: 'Can not update the tag',
				color: 'error'
			}, { root: true })
		}
	},
	async deleteTag({ commit, dispatch, getters }, tag) {
		try {
			await tagsApi.delete(tag)
			const tags = getters['tags']
			const index = tags.findIndex(item => item.id === tag.id)
			console.warn('index', index)
			Vue.delete(tags, index)
			commit('SET_TAGS', tags)
			dispatch('notify', {
				text: 'Tag deleted',
				color: 'success'
			}, { root: true })
		} catch (error) {
			dispatch('notify', {
				text: 'Can not delete the tag',
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