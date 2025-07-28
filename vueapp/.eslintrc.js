module.exports = {
	root: true,
	env: {
		node: true
	},
	'extends': [
		'plugin:vue/essential',
		'eslint:recommended',
	],
	rules: {
		'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
		'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
		'vue/html-closing-bracket-newline': ['warn', {
			'singleline': 'never',
			'multiline': 'never',
		}],
		'vue/html-indent': ['warn', 'tab'],
		'indent': ['warn', 'tab'],
		'comma-spacing': ['warn', { 'before': false, 'after': true }],
	  	'comma-dangle': ['warn', 'always-multiline'],
		'no-trailing-spaces': ['warn', { 'skipBlankLines': true }],
		'semi': ['warn', 'never'],
		'quotes': [2, 'single', { 'avoidEscape': true }],
		'complexity': ['warn', 5],
		'eqeqeq': ['warn', 'always'],
		'no-magic-numbers': ['warn', {
			'ignoreArrayIndexes': true,
			'ignore': [1],
		}],
		'no-multi-spaces': 'warn',
		'no-useless-catch': 'warn',
		'no-return-await': 'warn',
		'require-await': 'warn',
		'init-declarations': ['warn', 'always'],
		'no-use-before-define': 'warn',
		'comma-spacing': ['warn', { 'before': false, 'after': true }],
		'comma-dangle': ['warn', 'always-multiline'],
		'block-spacing': 'warn',
		'no-whitespace-before-property': 'warn',
		'no-trailing-spaces': ['warn', { 'skipBlankLines': true }],
		'no-nested-ternary': 'warn',
		'no-multiple-empty-lines': 'warn',
		'max-statements': 'warn',
		'max-params': 'warn',
		'max-nested-callbacks': ['warn', 3],
		'max-depth': 'warn',
		'keyword-spacing': ['warn', {
			'before': true,
			'after': true,
		}],
		'implicit-arrow-linebreak': ['warn', 'beside'],
		'func-style': ['warn', 'declaration', {
			'allowArrowFunctions': true,
		}],
		'func-call-spacing': ['warn', 'never'],
		'no-duplicate-imports': 'warn',
		'no-var': 'warn',
		'template-curly-spacing': 'warn',
		'prefer-template': 'warn',
		'prefer-destructuring': 'warn',
		'rest-spread-spacing': ['warn', 'never'],
	},
	overrides: [
		{
			files: [
				'**/__tests__/*.{j,t}s?(x)',
				'**/tests/unit/**/*.spec.{j,t}s?(x)'
			],
			env: {}
		},
		{
			files: [
				'**/__tests__/*.{j,t}s?(x)',
				'**/tests/unit/**/*.spec.{j,t}s?(x)'
			],
			env: {
				jest: true
			}
		}
	],
	parserOptions: {
		parser: 'babel-eslint'
	}
}