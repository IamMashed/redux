<template>
	<v-menu
		offset-y>

		<template #activator="{ on, attrs }">
			<v-btn
				color="primary"
				class="mr-10"
				outlined
				v-bind="attrs"
				v-on="on">
				Actions
			</v-btn>
		</template>

		<v-list>
			<slot></slot>
		</v-list>

	</v-menu>
</template>