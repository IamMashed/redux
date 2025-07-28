import { parseISO, format } from 'date-fns'

export default {

	booleanFilter: (v) => {
		return v ? 'YES' : 'NO'
	},

	percents: (value) => {
		return Number.isFinite(value) ? `${value}%` : value
	},

	currency: (value) => {
		return Number.isFinite(value) ? Number(value).toLocaleString('en-US', {
					style: 'currency',
					currency: 'USD',
				}).slice(0, -3)
				: value
	},

	miles: (value) => {
		return Number.isFinite(value) ? `${Number(value).toFixed(2)} Miles`
		: value
	},

	sqft: (value) => {
		return Number.isFinite(value) ? `${Number(value).toLocaleString('en-US')} sqft`
		: value
	},

	acres: (value) => {
		return Number.isFinite(value) ? `${Number(value).toLocaleString('en-US')} acres`
		: value
	},

	bignum: (value) => {
		return Number.isFinite(value) || Number(value) ? `${Number(value).toLocaleString('en-US')}`
		: value
	},

	date: (value) => {
		return value ? format(parseISO(value), 'M/dd/yyyy')
		: value
	},

	longDate: (value) => {
		return value ? format(parseISO(value), 'EEEE, LLLL d, yyyy')
		: value
	},

	datetime: (value) => {
		return value ? format(parseISO(value), `MMM dd, yyyy 'at' h:mm a`)
		: value
	},

	/**
	 * Get short year format
	 * @param {String} value
	 */
	shortYear: (value) => {
		return value ? String(value).substring(2, 4)
		: value
	},

	listToString: (value) => {
		return value && Array.isArray(value) ? value.join(', ')
		: value
	},

	/**
	 * Filter to remove last digit from property class in Nassau county
	 * @param {Number} value 2100
	 * @param {String} propClass property class: nassau, suffolk
	 */
	classFilter: (value, propClass) => {
		return propClass === 'nassau' ? Math.floor(value / 10) : value
	},

	/**
	 * Get initials from full name
	 * @param {String} value
	 */
	initials: (value) => {
		return value ? String(value).split(' ').map((n)=>n[0]).join('')
		: value
	},

	/**
	 * Format Phone number to (123) 456-7890
	 * @param {String} value
	 */
	phone: (value) => {
		return value ? value.replace(/[^0-9]/g, '')
							.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3')
		: value
	},

	/**
	 * 
	 * @param {*} value value
	 * @param {Object} mapper key:value paired mapper from backend constants
	 * @param {*} callback callback function
	 */
	mapperFilter: function(value, mapper, callback = (v) => v) {
		return mapper
			? callback(mapper[value])
			: value != null
				? value
				: '-'
	},

	/**
	 * Return line with joined owners
	 * @param {Array} owners Array of Owner's models
	 * @returns {String}
	 */
	owners: (owners) => {
		let list = []
		owners.forEach(item => {
			list.push(item.first_full_name)
			list.push(item.second_full_name)
		})
		list = list.filter(Boolean)
		return list.join(', ')
	},

	/**
	 * Return line with joined last owners
	 * @param {Array} owners Array of Owner's models
	 * @returns {String}
	 */
	lastOwners: (owners) => {
		if (owners) {
			const item = owners[0] || {}
			let list = []
			list.push(item.first_full_name)
			list.push(item.second_full_name)
			list = list.filter(Boolean)
			return list.join(', ')
		}
		return ''
	},

}