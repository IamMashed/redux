<template>
	<v-container>
		<h1>Edit User</h1>

		<v-card
			outlined>
			<v-card-title>{{ user.username }}</v-card-title>
			<v-divider></v-divider>
			<v-container>
				<v-form>
					<v-text-field
						v-model="user.email"
						label="Email"
						type="email"
						outlined
						dense>
					</v-text-field>
					<v-text-field
						v-model="user.username"
						label="Username"
						outlined
						dense>
					</v-text-field>
					<v-select
						v-model="user.role_id"
						label="Role"
						:items="roles"
						item-text="name"
						item-value="id"
						outlined
						dense>
					</v-select>
					<v-text-field
						v-model="user.password"
						label="password"
						type="password"
						required
						outlined
						dense>
					</v-text-field>
					<v-checkbox
						v-model="user.active"
						label="Active">
					</v-checkbox>
				</v-form>
			</v-container>
			<v-card-actions>
				<template v-if="id">
					<v-btn
						color="success"
						outlined
						@click="updateUser(user)">
						Update
					</v-btn>
					<v-btn
						color="error"
						outlined
						@click="deleteUser(user)">
						Delete
					</v-btn>
				</template>
				<template v-else>
					<v-btn
						color="success"
						outlined
						@click="createUser(user)">
						Create
					</v-btn>
				</template>
			</v-card-actions>
		</v-card>

		<confirm ref="confirm"></confirm>

	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'

const usersApi = apiFactory.get('users')

export default {
	props: {
		id: {
			type: Number,
			required: false,
		},
	},
	data: () => ({
		user: {
			username: '',
			email: '',
			password: '',
			role_id: null,
		},
	}),
	computed: {
		...mapGetters('roles', [
			'roles',
		]),
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		...mapActions('roles', [
			'loadRoles',
		]),
		async loadUser(id) {
			try {
				const { data } = await usersApi.get(id)
				this.user = data
			} catch(error) {
				this.notify({
					text: 'Can not load User',
					color: 'error'
				}, { root: true })
			}
		},
		async createUser(payload) {
			try {
				const confirm = await this.$refs.confirm.open(
					'Create user',
					'Are you sure you want to create User?',
					{ color: 'success' })
				if(confirm) {
					const { data } = await usersApi.create(payload)
					this.$router.push({
						name: 'user',
						params: {
							id:	data.id,
						},
					})
					this.notify({
						text: 'User created',
						color: 'success'
					}, { root: true })
				}
			} catch(error) {
				this.notify({
					text: 'Can not create User',
					color: 'error'
				}, { root: true })
			}
		},
		async updateUser(payload) {
			try {
				const confirm = await this.$refs.confirm.open(
					'Update user',
					'Are you sure you want to update User?',
					{ color: 'success' })
				if(confirm) {
					const { data } = await usersApi.update(payload)
					this.user = data
					this.notify({
						text: 'User update',
						color: 'success'
					}, { root: true })
				}
			} catch(error) {
				this.notify({
					text: 'Can not update User',
					color: 'error'
				}, { root: true })
			}
		},
		async deleteUser(payload) {
			try {
				const confirm = await this.$refs.confirm.open(
					'Delete user',
					'Are you sure you want to delete User?',
					{ color: 'error' })
				if(confirm) {
					await usersApi.delete(payload)
					this.$router.push({
						name: 'admin',
					})
					this.notify({
						text: 'User deleted',
						color: 'success'
					}, { root: true })
				}
			} catch(error) {
				this.notify({
					text: 'Can not delete User',
					color: 'error'
				}, { root: true })
			}
		},
	},
	mounted() {
		if(this.id) {
			this.loadUser(this.id)
		}
		this.loadRoles()
	},
}
</script>