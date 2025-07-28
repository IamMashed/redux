<template>
	<div>

		<v-data-table
			v-model="selected"
			:items="items"
			:headers="headers"
			single-select
			show-select
			item-key="index"
			@item-selected="setDefaultMonthsRange">

			<template #top
				v-if="isAdmin">
				<div class="d-flex justify-end my-4">
					
					<slot name="title"></slot>

					<v-spacer></v-spacer>

					<v-btn
						v-if="!editable"
						depressed
						color="secondary"
						class="mx-1"
						@click="edit">
						<v-icon left>mdi-pencil</v-icon>
						Edit
					</v-btn>

					<template v-else>
						<v-btn
							depressed
							color="error"
							class="mx-1"
							@click="cancel">
							<v-icon left>mdi-close</v-icon>
							Cancel
						</v-btn>

						<v-btn
							depressed
							color="success"
							class="mx-1"
							@click="save">
							<v-icon left>mdi-upload</v-icon>
							Save
						</v-btn>
					</template>
				</div>
			</template>

			<template #item.month="{ item }">
				{{ `${item.month}/${item.year}` }}
			</template>

			<template #item.value="{ item }">
				<v-text-field
					v-model.number="item.value"
					label="Edit"
					single-line
					hide-details
					placeholder="0"
					suffix="%"
					:disabled="!editable"
					@blur="queue.push(item), adjustToDate()">
				</v-text-field>
			</template>

			<template #item.adjustedToDate="{ item }">
				<div>{{ item.adjustedToDate | percents }}</div>
			</template>
			
		</v-data-table>

		<v-card>
			<v-row class="pa-4">
				<v-col
					cols="12"
					lg="3">
					<a-date
						v-model="startDate"
						label="Start date"
						type="month"
						:min="minDate"
						:max="maxDate">
					</a-date>
					<a-date
						v-model="endDate"
						label="End date"
						type="month"
						:min="minDate"
						:max="maxDate">
					</a-date>
				</v-col>
				<v-col
					cols="12"
					lg="9">
					<a-chart
						:config="chartConfig">
					</a-chart>
				</v-col>
			</v-row>
		</v-card>

		<confirm ref="confirm"></confirm>
		
	</div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../../api/apiFactory'
import { getPercents } from '../../utils'
import {
	eachMonthOfInterval,
	add,
	isAfter,
	isBefore,
	compareDesc,
	addMonths,
	subMonths,
	parseISO,
	format,
} from 'date-fns'
import Confirm from '../Confirm'
import AChart from '../AChart'
import ADate from '../ADate'

const timeAdjustmentsApi = apiFactory.get('time-adjustments')

