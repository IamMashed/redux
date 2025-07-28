<template>
	<v-list-item
		:to="route">
		<v-list-item-icon>
			<v-icon>
				{{ icon }}
			</v-icon>
		</v-list-item-icon>
		<v-list-item-title>
			{{ item.name }}
		</v-list-item-title>
	</v-list-item>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
	props: {
		item: {
			type: Object,
			required: true,
		},
	},
	computed: {
		...mapGetters('search', [
			'entities',
		]),
		entity() {
			return this.entities.find(item => item.name === this.item.entity)
		},
		icon() {
			return this.entity?.icon || ''
		},
		route() {
			const { id } = this.item
			const name = this.entity?.route || ''
			const params = this.entity?.params && this.entity?.params(this.item)
			return {
				name,
				params: {
					id,
					...params,
				},
			}
		},
	},
}
</script>