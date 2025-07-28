<template>
	<canvas ref="chart"></canvas>
</template>

<script>
import Chart from 'chart.js'

export default {
	props: {
		config: {
			type: Object,
			required: true,
		},
	},
	data: () => ({
		chart: null,
	}),
	methods: {
		init() {
			this.chart = new Chart(this.$refs.chart.getContext('2d'), this.config)
		},
		update() {
			this.chart.destroy()
			this.init()
		}
	},
	mounted() {
		this.init()
	},
	watch: {
		config: {
			deep: true,
			handler: 'update',
		},
	},
}
</script>