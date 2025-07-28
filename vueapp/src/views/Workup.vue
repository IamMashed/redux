<template>
	<v-container>
		<v-row>
			<v-col>
				<v-btn
					color="secondary"
					outlined>
					<v-icon left>mdi-printer</v-icon>
					Print
				</v-btn>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import { mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'

const singleCmaWorkupsApi = apiFactory.get('single-cma-workups')

export default {
	props: {
		id: {
			type: Number,
			required: true,
		},
	},
	data: () => ({
		workup: {},
	}),
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		async loadWorkup(id) {
			try {
				const { data } = await singleCmaWorkupsApi.get(id)
				this.workup = data
			} catch(error) {
				this.notify({
					text: 'Can not load CMA Workup',
					color: 'error'
				}, { root: true })
			}
		},
	},
}
</script>