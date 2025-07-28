import { resolve } from '../../utils'

const GoodBadReportService = {

	/**
	 * Compose pdf table for pdfmaker
	 * @param {Array} headers headers { text, value }
	 * @param {Array} items property models array
	 */
	composePdfTable(headers, items) {
		return {
			table: {
				headerRows: 1,
				widths: Array(headers.length).fill(`%`),

				body: [
					// Headers
					headers.map(header => ({
						text: header.text,
						margin: [0, 0, 0, 0],
						maxHeight: 15,
					})),

					// Body rows
					...items.map(item => {
						return headers.map(header => {
							if (item) {
								let text = resolve(header.value, item) || null
								if (header.format) {
									text = header.format(text, item)
								}

								let cell = {
									text,
									margin: [0, 0, 0, 0],
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
	},
}

export default GoodBadReportService