<template>
	<v-card
		height="100%"
		outlined>
		<v-card-title>
			List of Cases ({{ items.length }})
		</v-card-title>
		<v-divider></v-divider>

		<v-list
			max-height="60vh"
			class="py-0 overflow-scroll">
			<v-list-item-group>
				<template v-for="(item, key) in items">
					<case-list-item
						:value="item"
						:key="key">
					</case-list-item>
					<v-divider v-if="key !== items.length - 1" :key="`${key}-divider`"></v-divider>
				</template>
			</v-list-item-group>
		</v-list>
	</v-card>
</template>

<script>
import CaseListItem from './CaseListItem'

export default {
	components: {
		CaseListItem,
	},
	props: {
		items: {
			type: Array,
			required: true,
		},
	},
}
</script>