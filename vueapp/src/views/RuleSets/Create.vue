<template>
	<v-container>

		<h1 class="primary--text">Create or Edit a Rule Set</h1>

		<v-card>
			<v-container>
				<v-text-field
					v-model="ruleSet.rule_name"
					label="Rule Name">
				</v-text-field>
				<v-select
					v-model="ruleSet.county"
					:items="counties"
					label="County"
					:disabled="!counties[0]"
					placeholder="Select county"
					item-value="id"
					item-text="name">
				</v-select>
				<v-select
					v-model="ruleSet.town"
					:items="towns"
					label="Town"
					placeholder="Select township"
					item-text="name"
					item-value="name">
				</v-select>
			</v-container>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn :to="{ name: 'rule-sets' }">Cancel</v-btn>
				<v-btn
					@click="createRuleSet">
					Create
				</v-btn>
			</v-card-actions>
		</v-card>

	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../../api/apiFactory'

const townsApi = apiFactory.get('towns')
const ruleSetsApi = apiFactory.get('rule-sets')

export default {
	data: () => ({
		ruleSet: {
			rule_name: '',
			county: null,
			town: null,
		},
		towns: [],
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
		async loadTowns(countyid) {
			try {
				const { data } = await townsApi.getAll(countyid)
				// TODO: Remove this when best API is ready
				this.towns = Object.entries(data).map(([key, val]) => ({
						id: key,
						name: val,
					}))
			} catch(error) {
				this.notify({
					text: 'Can not load towns',
					color: 'error'
				}, { root: true })
			}
		},
		async createRuleSet() {
			try {
				await ruleSetsApi.create(this.ruleSet)
				this.$router.push({ name: 'rule-sets' })
				this.notify({
					text: 'Rule Set created',
					color: 'success'
				}, { root: true })
			} catch(error) {
				this.notify({
					text: 'Can not create Rule Set',
					color: 'error'
				}, { root: true })
			}
		},
	},
	watch: {
		'ruleSet.county'(val) {
			return val && this.loadTowns(val)
		},
	},
}
</script>