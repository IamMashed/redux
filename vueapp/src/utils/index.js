/**
 * Group array of objects by key
 * @param {Array} arr array of objects
 * @param {String} key key to group by
 */
function groupBy(arr, key) {
	return arr.reduce((rv, x) => {
		(rv[x[key]] = rv[x[key]] || []).push(x)
		return rv
	}, {})
}

/**
 * Key array of object by key
 * @param {Array} arr array of objects
 * @param {String} key key to key by
 */
function keyBy(arr, key) {
	return arr.reduce((obj, item) => {
		obj[item[key]] = item
		return obj
	}, {})
}

/**
 * Calculate percent
 * @param {Number} num
 * @param {Number} percent
 */
function getPercents(num, percent) {
	const c = (parseFloat(num) * parseFloat(percent)) / 100;
	return parseFloat(c);
}

/**
 * Remove empty and nullable values from object
 * @param {Object} obj 
 */
function removeEmpty(obj) {
	const o = {}
	Object.entries(obj).forEach(([key, val])  => {
		if(val === '' || val === null) {
			return 
		} else {
			o[key] = val
		}
	})
	return o
}

/**
 * Make null all empty values from object
 * @param {Object} obj 
 */
function makeNull(obj) {
	const o = {}
	Object.entries(obj).forEach(([key, val])  => {
		if(val === '') {
			return o[key] = null
		} else {
			o[key] = val
		}
	})
	return o
}

/**
 * Resolve value of Object property by string path
 * @param {String} path 
 * @param {Object} obj 
 * @param {String} separator 
 */
function resolve(path, obj = this, separator = '.') {
	var properties = Array.isArray(path) ? path : path.split(separator)
    return properties.reduce((prev, curr) => prev && prev[curr], obj)
}

/**
 * Map function for object
 * @param {Object} obj 
 * @param {*} fn 
 */
function objectMap(obj, fn) {
	return Object.fromEntries(
		Object.entries(obj).map(
			([k, v], i) => [k, fn(v, k, i)]
		)
	)
}

/**
 * Split array into chunks
 * @param {Array} arr subject array
 * @param {Number} size number of element in each chunk
 */
function chunkArray(arr, size) {
	return Array.from({ length: Math.ceil(arr.length / size) }, (v, i) =>
		arr.slice(i * size, i * size + size)
	)
}

/**
 * Find item by key
 * @param {Array} arr subject array
 * @param {Function} findFunc function used to find
 */
function findByKey(arr = [], findFunc) {
	const item = arr.find(item => findFunc(item))
	return item ?? {}
}

export {
	groupBy,
	keyBy,
	getPercents,
	removeEmpty,
	makeNull,
	resolve,
	objectMap,
	chunkArray,
	findByKey,
}