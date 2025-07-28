<template>
	<v-container>
		<h1 class="primary--text">Misc Settings</h1>

		<v-tabs vertical
			class="mt-10">
			<v-tab v-for="(county, key) in countiesSettings"
				:key="key">
				{{ countyFilter(county.county) || 'Shared' }}
			</v-tab>

			<v-tab-item v-for="(county, key) in countiesSettings"
				:key="key">
				<v-container>
					<v-card>
						<v-card-text>
							<v-textarea
								v-model="county.settings.pdf_header"
								label="Legal Address"
								outlined
								:disabled="!isAdmin">
							</v-textarea>

							<template
								v-if="county.county === null">
								<h4>Daily Report Email To:</h4>
								<v-combobox
									v-model="county.settings.daily_emails"
									multiple
									chips
									small-chips
									deletable-chips
									outlined
									dense
									:disabled="!isAdmin">
								</v-combobox>
							</template>

							<v-checkbox
								v-model="county.settings.show_formatted_rule_value"
								label="Show formatted rule value in Printed CMA Report">
							</v-checkbox>

						</v-card-text>
						<v-card-actions v-if="isAdmin">
							<v-spacer></v-spacer>
							<v-btn
								color="primary"
								@click="updateSettings(county)">
								Save
							</v-btn>
						</v-card-actions>
					</v-card>
				</v-container>
			</v-tab-item>
		</v-tabs>

	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'
import countyFilter from '../mixins/countyFilter'

const globalSettingsApi = apiFactory.get('global-settings')

export default {
	mixins: [
		countyFilter,
	],
	data: () => ({
		countiesSettings: [],
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
		]),
		...mapGetters('counties', [
			'counties',
		]),
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		async loadSettings() {
			try {
				const { data } = await globalSettingsApi.getAll()
				this.countiesSettings = data
			} catch(error) {
				this.notify({
					text: 'Can not load global settings',
					color: 'error'
				}, { root: true })
			}
		},
		async updateSettings(item) {
			try {
				await globalSettingsApi.update(item)
				this.notify({
					text: 'Settings updated',
					color: 'success'
				}, { root: true })
			} catch(error) {
				this.notify({
					text: 'Can not load global settings',
					color: 'error'
				}, { root: true })
			}
		},
	},
	mounted() {
		this.loadSettings()
	},
}
</script>