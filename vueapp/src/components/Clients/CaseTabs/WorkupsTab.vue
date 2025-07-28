<template>
	<v-container class="pa-4">
		<v-data-table
			:items="workups"
			:headers="headers"
			:items-per-page="-1"
			hide-default-footer>

			<template #item.is_primary="{ item }">
				<v-checkbox
					v-model="item.is_primary"
					class="ma-0"
					hide-details
					@change="updateWorkup(item)">
				</v-checkbox>
			</template>

			<template #item.created_at="{ value }">
				{{ value | date }}
			</template>

			<template #item.goodbad="{ item }">
				<v-card-actions>
					<v-btn
						:href="`${VUE_APP_API}files/${item.good_bad_report_file_id}`"
						target="_blank"
						color="info"
						outlined
						depressed
						small>
						Download
					</v-btn>
				</v-card-actions>
			</template>

			<template #item.action="{ item }">
				<v-card-actions>
					<!-- <v-btn
						:to="{
							name: 'workup',
							params: {
								id: item.id,
							},
						}"
						color="info"
						outlined
						depressed
						small>
						View
					</v-btn> -->
					<v-btn
						:href="`${VUE_APP_API}files/${item.report_file_id}`"
						target="_blank"
						color="info"
						outlined
						depressed
						small>
						Download
					</v-btn>
					<v-btn
						color="error"
						outlined
						depressed
						small
						@click="deleteWorkup(item.id)">
						Delete
					</v-btn>
				</v-card-actions>
			</template>
		</v-data-table>
	</v-container>
</template>

<script>
import { mapActions } from 'vuex'
import { apiFactory } from '../../../api/apiFactory'

const casesApi = apiFactory.get('cases')
const singleCmaWorkupsApi = apiFactory.get('single-cma-workups')

export default {
	props: {
		case: {
			type: Object,
			required: true,
		},
	},
	data: () => ({
		VUE_APP_API: process.env.VUE_APP_API,
		workups: [],
		headers: [
			{
				text: 'Primary',
				value: 'is_primary',
			},
			{
				text: 'Created At',
				value: 'created_at',
			},
			{
				text: 'Good/Bad report',
				value: 'goodbad',
			},
			{
				text: 'Action',
				value: 'action',
			},
		],
	}),
	methods: {
		...mapActions('notification', [
			'notify',
		]),

		async loadWorkups() {
			try {
				const { id } = this.case
				const { data } = await casesApi.singleCmaWorkups(id)
				this.workups = data
			} catch (error) {
				this.notify({
					text: 'Can not load Workups',
					color: 'error'
				}, { root: true })
			}
		},

		async updateWorkup(payload) {
			try {
				await singleCmaWorkupsApi.update(payload)
				this.notify({
					text: 'Workup updated',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not update Workup',
					color: 'error'
				}, { root: true })
			}
		},

		async deleteWorkup(id) {
			try {
				await singleCmaWorkupsApi.delete(id)
				const index = this.workups.findIndex(item => item.id === id)
				this.$delete(this.workups, index)
				this.notify({
					text: 'Workup deleted',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not delete Workup',
					color: 'error'
				}, { root: true })
			}
		},
	},
	watch: {
		'case.id': {
			immediate: true,
			handler: function (val) {
				if (val) {
					this.loadWorkups()
				}
			}
		}
	},
}
</script>