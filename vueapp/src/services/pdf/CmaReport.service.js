import filters from '../../filters/filters'
import { resolve, chunkArray } from '../../utils'

const fieldsColumnWidth = 13
const columnsCount = 5

const CmaReportService = {

	async genContent({
			comps,
			fields,
			property,
			results,
			comments,
			proposedAssessment,
			proposedMarketValue,
			mapImg,
			cellClass,
			header,
		}) {
		const subject = comps.splice(0, 1)
		const groups = chunkArray(comps, 4)
		const tables = await Promise.all(groups.map(async (comps, index) => {
			const pageBreak = index < groups.length - 1
			return await this.genCMATable([ ...subject, ...comps ], fields, pageBreak, cellClass)
		}))
		return [
			...(
				property?.state !== 'FL'
				? [ this.genHeader(header) ]
				: []
			),
			this.genSubheader(property),
			...tables,
			{
				columns: [
					this.genResultsTable({
						results,
						proposedAssessment,
						proposedMarketValue,
						property,
					}),
					this.genCommentsTable(comments)
				],
				columnGap: 10,
			},
			{
				text: `${property?.state === 'FL' ? 'Folio' : 'APN'}: ${property?.apn}, Address: ${property.address}`,
				pageBreak: 'before',
			},
			{
				image: mapImg || '',
				width: 760,
				alignment: 'center',
			},
		]
	},

	/**
	 * Generate header of pdf
	 * @param {Strint} header 
	 */
	genHeader(header = '') {
		return {
			text: header,
			preserveLeadingSpaces: true,
			style: [ 'cmaTableTitle' ],
		}
	},

	/**
	 * Generate subheader of pdf
	 * @param {Object} property property model
	 */
	genSubheader(property = {}) {
		const isFL = property?.state === 'FL'
		const {
			property_county,
			town,
			village,
		} = property

		const settlement = village ? `VILLAGE OF ${village}` : `TOWN OF ${town}`

		let text = `${property_county?.name} County CMA Report For: ${property?.section}/${property?.block}/${property?.lot}`.toUpperCase()
		if (isFL) {
			text = `${property_county?.name} County CMA Report For: ${property?.apn}`.toUpperCase()
		}
		if (property_county?.id === 'nassau') {
			text = `${property_county?.name} County CMA Report For: ${property?.section}/${property?.block}/${property?.lot} Located in ${settlement}`
		}
		return {
			columns: [
				{
					text: isFL ? 'Redux Property Tax Services LLC' : '',
					width: '30%',
				},
				{
					text,
					style: [ 'tableTitle' ],
					width: '40%',
				},
				{
					text: isFL ? property?.address : '',
					width: '30%',
					alignment: 'right',
				},
			],
		}
	},

	/**
	 * Generate CMA table
	 * @param {Array} comps array of comps models
	 * @param {Array} fields array of rows
	 */
	async genCMATable(comps = [], fields = [], pageBreak, cellClass) {
		const rows = await Promise.all(fields.map(async field => await this.genCMARow(comps, field, cellClass)))
		const columnWidth = (100 - fieldsColumnWidth)/columnsCount
		return {
			table: {
				headerRows: 1,
				widths: [
					`${fieldsColumnWidth}%`,
					...Array(comps.length).fill(`${columnWidth/2}%`),
					...Array(comps.length).fill(`${columnWidth/2}%`),
				],
				hLineWidths: fields.map(field => field.hLineWidth),
				hLineColors: fields.map(field => field.hLineColor),
				body: rows,
			},
			layout: {
							hLineWidth: (i, node) => {
								return (i === 0 || i === node.table.body.length)
									? 1.5
									: (
										node.table.hLineWidths[i-1] ?? 0.5
									)
							},
							vLineWidth: (i, node) => {
								return (i === 0 || i === node.table.body.length)
									? 1.5
									: 1
							},
							hLineColor: (i, node) => {
								return (i === 0 || i === node.table.body.length)
									? 'black'
									: (
										node.table.hLineColors[i-1] ?? 'gray'
									)
							},
							paddingTop: () => 0,
							paddingBottom: () => 0,
			},
			style: [ 'cmaTableText' ],
			margin: [ 0, 0, 0, 10 ],
			pageBreak: pageBreak ? 'after' : '',
		}
	},

	/**
	 * Generate CMA table row
	 * @param {Array} comps array of comps models
	 * @param {Array} field array of rows
	 */
	async genCMARow(comps, field, cellClass) {

		let fieldCell = {
			text: field.text,
			margin: [0, 0, 0, 0],
			maxHeight: 15,
			bold: true,
		}

		if (field.renderField) {
			fieldCell = field.renderField(field.text)
		}

		const cells = await Promise.all(comps.map(async (comp, index) => {
			async function renderCell(field) {
				const text = resolve(field.value, comp) ?? null
				let cell = {
					text,
					margin: [0, 0, 0, 0],
					alignment: field?.alignment,
					fillColor: cellClass(comp, field.value),
					maxHeight: 15,
					colSpan: field?.colSpan || 0,
				}

				if (field.render) {
					cell = await field.render(text, comp, field, index)
				}

				return cell
			}

			if (field.cells) {
				return await Promise.all(field.cells.map(renderCell))
			} else {
				const cell = await renderCell(field)
				return [ cell, cell ]
			}
		}))

		return [
			fieldCell,
			...cells.flat(),
		]
	},

	/**
	 * Generate results table
	 * @param {Object} results assessment results
	 * @param {Number} proposedAssessment
	 * @param {Number} proposedMarketValue
	 */
	genResultsTable({
		results = {},
		proposedAssessment = 0,
		proposedMarketValue = 0,
		property = {},
	}) {
		return {
			width: 'auto',
			...(
				property?.state === 'FL'
				? {
					table: {
						body: [
							[
								{
									text: '2020 Just/Market Value',
									bold: true,
									fillColor: '#ccc',
								},
								filters.currency(results?.current_market_value),
							],
							[
								{
									text: 'Proposed Value',
									bold: true,
									fillColor: '#ccc',
								},
								{
									text: filters.currency(proposedMarketValue),
									bold: true,
								},
							],
							[
								{
									text: 'Difference',
									fillColor: '#ccc',
									bold: true,
								},
								filters.currency(results?.current_market_value - proposedMarketValue),
							],
						],
						heights: [ 16, 16, 17 ],
					},
				} : {
					table: {
						body: [
							[
								'',
								'ASSESSMENT',
								'MARKET VALUE',
								// '%',
								// 'MAX BY LAW'
							],
							[
								'CURRENT',
								filters.bignum(results?.decidedCurrentAssessmentValue),
								filters.currency(results?.current_market_value),
								// '',
								// '',
							],
							[
								'REQUESTED',
								{
									text: filters.bignum(proposedAssessment),
									bold: true,
								},
								{
									text: filters.currency(proposedMarketValue),
									bold: true,
								},
								// filters.percents(Number(((results.current_assessment_value - proposedAssessment) / results?.current_assessment_value * 100).toFixed(2))),
								// '25%',
							],
							// [
							// 	'DIFFERENCE',
							// 	filters.bignum(results?.current_assessment_value - proposedAssessment),
							// 	filters.currency(results?.current_market_value - proposedMarketValue),
							// 	'',
							// 	results?.current_assessment_value && (results?.current_assessment_value * 0.25).toFixed(0),
							// ],
							[
								'MAX BY LAW (25%)',
								filters.bignum(Number(results?.current_assessment_value * 0.75).toFixed(0)),
								filters.currency((results?.current_assessment_value * 0.75) / results.assessment_ratio),
							],
						],
					},
				}
			),
			layout: {
				hLineWidth: function (i, node) {
					return (i === 0 || i === node.table.body.length)
						? 1.5
						: 0.5
				},
				vLineWidth: function (i, node) {
					return (i === 0 || i === node.table.widths.length)
						? 1.5
						: 0.5
				},
				hLineColor: function (i, node) {
					return (i === 0 || i === node.table.body.length)
						? 'black'
						: 'gray'
				},
				vLineColor: function (i, node) {
					return (i === 0 || i === node.table.widths.length)
						? 'black'
						: 'gray'
				},
			},
			style: [ 'cmaTableText' ],
		}
	},

	/**
	 * Generate comments table
	 * @param {Array} comments array of comments to show
	 */
	genCommentsTable(comments = []) {
		return  {
			table: {
				widths: ['*'],
				heights: [
					...Array(comments.length).fill(60 / comments.length),
				],
				body: [
					...comments.map(comment => ([ comment || ' ']))
				],
			},
			layout: {
				hLineWidth: () => 0.5,
				vLineWidth: () => 0.5,
				hLineColor: () => 'gray',
				vLineColor: () => 'gray',
			},
			style: [ 'printFieldText' ],
			color: 'red',
		}
	},

}

export default CmaReportService