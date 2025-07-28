<template>
	<div>
		<v-simple-table v-bind="$props"
			class="comparison-table">
			<template v-slot:default>
				<tbody>
					<slot
						v-for="(row, k) in rows"
						:name="`${row.value}.row`"
						:row="row">

						<tr :is="k === 0 ? `draggable` : `tr`"
							:key="k"
							:list="localItems"
							tag="tr"
							:move="handleMove"
							@end="dragged = true">
							<td class="text-uppercase"
								slot="header">
								<slot
									:name="`${row.value}.title`"
									:value="row.text">
									{{ row.text }}
								</slot>
							</td>
							<td v-for="(cell, i) in row.cells" :key="`${k}${i}`"
								class="comparison-table-cell"
								:class="[
									row.class,
									[k === 0 ? 'cursor-grab' : ''],
									itemClass(cell.item),
									cellClass(cell.item, row.value),
								]"
								@contextmenu.prevent="handleContextmenu(cell.item, row.value)">
								<slot
									:name="row.value"
									:item="cell.item"
									:index="i"
									:value="cell.value"
									:edit-item="editItem">
									{{ cell.value }}
								</slot>
							</td>
						</tr>
					</slot>
				</tbody>
			</template>
		</v-simple-table>

		<v-dialog v-model="dialog"
			max-width="500px"
			scrollable>

			<a-form
				@cancel="dialog = false"
				@submit="submit">

				<slot
					name="form"
					:editedItem="editedItem">

					<vue-form-json-schema
						v-if="schema && uiSchema"
						v-model="editedItem"
						:schema="schema"
						:ui-schema="uiSchema"
						class="layout wrap">
					</vue-form-json-schema>
				</slot>

				<template #actions="{ cancel, submit }">
					<slot name="form-actions"
						:cancel="cancel"
						:submit="submit"
						:editedItem="editedItem">
					</slot>
				</template>

			</a-form>
								
		</v-dialog>

		<confirm
			ref="confirm">
		</confirm>
	</div>
</template>

<script>
import { resolve } from '../utils'
import { clone } from 'lodash'
import VueFormJsonSchema from 'vue-form-json-schema'
import Draggable from 'vuedraggable'
import AForm from './AForm'
import Confirm from './Confirm'

export default {
	components: {
		VueFormJsonSchema,
		Draggable,
		AForm,
		Confirm,
	},
	props: {
		fields: {
			type: Array,
			required: true,
		},
		items: {
			type: Array,
			required: true,
		},
		schema: {
			type: Object,
		},
		uiSchema: {
			type: Array,
		},
		locked: {
			type: Boolean,
			default: false,
		},
		itemKey: {
			type: String,
			default: 'id',
		},
		lockedItems: {
			type: Array,
			default: () => ([]),
		},
		itemClass: {
			type: Function,
			default: () => ([]),
		},
		cellClass: {
			type: Function,
			default: () => ([]),
		},
	},
	data: () => ({
		localItems: [],
		editedItemIndex: -1,
		editedItem: null,
		dialog: false,
		dragged: false,
	}),
	computed: {
		rows() {
			return this.fields.map(field => {
				const row = {
					...field,
					cells: [],
				}

				this.localItems.forEach(item => {
					row.cells.push({
						value: resolve(field.value, item) || null,
						item: item,
					})
				})
				return row
			})
		},
	},
	methods: {
		addItem(item = {}) {
			this.editedItemIndex = -1
			this.editedItem = item
			this.$nextTick(() => this.dialog = true)
		},
		editItem(item) {
			this.editedItemIndex = this.items.indexOf(item)
			this.editedItem = clone(item)
			this.$nextTick(() => this.dialog = true)
		},
		async deleteItem(item) {
			const confirm = await this.$refs.confirm.open('Delete', 'Are you sure?', { color: 'red' })
			if(confirm) this.$emit('delete', item, this.items.indexOf(item))
		},
		submit() {
			this.editedItemIndex === -1
				? this.$emit('create', this.editedItem)
				: this.$emit('update', this.editedItem, this.editedItemIndex)

			this.closeDialog()
		},
		closeDialog() {
			this.dialog = false
		},
		/**
		 * Drag element only if dragged and 
		 * related context is NOT in locked items list
		 */
		handleMove(e) {
			return this.lockedItems.indexOf(e.draggedContext?.element?.[this.itemKey]) < 0 
				&& this.lockedItems.indexOf(e.relatedContext?.element?.[this.itemKey]) < 0
		},
		/**
		 * Emit context menu event
		 */
		handleContextmenu(item, field) {
			this.$emit('context', item, field)
		},
	},
	watch: {
		items: {
			deep: true,
			handler: function(newVal) {
				if(!this.locked) {
					if(this.dragged) {
						const ids = this.localItems.map(item => item.id)
						this.localItems = JSON.parse(JSON.stringify(newVal)).sort((a, b) => {
							var indexA = ids.indexOf(a['id'])
							var indexB = ids.indexOf(b['id'])
							if (indexA < 0) {
								return 1
							} else if (indexB < 0) {
								return -1
							} else if (indexA < indexB) {
								return -1
							} else if (indexA > indexB) {
								return 1
							} else {
								return 0       
							}
						})
					} else {
						this.localItems = newVal
					}
				}
			},
		},
	},
}
</script>

<style lang="scss">

#app.v-application .comparison-table {

	table {
		border-collapse: collapse;
	}

	tr {
		td {
			font-size: 12px;
			height: 28px;
		}

		td.comparison-table-cell {
			padding: 0 10px;
			border-left: 0.75em solid white;
			border-right: 0.75em solid white;
			border-color: white !important;
			background-color: var(--v-primary-lighten5);
			color: var(--v-primary-darken2);
			min-width: 200px;

			&.yellow {
				background-color: #ffeb3b !important;
			}

			.row {
				margin-top: unset;
				margin-bottom: unset;
				margin-right: -10px;
				margin-left: -10px;
			}

			.comparison-table-cell__content {
				height: 100%;
				margin-left: -10px;
				margin-right: -10px;
				padding: 0 8px;
			}
		}

		&:hover {
			.comparison-table-cell {
				background-color: var(--v-primary-lighten4);
			}
		}

		.col {
			padding: 0 8px;
		}
	}
}

/* Printing styles */
@media print {

	.v-application .comparison-table {

		tr {

			td,
			td.comparison-table-cell {
				height: 20px;
				border: 1px solid #000 !important;

				.yellow {
					background-color: yellow !important;
					color-adjust: exact;
				}
			}
		}

		.v-divider {
			border-color: #000;
		}
	}
}

</style>