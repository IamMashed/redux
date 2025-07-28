<template>
	<div></div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'

export default {
	computed: {
		...mapGetters('auth', [
			'isREDUX',
		]),
	},
	methods: {
		...mapActions('auth', [
			'loadUser',
		]),
		...mapMutations('auth', [
			'SET_USER',
		]),
		async route() {
			// NOTE: Unset user to allow normal data loading 
			// inside beforeEach route hook
			this.SET_USER({})
			await this.loadUser()
			console.warn('Is site redux?', this.isREDUX)
			const homeRoute = this.isREDUX ? 'applications' : 'cma'
			this.$router.replace(homeRoute)
		},
	},
	async mounted() {
		this.route()
	},
}
</script>
