<template>
	<v-data-table
		:items="clients"
		:headers="clientsHeaders"
		:item-class="() => 'cursor-pointer'"
		@click:row="navigateToClient">

		<template #item.full_name="{ value, item }">
			<router-link
				:to="{
					name: 'client',
					params: {
						id: item.id,
					}
				}">
				<v-avatar
					color="grey lighten-2"
					size="40">
					<span class="primary--text font-weight-bold">
						{{ value | initials }}
					</span>
				</v-avatar>
				{{ value }}
			</router-link>
		</template>

		<template #item.tags="{ value }">
			<v-chip
				v-for="(item) in value"
				:key="item.id"
				small
				dark
				class="chip--select-multi ma-1"
				:color="`${colorHash(item.name)} lighten-2`">
				{{ item.name }}
			</v-chip>
		</template>

		<template #item.created_at="{ value }">
			{{ value | date }}
		</template>

	</v-data-table>
</template>

<script>
import colorHash from '../../mixins/colorHash'

export default {
	props: {
		clients: {
			type: Array,
			default: () => ([]),
		},
	},
	mixins: [
		colorHash,
	],
	data: () => ({
		clientsHeaders: [
			{
				text: 'Client',
				value: 'full_name',
			},
			{
				text: 'Physical/Legal Address',
				value: 'mailing_line1', // TODO: check field from client model
			},
			{
				text: 'Tags',
				value: 'tags',
			},
			{
				text: 'Application received',
				value: 'created_at',
			},
		],
	}),
	methods: {
		navigateToClient(item) {
			this.$router.push({
				name: 'client',
				params: {
					id: item.id,
				}
			})
		},
	},
}
</script>