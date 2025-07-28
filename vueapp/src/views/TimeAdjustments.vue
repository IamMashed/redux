<template>
	<v-container>

		<h1 class="primary--text">Time Adjustments</h1>

		<v-expansion-panels>

			<v-expansion-panel
				v-for="(county, key) in countiesData"
				:key="key">

				<v-expansion-panel-header>
					<h2>{{ countyFilter(key) }}</h2>
				</v-expansion-panel-header>

				<v-expansion-panel-content>
					<time-adjustments-table
						:data="county"
						:parent-id="key">

					</time-adjustments-table>
				</v-expansion-panel-content>
			</v-expansion-panel>

		</v-expansion-panels>
	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'
import { groupBy } from '../utils'
import countyFilter from '../mixins/countyFilter'
import TimeAdjustmentsTable from '../components/Tables/TimeAdjustmentsTable'

const timeAdjustmentsApi = apiFactory.get('time-adjustments')

export default {
	components: {
		TimeAdjustmentsTable,
	},
	mixins: [
		countyFilter,
	],
	data: () => ({
		items: [],
		countiesData: {},
		headers: [
			{
				text: 'Date',
				value: 'month',
			},
			{
				text: 'Adjustment Delta',
				value: 'value',
			},
			{
				text: 'Adjusted to Date',
				value: 'adjustedToDate'
			},
		],
	}),
	computed: {
		...mapGetters('counties', [
			'counties',
		]),
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		async loadTimeAdjustments() {
			try {
				const { data } = await timeAdjustmentsApi.getAll()
				this.items = data
				this.countiesData = groupBy(this.items, 'county') // TODO: Remove when API is ready
			} catch(error) {
				this.notify({
					text: 'Can not load time adjustments',
					color: 'error'
				}, { root: true })
			}
		},
	},
	mounted() {
		this.loadTimeAdjustments()
	},
}
</script>