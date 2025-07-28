const path = require('path')

module.exports = {
	"lintOnSave": false,
	"transpileDependencies": [
		"vuetify"
	],
	"publicPath": process.env.NODE_ENV === 'production' ?
		'/vue/' :
		'/vue/',
	assetsDir: process.env.NODE_ENV === 'production' ?
		'../../static' :
		'',
    // publicPath: '',
	outputDir: process.env.NODE_ENV === 'production' ?
		path.resolve(__dirname, '../appflask/app/static/vue') :
		'dist',
	indexPath: process.env.NODE_ENV === 'production' ?
		'../../templates/vue/index.html':
		'index.html',
    // runtimeCompiler: undefined,
    // productionSourceMap: undefined,
    // parallel: undefined,
	// css: undefined,
	devServer: {
		proxy: {
			'^/api/': {
				target: 'http://localhost:5000/',
				ws: true,
				changeOrigin: true,
			},
			'^/_uploads/': {
				target: 'http://localhost:5000/',
				ws: true,
				changeOrigin: true,
			},
		},
	},
}