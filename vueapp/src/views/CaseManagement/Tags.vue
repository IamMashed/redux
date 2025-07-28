<template>
	<v-container>
		<h1 class="title">Tags</h1>

		<v-sheet
			class="mt-4">
			<v-data-table
				:items="tags"
				:headers="headers">

				<template #top
					v-if="isAdmin">
					<v-btn
						color="success"
						depressed
						@click="prependTag">
						Add tag
					</v-btn>
				</template>

				<template #item.name="{ item }">
					<v-edit-dialog
						v-if="isAdmin"
						:ref="`dialog-${tags.indexOf(item)}`"
						:return-value.sync="item.name"
						persistent
						large
						@save="saveTag(item)">
						<v-chip
							:color="`${colorHash(item.name)} lighten-2`"
							dark>
							{{ item.name }}
						</v-chip>
						<template #input>
							<v-text-field
								v-model="item.name"
								label="Name"
								single-line
								autofocus>
							</v-text-field>
						</template>
					</v-edit-dialog>

					<v-chip
						v-else
						:color="`${colorHash(item.name)} lighten-2`"
						dark>
						{{ item.name }}
					</v-chip>
				</template>

				<template #item.actions="{ item }">
					<v-btn
						text
						icon
						@click="deleteTag(item)">
						<v-icon small>mdi-delete</v-icon>
					</v-btn>
				</template>

			</v-data-table>
		</v-sheet>
	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import colorHash from '../../mixins/colorHash'

export default {
	mixins: [
		colorHash,
	],
	data: () => ({
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
		]),
		...mapGetters('tags', [
			'tags',
		]),
		headers() {
			return [
				{
					text: 'Name',
					value: 'name',
				},
				...(
					this.isAdmin ? [{
						text: 'Actions',
						value: 'actions',
						sortable: false,
					}] : []
				),
			]
		}
	},
	methods: {
		...mapActions('tags', [
			'loadTags',
			'addTag',
			'createTag',
			'updateTag',
			'deleteTag',
		]),
		prependTag() {
			this.addTag()
			this.$nextTick(() => this.$refs['dialog-0'].isActive = true)
		},
		saveTag(tag) {
			if(tag.id) {
				this.updateTag(tag)
			} else {
				this.createTag(tag)
			}
		},
	},
	mounted() {
		this.loadTags()
	},
}
</script>