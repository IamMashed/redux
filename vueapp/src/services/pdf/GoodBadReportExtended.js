import pdfMake from 'pdfmake/build/pdfmake'
import pdfFonts from 'pdfmake/build/vfs_fonts'
import filters from '../../filters/filters'

import { resolve } from '../../utils'

pdfMake.vfs = pdfFonts.pdfMake.vfs

const defaultHeaders = [
	{
		text: 'TYPE',
		value: 'r_type',
	},
	{
		text: 'PROXIMITY',
		value: 'proximity_formatted',
	},
	{
		text: 'SELLER',
		value: 'seller_full_name',
	},
	{
		text: 'BUYER',
		value: 'buyer_full_name',
	},
	{
		// TODO: Add value
		text: 'A',
		value: '',
	},
	{
		text: 'PRICE',
		value: 'last_sale_price_formatted',
	},
	{
		text: 'DATE',
		value: 'last_sale_date_formatted',
	},
	{
		text: 'BAD',
		value: 'status',
		format: (val) => {
			return val === 'bad' ? 'x' : ''
		},
	},
	{
		text: 'ADJ/V',
		value: 'adjusted_market_value_formatted',
	},
	{
		text: 'NUM',
		value: 'number',
	},
	{
		text: 'ST_NAME',
		value: 'street',
	},
	{
		text: 'STYLE',
		value: 'style',
	},
	{
		text: 'K',
		value: 'kitchens',
	},
	{
		text: 'GLA',
		value: 'gla_sqft_formatted',
	},
	{
		text: 'ACRES',
		value: 'lot_size',
	},
	{
		text: 'BTH',
		value: 'baths',
	},
	{
		text: 'BSMT',
		value: 'basement_type',
	},
	{
		text: 'GARAGES',
		value: 'garages',
	},
	{
		text: 'BUILT',
		value: 'age',
	},
	{
		text: 'CLASS',
		value: 'class',
	},
	{
		text: 'AV_TOTAL',
		value: 'comp_assessment_value_formatted',
	},
	{
		text: 'HAMLET',
		value: 'hamlet',
	},
	{
		text: 'DIS',
		value: 'district',
	},
	{
		text: 'SEC',
		value: 'section',
	},
	{
		text: 'BLK',
		value: 'block',
	},
	{
		text: 'LOT',
		value: 'lot',
	},
]

class GoodBadReportExtended {

	constructor({
		headers = defaultHeaders,
		items = [],
		nearbyItems = [],
		assessmentResults = {},
		averageRanges = {},
		styles = {},
		defaultStyle = {
			fontSize: 8,
			lineHeight: 1.5,
		},
		fileName = 'Untitled.pdf',
		pageSize = 'LEGAL',
		pageMargins = [10, 40, 10, 10],
		pageOrientation = 'landscape',
	}) {
		this.headers = headers
		// Limit items to 120 max
		this.items = items.slice(0, 120)
		this.nearbyItems = nearbyItems,
		this.assessmentResults = assessmentResults,
		this.averageRanges = averageRanges,
		this.styles = styles
		this.defaultStyle = defaultStyle
		this.fileName = fileName
		this.pageSize = pageSize
		this.pageMargins = pageMargins
		this.pageOrientation = pageOrientation
	}

	get subject() {
		return this.items?.[0]
	}

	get badItems() {
		return this.items.filter(item => item.status === 'bad')
	}

	generateContent() {
		return [
			this.constructor.composePdfTable(this.headers, this.items),
			this.generateSubheader(),
			this.constructor.composePdfTable(this.headers, this.nearbyItems),
		]
	}

	create() {
		const header = this.generateHeader()
		const content = this.generateContent()
		return pdfMake.createPdf({
			info: {
				title: this.fileName,
			},
			header,
			content,
			styles: this.styles,
			defaultStyle: this.defaultStyle,
			pageSize: this.pageSize,
			pageMargins: this.pageMargins,
			pageOrientation: this.pageOrientation,
		})
	}

	print() {
		this.create()
			.open()
	}

