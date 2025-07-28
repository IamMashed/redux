<template>
	<div>
		<v-sheet v-cloak
			id="drop-zone"
			class="primary lighten-4 pa-10 text-center primary--text cursor-pointer"
			outlined
			@drop.prevent="handleDropFile"
			@dragover.prevent
			@click="handleDropZoneClick">
			<v-icon
				x-large
				color="primary"
				class="ma-4">
				mdi-file-download-outline
			</v-icon>
			<p>Drop File</p>
		</v-sheet>
		<div class="d-flex align-center">
			<v-file-input
				ref="fileInput"
				v-model="file"
				chips
				:label="label"
				v-bind="attributes"></v-file-input>
			<v-btn
				small
				elevation="0"
				color="primary"
				class="ml-4 text-none"
				:disabled="disabled"
				@click="handleInput">
				<v-icon left>mdi-file-upload</v-icon>
				Upload File
			</v-btn>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		value: {
			type: [ Array, Object, String, Number ],
			required: false,
		},
		label: {
			type: String,
			default: 'Select File',
		},
		multiple: {
			type: Boolean,
			required: false,
			default: false,
		},
	},
	data: () => ({
		file: null,
	}),
	computed: {
		defaultValue() {
			return this.value || null
		},
		multipleAttr() {
			return this.multiple ? 'multiple' : ''
		},
		attributes() {
			return this.multiple
				? { multiple: 'multiple' }
				: {}
		},
		disabled() {
			return this.multiple
				? this.file && !this.file.length > 0
				: !this.file
		}
	},
	methods: {
		handleInput() {
			this.$emit('upload', this.file)
		},
		handleDropFile(e) {
			this.file = e.dataTransfer.files[0]
		},
		handleDropZoneClick() {
			this.$refs?.fileInput?.$refs?.['input']?.click()
		},
		handleFilePaste(e) {
			this.file = e.clipboardData.files[0]
		},
	},
	mounted() {
		window.addEventListener('paste', this.handleFilePaste)
	},
	beforeDestroy() {
        window.removeEventListener('paste', this.handleFilePaste)
	},
}
</script>

<style scoped>
#drop-zone {
	border: 1px dashed;
	border-color: #2c7dad !important;
}
</style>