import authApi from './authApi'
import constantsApi from './constantsApi'
import infoApi from './infoApi'
import countiesApi from './countiesApi'
import townsApi from './townsApi'
import villagesApi from './villagesApi'
import ratiossetsApi from './ratiossetsApi'
import ratiosApi from './ratiosApi'
import timeAdjustmentsApi from './timeAdjustmentsApi'
import assessmentDatesApi from './assessmentDatesApi'
import assessmentsApi from './assessmentsApi'
import propertiesApi from './propertiesApi'
import propertiesPhotosApi from './propertiesPhotosApi'
import ruleSetsApi from './ruleSetsApi'
import selectionRulesApi from './selectionRulesApi'
import inventoryRulesApi from './inventoryRulesApi'
import obsolescencesRulesApi from './obsolescencesRulesApi'
import singleCmaApi from './singleCmaApi'
import adjustmentsApi from './adjustmentsApi'
import globalSettingsApi from './globalSettingsApi'
import applicationsApi from './applicationsApi'
import tagsApi from './tagsApi'
import usersApi from './usersApi'
import rolesApi from './rolesApi'
import applicationTypesApi from './applicationTypesApi'
import applicationSourcesApi from './applicationSourcesApi'
import marketingCodesApi from './marketingCodesApi'
import applicationNotesApi from './applicationNotesApi'
import applicationHistoryApi from './applicationHistoryApi'
import takeoversApi from './takeoversApi'
import rejectReasonsApi from './rejectReasonsApi'
import lookupApi from './lookupApi'
import clientsApi from './clientsApi'
import clientTypesApi from './clientTypesApi'
import clientNotesApi from './clientNotesApi'
import casesApi from './casesApi'
import paymentTypesApi from './paymentTypesApi'
import paymentStatusesApi from './paymentStatusesApi'
import quickSearchApi from './quickSearchApi'
import notesApi from './notesApi'
import singleCmaWorkupsApi from './singleCmaWorkupsApi'
import datamappersApi from './datamappersApi'
import uploadApi from './uploadApi'

const apis = {
	'auth': authApi,
	'constants': constantsApi,
	'info': infoApi,
	'counties': countiesApi,
	'towns': townsApi,
	'villages': villagesApi,
	'ratiossets': ratiossetsApi,
	'ratios': ratiosApi,
	'time-adjustments': timeAdjustmentsApi,
	'assessment-dates': assessmentDatesApi,
	'assessments': assessmentsApi,
	'properties': propertiesApi,
	'properties-photos': propertiesPhotosApi,
	'rule-sets': ruleSetsApi,
	'selection-rules': selectionRulesApi,
	'inventory-rules': inventoryRulesApi,
	'obsolescences-rules': obsolescencesRulesApi,
	'single-cma': singleCmaApi,
	'adjustments': adjustmentsApi,
	'global-settings': globalSettingsApi,
	'applications': applicationsApi,
	'tags': tagsApi,
	'users': usersApi,
	'roles': rolesApi,
	'application-types': applicationTypesApi,
	'application-sources': applicationSourcesApi,
	'takeovers': takeoversApi,
	'marketing-codes': marketingCodesApi,
	'application-notes': applicationNotesApi,
	'application-history': applicationHistoryApi,
	'reject-reasons': rejectReasonsApi,
	'lookup': lookupApi,
	'clients': clientsApi,
	'client-types': clientTypesApi,
	'client-notes': clientNotesApi,
	'cases': casesApi,
	'payment-types': paymentTypesApi,
	'payment-statuses': paymentStatusesApi,
	'quick-search': quickSearchApi,
	'notes': notesApi,
	'single-cma-workups': singleCmaWorkupsApi,
	'datamappers': datamappersApi,
	'upload': uploadApi,
}

export const apiFactory = {
	get: name => apis[name],
}