	generateHeader() {
		const date = new Date()
		const dateFormatted = filters.longDate(date.toISOString())

		return {
			columns: [
				{
					width: '25%',
					stack: [
						dateFormatted,
						`TOTAL RECORDS = ${this.items.length}`,
					],
				},
				{
					width: '25%',
					text: `Subject ADJ/V = ${this.assessmentResults.current_market_value_formatted}`,
					style: [ 'cmaTableTitle' ],
				},
				{
					width: '35%',
					text: 'SUFFOLK COMPARABLES SPECIAL REPORT',
					style: [ 'title' ],
				},
				{
					width: '15%',
					columns: [
						{
							stack: [
								'DISTRICT',
								this.subject.district,
							],
						},
						{
							stack: [
								'SEC',
								this.subject.section,
							],
						},
						{
							stack: [
								'BLOCK',
								this.subject.block,
							],
						},
						{
							stack: [
								'LOT',
								this.subject.lot,
							],
						},
					],
				},
			],
			margin: 10,
		}
	}

	generateSubheader() {
		return {
			stack: [
				{
					columns: [
						{
							width: '45%',
							text: `TOTAL BAD COMPS = ${this.badItems.length}`,
						},
						{
							width: '35%',
							text: `Subject ADJ/V = ${this.assessmentResults.current_market_value_formatted}`,
							bold: true,
						},
					],
				},
				{
					columns: [
					{
						width: '12%',
						stack: [
							' ',
							`GOOD AVERAGE ADJ/V 1-4   =`,
							`GOOD AVERAGE ADJ/V 1-8   =`,
							`GOOD AVERAGE ADJ/V 1-12 =`,
						],
					},
					{
						width: '6%',
						stack: [
							'AVG ASS',
							filters.bignum(Number(this.averageRanges?.good?.['4']?.claimed_market_value?.toFixed(0))),
							filters.bignum(Number(this.averageRanges?.good?.['8']?.claimed_market_value?.toFixed(0))),
							filters.bignum(Number(this.averageRanges?.good?.['12']?.claimed_market_value?.toFixed(0))),
						],
					},
					{
						width: '10%',
						stack: [
							'AVG ADJ VAL',
							filters.bignum(Number(this.averageRanges?.good?.['4']?.proposed_assessment_value)),
							filters.bignum(Number(this.averageRanges?.good?.['8']?.proposed_assessment_value)),
							filters.bignum(Number(this.averageRanges?.good?.['12']?.proposed_assessment_value)),
						],
					},
					{
						width: '12%',
						stack: [
							' ',
							`ALL AVERAGE ADJ/V 1-4   =`,
							`ALL AVERAGE ADJ/V 1-8   =`,
							`ALL AVERAGE ADJ/V 1-12 =`,
						],
					},
					{
						width: '6%',
						stack: [
							'AVG ASS',
							filters.bignum(Number(this.averageRanges?.misc?.['4']?.claimed_market_value?.toFixed(0))),
							filters.bignum(Number(this.averageRanges?.misc?.['8']?.claimed_market_value?.toFixed(0))),
							filters.bignum(Number(this.averageRanges?.misc?.['12']?.claimed_market_value?.toFixed(0))),
						],
					},
					{
						width: '10%',
						stack: [
							'AVG ADJ VAL',
							filters.bignum(Number(this.averageRanges?.misc?.['4']?.proposed_assessment_value)),
							filters.bignum(Number(this.averageRanges?.misc?.['8']?.proposed_assessment_value)),
							filters.bignum(Number(this.averageRanges?.misc?.['12']?.proposed_assessment_value)),
						],
					},
					],
					bold: true,
				},
			],
			margin: [0, 20, 0, 0],
		}
	}

	/**
	 * Compose pdf table for pdfmaker
	 * @param {Array} headers headers { text, value }
	 * @param {Array} items property models array
	 */
	static composePdfTable(headers, items) {
		return {
			table: {
				headerRows: 1,
				widths: Array(headers.length).fill(`%`),

				body: [
					// Compose Headers row
					headers.map(header => ({
						text: header.text,
						fillColor: '#ffffc0',
						margin: 0,
						maxHeight: 15,
					})),

					// Compose Body rows
					...items.map(item => {
						return headers.map(header => {
							if (item) {
								let text = resolve(header.value, item) || null
								if (header.format) {
									text = header.format(text, item)
								}

								let cell = {
									text,
									margin: 0,
									maxHeight: 15,
								}

								if (header.render) {
									cell = header.render(text, item, header)
								}

								return cell
							}
							return null
						})
					}),
				],
			},
			layout: {
				hLineWidth: () => 0.5,
				vLineWidth: () => 0.5,
				hLineColor: () => 'gray',
				vLineColor: () => 'gray',
				paddingLeft: () => 0,
				paddingRight: () => 0,
				paddingTop: () => 0,
				paddingBottom: () => 0,
			},
			style: ['tableText'],
		}
	}
}

export default GoodBadReportExtended