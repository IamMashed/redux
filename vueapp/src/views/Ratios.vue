<template>
	<v-container>
		<h1 class="primary--text">Assessment Ratios</h1>

		<div
			v-for="(ratiosset, key) in ratiossets"
			:key="key">

			<h2>{{ countyFilter(key) }}</h2>

			<ratiosset-table
				:ratiosset="ratiosset"
				:years="years">
			</ratiosset-table>
			
		</div>

	</v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { apiFactory } from '../api/apiFactory'
import { groupBy, keyBy } from '../utils'
import countyFilter from '../mixins/countyFilter'

import RatiossetTable from '../components/Tables/RatiossetTable'

const ratiossetsApi = apiFactory.get('ratiossets')

export default {
	components: {
		RatiossetTable,
	},
	mixins: [
		countyFilter,
	],
	data: () => ({
		ratiossets: [],
	}),
	computed: {
		...mapGetters('years', [
			'years',
		]),
		...mapGetters('counties', [
			'counties',
		]),
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		/**
		 * Populate ratios years if not exists
		 */
		populateYears(arr, parentId) {
			this.years.map(year => {
				if(!arr.hasOwnProperty(year)) {
					arr[year] = {
						value: null,
						year,
						ratios_settings_id: parentId,
					}
				}
			})
			return arr
		},
		async loadRatios() {
			try {
				const { data } = await ratiossetsApi.getAll()
				this.ratiossets = data

				this.ratiossets = data.map(i => {
					i.ratios = keyBy(i.ratios, 'year')
					i.ratios = this.populateYears(i.ratios, i.id)
					return i
				})

				this.ratiossets = groupBy(data, 'county')

			} catch(error) {
				this.notify({
					text: 'Can not load ratios',
					color: 'error'
				}, { root: true })
			}
		},
	},
	mounted() {
		this.loadRatios()
	},
}
</script>