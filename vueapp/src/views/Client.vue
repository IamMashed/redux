<template>
	<div>
		<v-toolbar
			dense
			elevation="0">
			<v-app-bar-nav-icon
				@click="toggleSidebar">
			</v-app-bar-nav-icon>

			<v-btn
				class="mr-2"
				icon
				small
				:to="{
					name: 'lookup',
				}">
				<v-icon>mdi-chevron-left</v-icon>
			</v-btn>

			<h1 class="title font-weight-bold mr-12 pr-12">
				Client
			</h1>

			<v-tabs
				v-model="tab"
				class="ml-12">
				<v-tab class="mx-4">
					Main
				</v-tab>
				<v-tab class="mx-4">
					Billing
				</v-tab>
			</v-tabs>
			<v-spacer></v-spacer>

			<v-card-actions
				class="v-card__actions--wide">
				<client-actions
					@delete:client="deleteClient"
					@delete:case="$refs.caseView.deleteCase()">
				</client-actions>
				<v-btn
					color="primary"
					outlined>
					Send Template
				</v-btn>
				<v-btn
					color="secondary"
					outlined>
					Add field
				</v-btn>
				<v-btn
					color="secondary"
					outlined>
					Create App
				</v-btn>
			</v-card-actions>
		</v-toolbar>
		<v-divider></v-divider>

		<v-container>
			<v-tabs-items v-model="tab"
				class="transparent">
				<v-tab-item>
					<v-row>
						<v-col cols="3"
							class="pt-0">
							<client-info
								:client="client"
								@update:client="updateClient">
							</client-info>
						</v-col>

						<v-col cols="9"
							class="pt-0">
							<router-view
								ref="caseView"
								:items="cases">
							</router-view>
						</v-col>
					</v-row>

					<comments-card
						:items="notes"
						@create="createNote">
					</comments-card>
				</v-tab-item>
			</v-tabs-items>
		</v-container>

		<confirm ref="confirm"></confirm>

	</div>
</template>

<script>
import { mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'

import ClientInfo from '../components/Clients/ClientInfo'
import ClientActions from '../components/Clients/ClientActions'
import CommentsCard from '../components/Applications/CommentsCard'
import Confirm from '../components/Confirm'

const clientsApi = apiFactory.get('clients')
const clientNotesApi = apiFactory.get('client-notes')

export default {
	components: {
		ClientInfo,
		ClientActions,
		CommentsCard,
		Confirm,
	},
	props: {
		id: {
			type: Number,
			required: true,
		},
	},
	data: () => ({
		tab: 0,
		client: {},
		notes: [],
	}),
	computed: {
		cases() {
			return this.client?.case_properties || []
		},
	},
	methods: {
		...mapActions('sidebar', {
			toggleSidebar: 'toggle',
		}),
		...mapActions('notification', [
			'notify',
		]),
		async loadClient(id) {
			try {
				const { data } = await clientsApi.get(id)
				this.client = data
			} catch(error) {
				this.notify({
					text: 'Can not load Client',
					color: 'error'
				}, { root: true })
			}
		},
		async updateClient(client) {
			try {
				const confirm = await this.$refs.confirm.open('Update client', 'Are you sure you want to update Client?', { color: 'success' })
				if(confirm) {
					const { data } = await clientsApi.update(client)
					this.client = data
					this.notify({
						text: 'Client updated',
						color: 'success'
					}, { root: true })
				}
			} catch (error) {
				this.notify({
					text: 'Can not update Client',
					color: 'error'
				}, { root: true })
			}
		},
		async deleteClient() {
			try {
				const confirm = await this.$refs.confirm.open(
					'Delete client',
					`Are you certain you want to permanently delete the Client? To continue, type 'delete me' in the dialog box and click Delete`,
					{
						color: 'error',
						width: 400,
						promptText: 'delete me',
					})
				if(confirm) {
					await clientsApi.delete(this.client)
					this.$router.push({
						name: 'lookup',
					})
					this.notify({
						text: 'Client deleted',
						color: 'success'
					}, { root: true })
				}
			} catch (error) {
				this.notify({
					text: 'Can not delete Client',
					color: 'error'
				}, { root: true })
			}
		},
		async loadNotes(clientId) {
			try {
				const { data } = await clientNotesApi.getAll(clientId)
				this.notes = data
			} catch(error) {
				this.notify({
					text: 'Can not load Client Notes',
					color: 'error'
				}, { root: true })
			}
		},
		async createNote(note) {
			try {
				const { data } = await clientNotesApi.create(this.id, note)
				this.notes.unshift(data)
				this.notify({
					text: 'Note added',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not create note',
					color: 'error'
				}, { root: true })
			}
		},
	},
	mounted() {
		this.loadClient(this.id)
		this.loadNotes(this.id)
	},
	watch: {
		'$route.name'() {
			this.loadClient(this.id)
			this.loadNotes(this.id)
		},
	},
}
</script>