export default {
	components: {
		Confirm,
		AChart,
		ADate,
	},
	props: {
		data: {
			type: Array,
			required: true,
		},
		parentId: {
			type: [ String, Number ],
			required: true,
		},
	},
	data: () => ({
		editable: false,
		items: [],
		itemsCopy: [],
		selected: [],
		queue: [],
		headers: [
			{
				text: 'Month',
				value: 'month',
			},
			{
				text: 'Monthly adjustment %',
				value: 'value',
			},
			{
				text: 'Cumulative Adjustment %',
				value: 'adjustedToDate'
			},
		],
		startDate: '',
		endDate: '',
		minDate: '2010-01',
		maxDate: format(
			add(new Date(), {
				months: 2,
			}),
			'yyyy-MM'
		),
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
		]),
		startingPoint() {
			if (this.selected[0])
				return this.items.findIndex(item => item === this.selected[0])
			else return 0
		},
		months() {
			return eachMonthOfInterval({
				start: new Date(2010, 0, 1), // FIXME: take from minDate
				end: addMonths(new Date(), 2), // FIXME: take + N months from data
			}).map(item => ({
				county: this.parentId,
				year: format(item, 'yyyy'),
				month: format(item, 'M'),
				value: 0,
				index: format(item, 'yyyy-MM'),
			}))
		},
		timeline() {
			return this.items.map(item => {
				// TODO: refactor interval check
				if(
					isAfter(parseISO(item.index), subMonths(parseISO(this.startDate), 1)) &&
					isBefore(parseISO(item.index), addMonths(parseISO(this.endDate), 1))
				) {
					return {
						x: item.index,
						y: this.selected[0] ? item.adjustedToDate : item.value,
					}
				} else {
					return false
				}
			}).filter(Boolean)
		},
		chartConfig() {
			return {
				type:    'line',
				data: {
					datasets: [
						{
							label: this.parentId,
							data: this.timeline,
							borderColor: '#1dbab4',
							fill: false,
						},
					]
				},
				options: {
					responsive: true,
					scales: {
						xAxes: [{
							type:       "time",
							time:       {
								format: 'YYYY/MM',
								tooltipFormat: 'll'
							},
							scaleLabel: {
								display:     true,
								labelString: 'Month'
							}
						}],
						yAxes: [{
							scaleLabel: {
								display:     true,
								labelString: this.selected[0] ? 'Adjusted to Date'  : 'Adjustment Delta'
							}
						}]
					},
				},
			}
		},
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		edit() {
			this.itemsCopy = JSON.parse(JSON.stringify(this.items))
			this.editable = true
		},
		cancel() {
			this.items = JSON.parse(JSON.stringify(this.itemsCopy))
			this.editable = false
			this.adjustToDate()
		},
		/**
		 * Populate months if not exists
		 */
		populateMonth(arr) {
			// Add items from months array to items if not exists
			this.months.map(item => {
				const matched = arr.find(i => i.month == item.month && i.year == item.year)
				if(!matched) {
					arr.push(item)
				} else {
					matched.index = `${matched.year}-${(`0${matched.month}`).slice(-2)}`
				}
			})
			// Sort populated array by date
			return arr.sort((a, b) => compareDesc(new Date(a.year, a.month), new Date(b.year, b.month)))
		},
		setDefaultMonthsRange() {
			this.$nextTick(() => {
				// TODO: add boolean computed isSelected or selected item
				if(this.selected[0]) {
					let dt = this.selected[0].index
					dt = parseISO(dt)
					// TODO: Get 18 and 36 from data
					this.endDate = format(addMonths(dt, 18), 'yyyy-MM')
					this.startDate = format(subMonths(dt, 18), 'yyyy-MM')
				} else {
					this.endDate = this.maxDate
					// TODO: Refactor to store date as Date type and computed property in ISO format
					const startDate = subMonths(parseISO(this.endDate), 36)
					this.startDate = format(startDate, 'yyyy-MM')
				}
			})
		},
		/**
		 * Adjust delta to date
		 */
		adjustToDate() {
			/**
			 * Use reducer for positive cumulative delta
			 */
			this.items.reduce((accumulator, currentValue, index) => {
				if (index === this.startingPoint) {
					const item = this.items[index]
					item.adjustedToDate = 0
					this.$set(this.items, index, item)
				} else if (index > this.startingPoint) {
					const n =
						-1 *
							getPercents(
								accumulator,
								currentValue.value
							) +
						accumulator

					const p = (n - 1) * 100
					const item = this.items[index]
					item.adjustedToDate = Number(p.toFixed(2))
					this.$set(this.items, index, item)
					return n
				}
				return 1
			}, 1)

			/**
			 * Use right reducer for negative cumulative delta
			 */
			this.items.reduceRight((accumulator, currentValue, index) => {
				if (index < this.startingPoint) {
					const n =
						getPercents(
							accumulator,
							currentValue.value
						) + accumulator

					const p = (n - 1) * 100
					const item = this.items[index]
					item.adjustedToDate = Number(p.toFixed(2))
					this.$set(this.items, index, item)
					return n
				}
				return 1
			}, 1)
		},
		async save() {
			try {
				const confirm = await this.$refs.confirm.open('Submit Time adjustments', 'Are you sure you want to make changes to the Time Adjustments?', { color: 'success' })
				if(confirm) {
					await Promise.all(this.queue.map(async r => {
						return await this.saveItem(r)
					}))
					this.queue = []
					this.notify({
						text: 'Time Adjustments updated',
						color: 'success'
					}, { root: true })
				} else {
					this.cancel()
				}
				this.editable = false
				return this.adjustToDate()
			} catch (error) {
				this.notify({
					text: 'Error while Time Adjustments update',
					color: 'error'
				}, { root: true })
			}
		},
		async saveItem(item) {
			try {
				if(item.id) {
					await timeAdjustmentsApi.update(item)
				} else {
					const { data } = await timeAdjustmentsApi.create(item)
					const index = this.items.findIndex(i => i.index === item.index)
					this.$set(this.items, index, { ...item, id: data.id })
				}
			} catch (error) {
				this.notify({
					text: 'Can not update Time Adjustments',
					color: 'error'
				}, { root: true })
			}
		},
	},
	mounted() {
		this.items = JSON.parse(JSON.stringify(this.data))
		this.items = this.populateMonth(this.items)
		this.adjustToDate()
		this.setDefaultMonthsRange()
	},
	watch: {
		startingPoint() {
			this.adjustToDate()
		}
	},
}
</script>