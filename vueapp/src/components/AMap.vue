<template>
	<div ref="map" class="map"
		:style="mapStyle">
		<slot :map="map"></slot>
	</div>
</template>

<script>
import mapboxgl from 'mapbox-gl/dist/mapbox-gl'

mapboxgl.accessToken =
	'pk.eyJ1IjoicmVkdXgxIiwiYSI6ImNrNXpnMzkzYzJyMmIzbG5uM2xlZGJjdWwifQ._0ovg99Mq_VwbVTmrUrJPw'

export default {
	props: {
		styleId: {
			type: String,
			// default: 'navigation-preview-night-v4',
			default: 'light-v9',
		},
		center: {
			type: Array,
			required: true,
		},
		zoom: {
			type: Number,
			default: 15,
		},
		layers: {
			type: Array,
			default: () => ([]),
		},
		images: {
			type: Array,
			default: () => ([
				{
					name: 'map-marker-sbj',
					url: '/static/images/marker-sbj.png',
				},
				{
					name: 'map-marker-good',
					url: '/static/images/marker-good.png',
				},
				{
					name: 'map-marker-good-selected',
					url: '/static/images/marker-good-selected.png',
				},
				{
					name: 'map-marker-bad',
					url: '/static/images/marker-bad.png',
				},
				{
					name: 'map-marker-bad-selected',
					url: '/static/images/marker-bad-selected.png',
				},
			]),
		},
		width: {
			required: false,
			default: '100%',
		},
		height: {
			required: false,
			default: '100%',
		},
	},
	data: () => ({
		map: null,
		resolve: null,
		reject: null,
	}),
	computed: {
		mapStyle() {
			return {
				width: this.width,
				height: this.height,
			}
		},
	},
	methods: {
		async initMap() {
			this.map = new mapboxgl.Map({
				container: this.$refs.map,
				style: `mapbox://styles/${this.styleId}`,
				zoom: this.zoom,
				center: this.center,
				preserveDrawingBuffer: true,
			})

			this.map.addControl(new mapboxgl.NavigationControl(), 'top-right')
			
			this.map.on('style.load', () => {
				this.addLayers(this.layers)
			})
			this.map.on('load', async () => {
				await this.addLayers(this.layers)
			})

			// When a click event occurs on a feature in the beaches layer, open a popup at the
			// location of the feature, with description HTML from its properties.
			// this.map.on('click', 'beaches', (e) => {
			// 	this.$emit('click', e.features[0])
			// 	// var coordinates = e.features[0].geometry.coordinates.slice();
			// 	// var description = e.features[0].properties.priority;
				
			// 	// // Ensure that if the map is zoomed out such that multiple
			// 	// // copies of the feature are visible, the popup appears
			// 	// // over the copy being pointed to.
			// 	// while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
			// 	// 	coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
			// 	// }
				
			// 	// new mapboxgl.Popup()
			// 	// 	.setLngLat(coordinates)
			// 	// 	.setHTML(`Пріоритетність: ${description}`)
			// 	// 	.addTo(this.map);
			// });

			// this.map.on('click', (e) => {
			// 	console.error(e)
			// })
			
			// Change the cursor to a pointer when the mouse is over the beaches layer.
			// this.map.on('mouseenter', 'beaches', () => {
			// 	this.map.getCanvas().style.cursor = 'pointer';
			// });
			
			// // Change it back to a pointer when it leaves.
			// this.map.on('mouseleave', 'beaches', () => {
			// 	this.map.getCanvas().style.cursor = '';
			// });

			this.map.on('sourcedata', (e) => {
				if (e.isSourceLoaded) {
					// console.warn('SOURCE DATA LOADED')
					this.$emit('source-data-loaded', e)
					this.resolve()
				}
			})

			await this.waitForLoad()
			return this.$emit('map-loaded')

		},
		// addLayers(layers) {
		// 	return layers.forEach(layer => {
		// 		this.map.addLayer(layer)
		// 	})
		// },
		async addLayers () {
			// let [...children] = this.$children
			// TODO: consider sorting or using slots if we run to render order problems
			// children.sort(child => {
			//   return child.key
			// })

			this.images.map(item => {
				this.map.loadImage(item.url, (error, image) => {
					if (error) throw error

					// Add map-marker image if not exists
					const imageId = item.name
					if(!this.map.hasImage(imageId)) {
						this.map.addImage(imageId, image, {
							// 'sdf': 'true'
						})
					}

					Promise.all(this.$children.map(async (child) => {
						if(child.deferredMountedTo) await child.deferredMountedTo(this.map)
					}))
				})
			})
		},
		waitForLoad() {
			return new Promise((resolve, reject) => {
				this.resolve = resolve
				this.reject = reject
			})
		},
		setStyle(styleId) {
			this.map.setStyle('mapbox://styles/' + styleId)
		},
	},
	async mounted() {
		await this.initMap()
		this.$emit('mounted')
	},
	watch: {
		styleId(newVal) {
			this.map.setStyle(`mapbox://styles/${newVal}`)
		},
		center: {
			deep: true,
			handler(newVal) {
				if(this.map) this.map.flyTo({ center: newVal })
			},
		},
	},
}
</script>

<style>
@import url('https://api.tiles.mapbox.com/mapbox-gl-js/v1.6.1/mapbox-gl.css');
</style>