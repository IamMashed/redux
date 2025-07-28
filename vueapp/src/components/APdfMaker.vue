<template>
	<div>
		<slot v-if="!hideContent">
			<v-btn
				color="primary"
				@click="download">
				<slot name="button:title">
					Download PDF
				</slot>
			</v-btn>
		</slot>
	</div>
</template>

<script>
import pdfMake from 'pdfmake/build/pdfmake'
import pdfFonts from 'pdfmake/build/vfs_fonts'
pdfMake.vfs = pdfFonts.pdfMake.vfs

export default {
	props: {
		content: {
			type: Array,
			default: () => ([]),
		},
		styles: {
			type: Object,
			default: () => ({}),
		},
		pageSize: {
			type: String,
			default: 'A4',
		},
		pageMargins: {
			type: Array,
			default: () => ([
				20, 20, 20, 20
			]),
		},
		pageOrientation: {
			type: String,
			default: 'portrait',
		},
		defaultStyle: {
			type: Object,
			default: () => ({}),
		},
		fileName: {
			type: String,
			default: 'Untitled.pdf',
		},
		hideContent: {
			type: Boolean,
			default: false,
		},
	},
	methods: {
		create() {
			return pdfMake.createPdf({
				info: {
					title: this.fileName,
				},
				content: this.content,
				pageSize: this.pageSize,
				pageMargins: this.pageMargins,
				pageOrientation: this.pageOrientation,
				defaultStyle: this.defaultStyle,
				styles: this.styles,
			})
		},
		download() {
			this.create()
				.download(this.fileName)
		},
		open() {
			this.create()
				.open()
		},
		print() {
			this.create()
				.print()
		},
		async getBlob() {
			return new Promise((resolve) => {
				this.create()
					.getBlob(blob => {
						return resolve(blob)
					})
			})
		},
	},
}
</script>