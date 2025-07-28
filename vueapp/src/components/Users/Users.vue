<template>
	<v-container>
		<v-data-table
			:items="users"
			:headers="headers">

			<template #top>
				<v-card-actions>
					<v-btn
						:to="{
							name: 'user-create',
						}"
						color="success"
						outlined>
						Create
					</v-btn>
				</v-card-actions>
			</template>

			<template #item.actions="{ item }">
				<v-btn
					:to="{
						name: 'user',
						params: {
							id: item.id,
						},
					}"
					color="success"
					outlined
					small>
					Edit
				</v-btn>
			</template>
		</v-data-table>
	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
	data: () => ({
		headers: [
			{
				text: 'ID',
				value: 'id',
			},
			{
				text: 'Email',
				value: 'email',
			},
			{
				text: 'Username',
				value: 'username',
			},
			{
				text: 'Role',
				value: 'role.name',
			},
			{
				text: 'Edit',
				value: 'actions',
			},
		],
	}),
	computed: {
		...mapGetters('users', [
			'users',
		]),
	},
	methods: {
		...mapActions('users', [
			'loadUsers',
		]),
	},
	mounted() {
		this.loadUsers()
	},
}
</script>