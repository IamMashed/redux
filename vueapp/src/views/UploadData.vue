<template>
	<v-container>

		<h1 class="primary--text">Upload Data</h1>

		<v-expansion-panels>

			<v-expansion-panel
				v-for="(datamapper, index) in datamappers"
				:key="index">

				<v-expansion-panel-header>
					<h2>{{ datamapper.name }}</h2>
				</v-expansion-panel-header>

				<v-expansion-panel-content>
					<v-alert
						color="info"
						dense
						text>
						Please map Excel columns to database fields
					</v-alert>
					<v-row>
						<v-col
							v-for="(field, key) in datamapper.fields"
							:key="key">
							<v-text-field
								v-model="datamappers[index].fields[key]"
								:label="key"
								outlined
								dense>
							</v-text-field>
						</v-col>
					</v-row>

					<photo-upload
						ref="photoUpload"
						@upload="(file) => processFile(file, datamapper)">
					</photo-upload>
				</v-expansion-panel-content>
			</v-expansion-panel>

		</v-expansion-panels>
	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'

import PhotoUpload from '../components/PhotoUpload'

const datamappersApi = apiFactory.get('datamappers')
const uploadApi = apiFactory.get('upload')

export default {
	components: {
		PhotoUpload,
	},
	data: () => ({
		datamappers: [],
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
		async loadDataMappers() {
			try {
				const { data } = await datamappersApi.getAll()
				this.datamappers = data
			} catch(error) {
				this.notify({
					text: 'Can not load Data Mappers',
					color: 'error'
				}, { root: true })
				throw error
			}
		},

		async updateDatamapper(payload = Object) {
			try {
				await datamappersApi.update(payload)
			} catch(error) {
				this.notify({
					text: 'Can not update Data Mapper',
					color: 'error'
				}, { root: true })
			}
		},

		/**
		 * Upload File
		 */
		async uploadFile(file = File, datamapper = Object) {
			try {
				const datamapperName = datamapper.name

				let formData = new FormData()
				formData.append(`${datamapperName}_file`, file)
				await uploadApi[datamapperName](formData)

				this.notify({
					text: 'File Uploaded',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not upload File',
					color: 'error'
				}, { root: true })
				throw error
			}
		},

		async processFile(file = File, datamapper = Object) {
			await this.updateDatamapper(datamapper)
			await this.uploadFile(file, datamapper)
		},
	},
	mounted() {
		this.loadDataMappers()
	},
}
</script>