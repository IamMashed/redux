<template>
	<v-data-table
		:items="cases"
		:headers="casesHeaders"
		:item-class="() => 'cursor-pointer'"
		@click:row="navigateToCase">

		<template #item.apn="{ value, item }">
			<router-link
				:to="{
					name: 'client-case',
					params: {
						id: item.client_id,
						caseid: item.id,
					}
				}">
				{{ value }}
			</router-link>
		</template>

		<template #item.assessment.value="{ value }">
			{{ value | bignum }}
		</template>

		<template #item.hearing_date="{ value }">
			{{ value | date }}
		</template>

		<template #item.workups="{ value, item }">
			<router-link
				:to="{
					name: 'client-case',
					params: {
						id: item.client_id,
						caseid: item.id,
					},
					hash: '#saved-cma',
				}">
				{{ value.length }}
			</router-link>
		</template>

	</v-data-table>
</template>

<script>
export default {
	props: {
		cases: {
			type: Array,
			default: () => ([]),
		},
	},
	data: () => ({
		casesHeaders: [
			{
				text: 'Folio',
				value: 'apn',
			},
			{
				text: 'Address',
				value: 'full_address',
			},
			{
				text: 'Client name',
				value: 'client.full_name',
			},
			{
				text: 'Assessment value',
				value: 'assessment.value',
			},
			{
				text: 'Hearing Date',
				value: 'hearing_date',
			},
			{
				text: 'Workups',
				value: 'workups',
			},
		],
	}),
	methods: {
		navigateToCase(item) {
			this.$router.push({
				name: 'client-case',
				params: {
					id: item.client_id,
					caseid: item.id,
				}
			})
		},
	},
}
</script>