<template>
	<div></div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
	computed: {
		...mapGetters('applications', [
			'defaultStatus',
		]),
	},
	methods: {
		...mapActions('applications', [
			'loadCaseInfo',
		]),
		routeToApplication() {
			const { key, applications } = this.defaultStatus
			const route = {
				name: 'application',
				params: {
					id: applications?.[0],
					status: key,
				},
			}
			this.$router.push(route)
		},
	},
	async mounted() {
		await this.loadCaseInfo()
		this.routeToApplication()
	},
}
</script>