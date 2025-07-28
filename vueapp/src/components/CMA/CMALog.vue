<template>
	<v-dialog
		v-model="show"
		max-width="1000"
		scrollable>
		<template #activator="{ on, attrs }">
			<v-btn
				color="primary"
				outlined
				v-bind="attrs"
				v-on="on">
				CMA Log
			</v-btn>
		</template>

		<v-card
			:loading="loading">
			<v-card-title>CMA Log</v-card-title>
			<v-divider></v-divider>
			<div
				style="max-height: 80vh;">
				<v-data-table
					:items="rules"
					:headers="headers"
					:items-per-page="-1"
					hide-default-footer
					dense>

					<template #item.enabled="{ value }">
						{{ value | booleanFilter }}
					</template>

					<template #item.plot_removed="{ item }">
						<v-btn
							v-if="item.comps_removed"
							color="primary"
							x-small
							outlined
							@click="plot({ remove_reason: item.rule_key })">
							plot
						</v-btn>
					</template>

					<template #item.plot_added="{ item }">
						<v-btn
							v-if="item.comps_added"
							color="primary"
							x-small
							outlined
							@click="plot({ added_reason: item.rule_key })">
							plot
						</v-btn>
					</template>

					<template #body.append>
						<tr class="font-weight-bold">
							<td>Remaining Comps</td>
							<td></td>
							<td>{{ remainingComps.length }}</td>
						</tr>
					</template>
				</v-data-table>

				<v-container class="mt-5">
					<v-text-field
						v-model="apn"
						outlined
						dense
						placeholder="Search Potential Comp"
						hide-details>
					</v-text-field>
				</v-container>

				<v-list>
					<v-list-item v-for="(item, key) in searchedComp"
						:key="key"
						three-line>
						<v-list-item-content>
							<v-list-item-title class="text-h6">
								<b>{{ item.apn }}</b>
							</v-list-item-title>
							<v-list-item-title>
								{{ item.address }}
							</v-list-item-title>
							<v-list-item-title>
								<span v-if="item.remove_reason">
									Reason not Included: <b>This property failed at {{ item.remove_reason }}</b>
								</span>
								<span v-else>This Comp is one of the available Comps</span>
							</v-list-item-title>
							<v-card-actions>
								<v-btn
									:to="{
										name: 'cma-compare',
										params: {
											id: item.id,
										}
									}"
									target="_blank"
									color="secondary"
									outlined
									small>
									View Property
								</v-btn>
								<v-btn
									color="primary"
									outlined
									small
									@click="plot({ apn: item.apn }), $emit('fly-to', item.id)">
									Plot
								</v-btn>
							</v-card-actions>
						</v-list-item-content>
					</v-list-item>
				</v-list>

				<v-container v-if="apn && searchedComp.length < 1">
					<b>No results found</b>
				</v-container>
			</div>
		</v-card>
	</v-dialog>
</template>

<script>
export default {
	props: {
		rules: {
			type: Array,
			required: true,
		},
		comps: {
			type: Array,
			required: true,
		},
		loading: {
			type: Boolean,
			default: false,
		},
	},
	data: () => ({
		show: false,
		headers: [
			{
				text: 'Rule',
				value: 'rule_key',
			},
			{
				text: 'Enabled',
				value: 'enabled',
			},
			{
				text: 'Comps',
				value: 'comps_count',
			},
			{
				text: 'Removed',
				value: 'comps_removed',
			},
			{
				text: 'Added',
				value: 'comps_added',
			},
			{
				text: 'Show Removed',
				value: 'plot_removed',
			},
			{
				text: 'Show Added',
				value: 'plot_added',
			},
		],
		apn: '',
	}),
	computed: {
		searchedComp() {
			if(this.apn) {
				return this.comps.filter(item => {
					return item.apn.includes(this.apn)
						|| item.address?.toLowerCase().includes(this.apn?.toLowerCase())
				})?.slice(0, 11)
			} else {
				return []
			}
		},
		remainingComps() {
			return this.comps.filter(item => !item.remove_reason)
		},
	},
	methods: {
		plot(filter) {
			this.$emit('plot', filter)
			this.show = false
		},
	},
	watch: {
		show(v) {
			if (v) {
				this.$emit('load-data')
			}
		},
	},
}
</script>