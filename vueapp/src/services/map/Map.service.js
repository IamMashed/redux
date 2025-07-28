const MapService = {

	generateEquidistantPointsInCircle: function ({
		totalPoints = 1,
		options = {
			distanceBetweenPoints: 50
		}
	}) {
		let points = []
		let theta = (Math.PI * 2) / totalPoints
		let angle = theta
		for (let i = 0; i < totalPoints; i++) {
			angle = theta * i
			points.push({
				x: options.distanceBetweenPoints * Math.cos(angle),
				y: options.distanceBetweenPoints * Math.sin(angle)
			})
		}
		return points
	},

	generateEquidistantPointsInSpiral: function ({
		totalPoints = 10,
		options = {
			rotationsModifier: 1250, // Higher modifier: closer spiral lines
			distanceBetweenPoints: 32, // Distance between points in spiral
			radiusModifier: 50000, // Spiral radius
			lengthModifier: 1000 // Spiral length modifier
		}
	}) {
		let points = []
		// Higher modifier = closer spiral lines
		const rotations = totalPoints * options.rotationsModifier
		const distanceBetweenPoints = options.distanceBetweenPoints
		const radius = totalPoints * options.radiusModifier
		// Value of theta corresponding to end of last coil
		const thetaMax = rotations * 2 * Math.PI
		// How far to step away from center for each side.
		const awayStep = radius / thetaMax
		for (
			let theta = distanceBetweenPoints / awayStep; points.length <= totalPoints + options.lengthModifier;

		) {
			points.push({
				x: Math.cos(theta) * (awayStep * theta),
				y: Math.sin(theta) * (awayStep * theta)
			})
			theta += distanceBetweenPoints / (awayStep * theta)
		}
		return points.slice(0, totalPoints)
	},

	generateLeavesCoordinates: function ({
		nbOfLeaves,
		circleToSpiralSwitchover = 5,
		options,
	}) {
		let points = []
		// Position cluster's leaves in circle if below threshold, spiral otherwise
		if (nbOfLeaves < circleToSpiralSwitchover) {
			points = this.generateEquidistantPointsInCircle({
				totalPoints: nbOfLeaves,
				options,
			})
		} else {
			points = this.generateEquidistantPointsInSpiral({
				totalPoints: nbOfLeaves,
				options,
			})
		}
		return points
	},
}

export default MapService