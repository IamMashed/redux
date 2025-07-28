<template>
<div>
	<v-data-table
		:items="items"
		:headers="headers">

		<template #top
			v-if="isAdmin">
			<div class="d-flex justify-end my-4">
				<v-btn
					v-if="!editable"
					depressed
					color="secondary"
					class="mx-1"
					@click="edit">
					<v-icon left>mdi-pencil</v-icon>
					Edit
				</v-btn>

				<template v-else>
					<v-btn
						depressed
						color="error"
						class="mx-1"
						@click="cancel">
						<v-icon left>mdi-close</v-icon>
						Cancel
					</v-btn>

					<v-btn
						depressed
						color="success"
						class="mx-1"
						@click="save">
						<v-icon left>mdi-upload</v-icon>
						Save
					</v-btn>
				</template>
			</div>
		</template>

		<template
			v-for="year in years"
			v-slot:[`item.ratios.${year}.value`]="{ item }">
			<v-autonumeric
				v-if="item.ratios[year]"
				:key="year"
				v-model.number="item.ratios[year].value"
				single-line
				hide-details
				placeholder="0"
				class="align-right"
				:disabled="!editable"
				:an-options="{ decimalPlaces: 4 }"
				@blur="queue.push(item.ratios[year])">
			</v-autonumeric>
		</template>
	</v-data-table>

	<confirm ref="confirm"></confirm>

</div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../../api/apiFactory'
import Confirm from '../../components/Confirm'

const ratiosApi = apiFactory.get('ratios')

export default {
	components: {
		Confirm,
	},
	props: {
		ratiosset: {
			type: Array,
			required: true,
		},
		years: {
			type: Array,
			required: true,
		},
	},
	data: () => ({
		editable: false,
		items: [],
		itemsCopy: [],
		queue: [],
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
		]),
		headers() {
			return [
				{
					text: 'Town',
					value: 'name',
				},
				{
					text: 'District',
					value: 'description',
				},
				...this.years.map(year => {
					return {
						text: year,
						value: `ratios.${year}.value`,
					}
				}),
			]
		},
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		edit() {
			this.itemsCopy = JSON.parse(JSON.stringify(this.items))
			this.editable = true
		},
		cancel() {
			this.items = JSON.parse(JSON.stringify(this.itemsCopy))
			this.editable = false
		},
		async save() {
			try {
				const confirm = await this.$refs.confirm.open('Submit Ratios data', 'Are you sure you want to make changes to the Ratios?', { color: 'success' })
				if(confirm) {
					await Promise.all(this.queue.map(async r => {
						return await this.saveRatio(r)
					}))
					this.notify({
						text: 'Ratios updated',
						color: 'success'
					}, { root: true })
				} else {
					this.cancel()
				}
				return this.editable = false
			} catch (error) {
				this.notify({
					text: 'Error while ratios update',
					color: 'error'
				}, { root: true })
			}
		},
		async saveRatio(ratio) {
			try {
				if(ratio.id) {
					await ratiosApi.update(ratio)
				} else {
					const { data } = await ratiosApi.create(ratio)
					const index = this.items.findIndex(item => item.id === ratio.ratios_settings_id)
					this.$set(this.items[index].ratios, ratio.year,
						{
							...this.items[index].ratios[ratio.year],
							id: data.id
						})
				}
			} catch (error) {
				this.notify({
					text: 'Can not update ratio',
					color: 'error'
				}, { root: true })
			}
		},
	},
	mounted() {
		this.items = JSON.parse(JSON.stringify(this.ratiosset))
	},
}
</script>