import Vue from 'vue'
import filters from './filters'

Object.keys(filters).forEach(k => {
	Vue.filter(k, filters[ k ])
})