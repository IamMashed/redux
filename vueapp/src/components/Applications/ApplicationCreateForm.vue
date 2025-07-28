<template>
	<v-dialog v-model="innerValue"
		max-width="500px"
		scrollable>
		<v-card
			elevation="0"
			:loading="isLoading"
			outlined>
			<v-card-title>
				Create new application
			</v-card-title>
			<v-form
				@submit.prevent="createApplication">
				<v-container>
					<v-autocomplete
						v-model="propertyId"
						label="Search Address"
						:items="properties"
						:search-input.sync="address"
						item-text="address"
						item-value="id"
						outlined
						dense>
					</v-autocomplete>
				</v-container>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn
						color="error"
						outlined
						@click="innerValue = false">
						Close
					</v-btn>
					<v-btn
						color="primary"
						type="submit"
						outlined
						:disabled="!propertyId">
						Create
					</v-btn>
				</v-card-actions>
			</v-form>
		</v-card>
	</v-dialog>
</template>

<script>
import { mapActions } from 'vuex'
import { apiFactory } from '../../api/apiFactory'
import { debounce } from 'lodash'

const propertiesApi = apiFactory.get('properties')
const applicationsApi = apiFactory.get('applications')

export default {
	props: {
		value: null,
	},
	data: () => ({
		innerValue: false,
		propertyId: null,
		address: '',
		properties: [],
		isLoading: false,
	}),
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		async search(address) {
			if (!address) return

			this.isLoading = true

			try {
				const params = {
					address,
					limit: 10,
				}
				const { data } = await propertiesApi.getAll(params)
				this.properties = data
			} catch (error) {
				this.notify({
					text: 'Can not find Properties',
					color: 'error'
				}, { root: true })
			} finally {
				this.isLoading = false
			}
		},
		bouncedSearch: debounce(function(address) {
			return this.search(address)
		}, 300),
		async createApplication() {
			try {
				this.isLoading = true
				const application = {
					property_id: this.propertyId,
				}
				const { data } = await applicationsApi.create(application)
				this.propertyId = null
				this.address = ''
				this.$router.push({
					name: 'application',
					params: {
						status: 'incoming',
						id: data.id,
					},
				})
				this.$emit('create')
				this.innerValue = false
			} catch (error) {
				const message = error?.response?.data?.message || ''
				this.notify({
					text: `Can not create Application. ${message}`,
					color: 'error'
				}, { root: true })
			} finally {
				this.isLoading = false
			}
		},
	},
	watch: {
		// Handles internal model changes
		innerValue(newVal) {
			this.$emit('input', newVal)
		},
		// Handles external model changes
		value(newVal) {
			this.innerValue = newVal
		},
		address: 'bouncedSearch',
    },
	created() {
		if (this.value) {
			this.innerValue = this.value
		}
	},
}
</script>