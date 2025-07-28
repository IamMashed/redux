import filters from '../filters/filters'

class AssessmentResult {
	constructor(obj) {
		this.assessment_ratio 			= obj.assessment_ratio
		this.current_market_value 		= obj.current_market_value
		this.claimed_market_value 		= obj.claimed_market_value

		this.current_assessment_value 	= obj.current_assessment_value
		this.override_assessment_value 	= obj.override_assessment_value
		this.proposed_assessment_value 	= obj.proposed_assessment_value
		this.tax_value 					= obj.tax_value
	}

	get decidedCurrentAssessmentValue() {
		return this.override_assessment_value || this.current_assessment_value
	}

	get current_market_value_formatted() {
		return filters.currency(this.current_market_value)
	}
}

export default AssessmentResult
