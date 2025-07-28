<template>
	<div>
		<v-tooltip ref="tooltip"
			top>
			<template v-slot:activator="{ on, attrs }">
				<p 	ref="apn"
					v-bind="attrs"
					v-on="on"
					class="cursor-pointer"
					@click="copyToClipboard"
					@mousedown="isClicked = true"
					@mouseup="isClicked = false">
					{{ property.apn }}
				</p>
			</template>
			{{ isClicked ? 'Copied 🎉' : 'Copy to Clipboard' }}
		</v-tooltip>
	</div>
</template>

<script>
export default {
	props: {
		feature: {
			type: Object,
			required: true,
		},
	},
	data: () => ({
		isClicked: false,
	}),
	computed: {
		property() {
			return this.feature.properties || {}
		},
	},
	methods: {
		copyToClipboard() {
			var dummy = document.createElement('textarea')
			document.body.appendChild(dummy)
			dummy.value = this.property.apn
			dummy.select()
			document.execCommand('copy')
			document.body.removeChild(dummy)
		},
	},
}
</script>