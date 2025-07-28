import { groupBy, flatten } from 'lodash'
import mapboxgl from 'mapbox-gl/dist/mapbox-gl'
import MapService from '../map/Map.service'

const mapboxUrl = process.env.VUE_APP_MAPBOX_URL
const mapboxToken = process.env.VUE_APP_MAPBOX_TOKEN
const mapboxMarkerUrl = process.env.VUE_APP_MAPBOX_MARKER_URL

const MapboxApi = {
	
	/**
	 * Generate Map Image URL from Mapbox Static API
	 * 
	 * @param {String} styleId username and style id, e.g. `mapbox/satellite-v9`
	 * @param {Object} geojson valid geojson data
	 * @param {Number} width image width in px
	 * @param {Number} height image height in px
	 * 
	 * @returns {String} Map Image URL
	 */
	genStaticMapURL({
		styleId,
		geojson,
		pins,
		markers,
		width = 1123,
		height = 794,
	}) {
		const overlays = []

		if (geojson) {
			overlays.push(`geojson(${JSON.stringify(geojson)})`)
		}
		
		if (pins) {
			overlays.push(this.genPinsOverlay(pins))
		}

		if (markers) {
			overlays.push(this.genMarkersOverlay(markers))
		}

		const overlay = overlays.join(',')

		const mapOptions = this.getMapOptions(markers)

		let {
			bearing,
			center: {
				lng,
				lat,
			},
			zoom,
		} = mapOptions

		// Increase zoom cause it so small
		if (zoom <= 17.25) {
			zoom += 0.75
		} else {
			zoom = 18
		}

		return `${mapboxUrl}/${styleId}/static/${overlay}/${lng},${lat},${zoom},${bearing}/${width}x${height}@2x?access_token=${mapboxToken}`
	},
	
	/**
	 * Generate Pins Overlay for Mapbox Static API
	 * 
	 * @param {Array} pins array of pins
	 * 
	 * @returns {String} pins overlay
	 * 
	 * @example `pin-l-s+000(50.0000,30.0000)`
	 */
	genPinsOverlay(pins) {
		return pins.map(({
			label,
			color = 'fff',
			coords: [lon, lat],
		}) => {
			return `pin-l-${label}+${color}(${lon},${lat})`
		}).join(',')
	},
	
	/**
	 * Generate Markers Overlay for Mapbox Static API
	 * 
	 * @param {Array} markers array of pins
	 * 
	 * @returns {String} markers overlay
	 * 
	 * @example `url-some-url(50.0000,30.0000)`
	 */
	genMarkersOverlay(markers) {
		markers = flatten(this.genClusteredPins(markers))

		return markers.map(({
			label,
			coords: [lon, lat],
		}) => {
			const { protocol, hostname, port } = window.location
			const baseUrl = process.env.NODE_ENV === 'production'
				? `${protocol}//${hostname}:${port}${mapboxMarkerUrl}`
				: mapboxMarkerUrl
			const encodedURL = encodeURIComponent(`${baseUrl}/marker-label-${label}.png`)
			return `url-${encodedURL}(${lon},${lat})`
		}).join(',')
	},

	/**
	 * Get mapbox map options based on coords
	 * @param {Array} markers array of markers
	 */
	getMapOptions(markers) {
		var bounds = new mapboxgl.LngLatBounds()
		markers.forEach(item => bounds.extend(item.coords))

		const map = new mapboxgl.Map({
			container: document.createElement('div'),
		})
		return map.cameraForBounds(bounds)
	},

	/**
	 * Get map instance bounded to marker coords
	 * @param {Array} markers array of markers
	 */
	createMap(markers) {
		var bounds = new mapboxgl.LngLatBounds()
		markers.forEach(item => bounds.extend(item.coords))

		const map =  new mapboxgl.Map({
			container: document.createElement('div'),
		})
		const mapOptions = map.cameraForBounds(bounds)
		let {
			center,
			zoom,
		} = mapOptions

		if (zoom <= 17.25) {
			zoom += 0.75
		} else {
			zoom = 18
		}

		map.setCenter(center)
		map.setZoom(zoom)

		return map
	},

	/**
	 * Generate clustered coordinates if same used
	 * @param {Array} markers
	 */
	genClusteredPins(markers) {
		const map = this.createMap(markers)
		const ma = groupBy(markers, ({ coords: [ lon, lat ] }) => `${lon},${lat}`);

		return Object.values(ma).map(group => {
			if (group.length > 1) {
				const leavesCoordinates = MapService.generateLeavesCoordinates({
					nbOfLeaves: group.length,
					options: {
						distanceBetweenPoints: 22,
						rotationsModifier: 1250,
						radiusModifier: 50000,
						lengthModifier: 1000,
					},
				})

				const XY = map.project(group[0].coords)

				return group.map((marker, index) => {
					let spiderLeafLatLng = map.unproject([
						XY.x + leavesCoordinates[index].x,
						XY.y + leavesCoordinates[index].y
					])

					const coords = [
						spiderLeafLatLng.lng,
						spiderLeafLatLng.lat,
					]

					return {
						...marker,
						coords,
					}
				})
			} else {
				return group
			}
		})
	},

	/**
	 * Randomize Pin coordinates
	 * @param {Object} marker Marker
	 */
	randomizeCoords(marker) {
		let { coords: [ lon, lat ] } = marker

		const bbox = [
			lon - 0.0001,
			lat - 0.0001,
			lon + 0.0001,
			lat + 0.0001
		]
		const coords = this.coordInBBox(bbox)

		return {
			...marker,
			coords,
		}
	},

	/**
	 * Generate random in bbox
	 * @param {Array} bbox coordinate bbox
	 */
	coordInBBox(bbox) {
		return [
			Math.random() * (bbox[2] - bbox[0]) + bbox[0],
			Math.random() * (bbox[3] - bbox[1]) + bbox[1],
		]
	},
}

export default MapboxApi