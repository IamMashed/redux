<template>
	<v-btn
		@click="loadData"
		icon
		:loading="loading"
		color="primary">
		<slot>
			<v-icon>
				mdi-file-download
			</v-icon>
		</slot>
	</v-btn>
</template>

<script>
import { mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'
import Blob from 'blob'
import { saveAs } from 'file-saver'

const notesApi = apiFactory.get('notes')

export default {
	props: {
		id: {
			type: Number,
			required: true,
		},
		name: {
			type: String,
			required: true,
		},
	},
	data: () => ({
		data: null,
		loading: false,
	}),
	computed: {
		encoding() {
			return this.type === '.pdf'
				? 'latin1'
				: 'utf8'
		},
		filename() {
			return `${this.name}${this.type}`
		},
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		/**
		 * Load Note data
		 */
		async loadData() {
			try {
				this.loading = true
				const { data } = await notesApi.get(this.id)
				const { attachment, attachment_extension } = data
				this.data = attachment
				this.type = attachment_extension

				await this.download()
			} catch (error) {
				this.notify({
					text: 'Can not load Data',
					color: 'error'
				}, { root: true })
			}
		},
		/**
		 * Fetch data as blob and download it
		 */
		async download() {
			try {
				this.loading = true
				const data = Buffer.from(this.data, this.encoding)
				const blob = new Blob([ data ]) // NOTE: it's fallback for Blob API
				saveAs(blob, this.filename)
			} catch (error) {
				console.error(error)
			} finally {
				this.loading = false
			}
		},
	},
}
</script>