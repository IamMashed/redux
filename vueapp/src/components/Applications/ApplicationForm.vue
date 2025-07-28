<template>
	<v-card
		elevation="0"
		height="100%"
		outlined
		class="py-1">
		<v-card-title>
			Application Form
			<v-spacer></v-spacer>
			<v-btn
				:color="scanViewLocked ? 'primary' : 'dark'"
				@click="scanViewLocked = !scanViewLocked"
				icon>
				<v-icon>{{ scanViewLocked ? 'mdi-pin' : 'mdi-pin-outline' }}</v-icon>
			</v-btn>
			<v-btn @click="$refs.scanView.zoomIn()" icon>
				<v-icon>mdi-magnify-plus-outline</v-icon>
			</v-btn>
			<v-btn @click="$refs.scanView.zoomOut()" icon>
				<v-icon>mdi-magnify-minus-outline</v-icon>
			</v-btn>
			<v-btn @click="$refs.scanView.resetView()" icon>
				<v-icon>mdi-fullscreen</v-icon>
			</v-btn>
			<v-btn @click="rotateScan(false)" icon>
				<v-icon>mdi-rotate-left</v-icon>
			</v-btn>
			<v-btn @click="rotateScan90()" icon>
				<v-icon>mdi-rotate-3d-variant</v-icon>
			</v-btn>
			<v-btn @click="rotateScan" icon>
				<v-icon>mdi-rotate-right</v-icon>
			</v-btn>
		</v-card-title>

		<v-container>
			<scan-viewer
				ref="scanView"
				:value.sync="value"
				:locked="scanViewLocked">
			</scan-viewer>
		</v-container>
	</v-card>
</template>

<script>
import ScanViewer from '../ScanViewer'

export default {
	components: {
		ScanViewer,
	},
	props: {
		value: {
			type: String,
			default: '',
		},
	},
	data: () => ({
		scanViewLocked: false,
	}),
	methods: {
		async rotateScan(isClockwise = true) {
			const newVal = await this.rotateBase64Image90deg(this.value, isClockwise)
			return this.$emit('input', newVal)
		},
		async rotateScan90() {
			let newVal = await this.rotateBase64Image90deg(this.value)
			newVal = await this.rotateBase64Image90deg(newVal)
			return this.$emit('input', newVal)
		},
		rotateBase64Image90deg(base64Image, isClockwise) {
			return new Promise((resolve, reject) => {
				// create an off-screen canvas
				let offScreenCanvas = document.createElement('canvas')
				let offScreenCanvasCtx = offScreenCanvas.getContext('2d')

				// cteate Image
				// TODO: store binary with data attribute
				let img = new Image()
				img.src = `data:image/jpeg;base64, ${base64Image}`
				
				img.onload = function() {

					// set its dimension to rotated size
					offScreenCanvas.height = img.width
					offScreenCanvas.width = img.height

					// rotate and draw source image into the off-screen canvas:
					if (isClockwise) { 
						offScreenCanvasCtx.rotate(90 * Math.PI / 180)
						offScreenCanvasCtx.translate(0, -offScreenCanvas.width)
					} else {
						offScreenCanvasCtx.rotate(-90 * Math.PI / 180)
						offScreenCanvasCtx.translate(-offScreenCanvas.height, 0)
					}
					offScreenCanvasCtx.drawImage(img, 0, 0)

					// encode image to data-uri with base64
					let result = offScreenCanvas.toDataURL('image/jpeg', 100)
					result = result.split(',')?.[1]
					return resolve(result)
				}

				img.onerror = reject
			})
		},
	},
}
</script>