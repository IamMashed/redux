/**
 * Mixin for generating color using hash table
 */
export default {
	methods: {
		/**
		 * Generate color based on string using hash table
		 * @param {String} value string to use for color hashing
		 * 
		 * @returns {String} color
		 */
		colorHash(value) {
			const colours = ['red', 'pink', 'purple', 'deep-purple', 'indigo', 'cyan', 'teal', 'green', 'light-green', 'lime', 'amber' ]

			let sum = 0
			for (var i = 0; i < value.length; i++){
				sum += value.charCodeAt(i)
			}
			const index =  sum % colours.length
			return colours[index]
		},
	},
}