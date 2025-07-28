# Register all the models in the app by importing them
from app.settings.models import AssessmentDate
from app.database.models.files import Files
from app.database.models.assessment import Assessment
from app.database.models.sale import Sale, SaleValidation
from app.database.models.owner import Owner, OwnerValidation
from app.database.models.user import User, Role, AnonymousUser
from app.rules.models import PropertiesRules, InventoryRules
from app.database.models.cma import CmaResult, CmaTask
from app.settings.models import RatiosSettings, Ratio
from app.database.models.property_photo import PropertyPhoto
from app.database.models.property import Property  # Property table should be imported after Sale, Assessment
from app.case_management.models import Client, CompanyServing, \
    Application, ApplicationType, CaseProperty

