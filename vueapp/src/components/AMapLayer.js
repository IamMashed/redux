import { cloneDeep, groupBy } from 'lodash'
import MapService from '../services/map/Map.service'

let clusterGroups = []

export default {
	render() {},
	props: {
		/**
		 * Main Map Layer
		 */
		layer: {
			default: () => ({}),
			type: [Object, String]
		},

		/**
		 * Cluster Layer
		 */
		clusterLayer: {
			default: null,
			type: [Object, String, null]
		},

		/**
		 * Cluster Count Label Layer
		 */
		clusterCountLayer: {
			type: [Object, String, null],
			default: () => ({
				id: 'cluster-count',
				type: 'symbol',
				filter: ['has', 'point_count'],
				layout: {
					'text-field': '{point_count}',
					'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
					'text-size': 14,
				},
				paint: {
					'text-color': '#ffffff',
				},
			})
		},
	},
	data: () => ({
		map: null,
		maxLeavesToSpiderify: 255,
		spiderLeavesCollection: [],
		spiderLegsCollection: [],
	}),
	computed: {
		source() {
			return this.layer?.source
		},
		cluster() {
			return this.source?.cluster || false
		},
		spiderLegsId() {
			return `${this.layer?.id}-spider-legs`
		},
		spiderLeavesId() {
			return `${this.layer?.id}-spider-leaves`
		},
	},
	methods: {
		async deferredMountedTo(map) {
			this.map = map
			this.removeListeners()
			this. removeLayers()
			await this.addLayers()
			this.addListeners()
		},

		async addLayers() {
			if (this.clusterLayer) {
				const {
					source,
					clusterLayer,
					clusterCountLayer,
				} = this

				const {
					layerSource,
					clusterLayerSource,
				} = this.getClusteredSources(source)

				await this.map.addLayer({
					...this.layer,
					source: layerSource,
				})

				await this.map.addLayer({
					...clusterLayer,
					source: clusterLayerSource,
				}, this.layer.id)

				await this.map.addLayer({
					...clusterCountLayer,
					source: clusterLayerSource,
				})
			} else {
				await this.map.addLayer(this.layer)
			}
		},

		/**
		 * Remove all layers
		 */
		removeLayers() {
			this.removeLayer(this.layer.id)
			this.removeLayer(this.clusterLayer?.id)
			this.removeLayer(this.clusterCountLayer?.id)
		},

		/**
		 * Remove layer and it's source by Layer ID
		 * @param {String} layerId Layer ID
		 */
		removeLayer(layerId) {
			if (!layerId) return

			let oldLayer = this.map.getLayer(layerId)

			if (oldLayer) {
				this.map.removeLayer(layerId)
				try {
					this.map.removeSource(oldLayer.source)
				} catch {
					console.warn('Could not remove source', oldLayer.source)
				}
			}
		},

		addListeners() {
			this.map.on('click', this.clickHandler)
			if (this.clusterLayer) {
				this.map.on('sourcedata', this.clusterLoadHandler)
			}
		},

		removeListeners() {
			this.map.off('click', this.clickHandler)
			if (this.clusterLayer) {
				this.map.off('sourcedata', this.clusterLoadHandler)
			}
		},

		clickHandler(e) {

			const features = this.map
				.queryRenderedFeatures(e.point)

			if (this.clusterLayer && features.find(feature => feature?.layer?.id === this.clusterLayer.id)) {
				let clusterFeatures = this.map.queryRenderedFeatures(e.point, {
					layers: [this.clusterLayer?.id]
				})

				const clFeatures = JSON.parse(clusterFeatures[0].properties.features)

				if (this.spiderLeavesCollection.find(feature => {
					const fCoords = feature.properties.cluster_coordinates
					const cCoords = clFeatures[0].geometry.coordinates
					return fCoords[0] === cCoords[0]
						&& fCoords[1] === cCoords[1]
				})) {
					this.unspiderifyCluster(clusterFeatures[0], e)
				} else {
					const spiderifiedCluster = {
						// id: clusterId,
						coordinates: clFeatures[0].geometry.coordinates,
					}
					this.buildSpider(spiderifiedCluster, JSON.parse(features[0].properties.features))
				}
			} 
			
			if ((features.filter(feature => {
				return feature?.layer?.id === this.layer.id
					|| feature?.layer?.id === this.spiderLeavesId
			}).length !== 0)) {
				this.$emit('click', features[0], this.map, e)
			}
		},

		/**
		 * Get clustered source for mapbox layer
		 * @param {Object} source Mapbox layer source
		 * @returns {Object} with unique and clustered features source
		 */
		getClusteredSources(source) {
			let {
				data: { features },
			} = source

			const dup = []
			const uniq = []

			const layerSource = cloneDeep(source)
			const clusterLayerSource = cloneDeep(source)

			features.map((feature) => {
				const founded = features.filter(item => {
					return item.geometry.coordinates[0] === feature.geometry.coordinates[0]
						&& item.geometry.coordinates[1] === feature.geometry.coordinates[1]
				})

				if(founded.length > 1) {
					dup.push(feature)
				} else {
					uniq.push(feature)
				}
			})

			const clusters = Object.values(groupBy(dup, item => item.geometry.coordinates))

			clusterGroups = clusters.map((cluster, index) => ({
				geometry: cluster[0].geometry,
				properties: {
					cluster_id: index,
					cluster_coordinates: cluster[0].geometry.coordinates,
					features: cluster,
					point_count: cluster.length,
				},
			}))

			layerSource.data.features = uniq
			clusterLayerSource.data.features = clusterGroups

			return {
				layerSource,
				clusterLayerSource,
			}
		},

		spiderifyCluster(feature, map, e, callback) {
			let features = this.map.queryRenderedFeatures(e.point, {
				layers: [this.clusterLayer?.id]
			})
			let clusterId = features[0].properties.cluster_id
	
			const spiderifiedCluster = {
				id: clusterId,
				coordinates: feature.geometry.coordinates,
			}

			this.map
				.getSource(this.clusterLayer?.id)
				.getClusterLeaves(
					spiderifiedCluster.id,
					this.maxLeavesToSpiderify,
					0,
					(error, features) => {
						return callback(spiderifiedCluster, features, error)
					})
		},

		unspiderifyCluster(clusterFeature) {
			const spiderLeavesCollection = this.spiderLeavesCollection.filter(leaves => {
				const fCoords = leaves.properties.cluster_coordinates
				const cCoords = JSON.parse(clusterFeature.properties.cluster_coordinates)
				return fCoords[0] !== cCoords[0]
					|| fCoords[1] !== cCoords[1]
			})
			this.$set(this, 'spiderLeavesCollection', spiderLeavesCollection)
			this.addSpiderLegsLayer()
			this.addSpiderLeavesLayer()
		},

		buildSpider(spiderifiedCluster, features) {

			let leavesCoordinates = MapService.generateLeavesCoordinates({
				nbOfLeaves: features.length,
			})

			let clusterXY = this.map.project(spiderifiedCluster.coordinates)

			// Generate spiderlegs and leaves coordinates
			features.forEach((element, index) => {
				let spiderLeafLatLng = this.map.unproject([
					clusterXY.x + leavesCoordinates[index].x,
					clusterXY.y + leavesCoordinates[index].y
				])
		
				this.spiderLeavesCollection.push({
					type: 'Feature',
					geometry: {
						type: 'Point',
						coordinates: [spiderLeafLatLng.lng, spiderLeafLatLng.lat]
					},
					properties: {
						...element.properties,
						cluster_coordinates: spiderifiedCluster.coordinates,
					},
				})
		
				// this.spiderLegsCollection.push({
				// 	type: 'Feature',
				// 	geometry: {
				// 		type: 'LineString',
				// 		coordinates: [
				// 			spiderifiedCluster.coordinates,
				// 			[spiderLeafLatLng.lng, spiderLeafLatLng.lat]
				// 		]
				// 	}
				// })
			})

			// Draw spiderlegs and leaves coordinates
			this.addSpiderLegsLayer()
			this.addSpiderLeavesLayer()
		},

		addSpiderLegsLayer() {
			const source = {
				type: 'geojson',
				data: {
					type: 'FeatureCollection',
					features: this.spiderLegsCollection,
				},
			}

			if (this.map.getLayer(this.spiderLegsId)) {
				this.map.getSource(this.spiderLegsId).setData(source.data)
			} else {
				this.map.addLayer({
					id: this.spiderLegsId,
					type: 'line',
					source,
					paint: {
						'line-width': 4,
						'line-color': 'rgba(128, 128, 128, 0.5)',
					},
				}, this.clusterLayer?.id)
			}
		},

		addSpiderLeavesLayer() {
			const {
				type,
				paint,
				layout,
			} = this.layer

			const source = {
				type: 'geojson',
				data: {
					type: 'FeatureCollection',
					features: this.spiderLeavesCollection
				},
			}

			if (this.map.getLayer(this.spiderLeavesId)) {
				this.map.getSource(this.spiderLeavesId).setData(source.data)
			} else {
				this.map.addLayer({
					id: this.spiderLeavesId,
					type,
					source,
					paint,
					layout,
				})
			}
		},

		clearSpiderifiedCluster() {
			this.spiderLegsCollection = []
			this.spiderLeavesCollection = []
			this.removeLayer(this.spiderLegsId)
			this.removeLayer(this.spiderLeavesId)
		},

		clusterLoadHandler(e) {
			if (this.clusterLayer.id) {
				if (e.sourceId === this.clusterLayer.id) {
					this.$emit('cluster-layer-loaded', clusterGroups)
					this.map.off('sourcedata', this.clusterLoadHandler)
				}
			}
		},
	},
	watch: {
		layer: {
			deep: true,
			handler(newVal) {
				const { source } = newVal
				const { data } = source

				if(this.map && data) {
					if (this.clusterLayer) {
						this.map.on('sourcedata', this.clusterLoadHandler)
						const {
							layerSource,
							clusterLayerSource,
						} = this.getClusteredSources(source)

						this.map.getSource(newVal.id).setData(layerSource.data)
						this.map.getSource(this.clusterLayer?.id).setData(clusterLayerSource.data)
						this.map.getSource(this.clusterCountLayer?.id).setData(clusterLayerSource.data)

						// Clear opened clusters
						this.clearSpiderifiedCluster()
					} else {
						this.map.getSource(newVal.id).setData(data)
					}
				}
				this.map.setLayoutProperty(newVal.id, 'visibility', newVal?.layout?.visibility);
			},
		},
	},
}