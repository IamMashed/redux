module.exports = {
	preset: '@vue/cli-plugin-unit-jest',
	testEnvironment: 'jest-environment-jsdom-sixteen',
	transformIgnorePatterns: ['/node_modules/(?!vuetify)'],
}
