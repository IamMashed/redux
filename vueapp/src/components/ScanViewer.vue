<template>
	<div class="pan-zoom-container">
		<pan-zoom
			ref="panZoom"
			class="panzoom-container"
			@init="initHandler"
			@zoom="zoomHandler">
			<!-- TODO: store binary with data attribute -->
			<v-img
				:src="`data:image/jpeg;base64, ${value}`">
			</v-img>
		</pan-zoom>
	</div>
</template>

<script>
export default {
	props: {
		value: {
			type: String,
			default: '',
		},
		locked: {
			type: Boolean,
			default: false,
		},
	},
	data: () => ({
		panzoom: null,
		zoom: 1,
	}),
	methods: {
		initHandler(e) {
			this.panzoom = e
		},
		zoomHandler(e) {
			const { scale } = e.getTransform()
			this.zoom = scale
		},
		zoomIn() {
			const { x, y } = this.panzoom.getTransform()
			this.panzoom.smoothZoom(x, y, 1.25)
		},
		zoomOut() {
			const { x, y } = this.panzoom.getTransform()
			this.panzoom.smoothZoom(x, y, 0.8)
		},
		resetView() {
			this.panzoom.moveTo(0, 0)
			this.panzoom.zoomAbs(0, 0, 1)
		},
	},
	watch: {
		value() {
			if(!this.locked) {
				this.resetView()
			}
		},
	},
}
</script>

<style>

.pan-zoom-container {
	overflow: hidden;
	max-height: 53vh;
}

</style>