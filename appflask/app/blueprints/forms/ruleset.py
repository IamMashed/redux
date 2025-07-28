from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, BooleanField, SelectField, HiddenField, \
    SelectMultipleField, DateField
from wtforms.validators import ValidationError, DataRequired, Optional

from app.rules.adjustments import ALL_ADJUSTMENTS
from app.rules.models import PropertiesRules


class PropertyRuleFilterForm(FlaskForm):
    county = SelectField('County', id='select_county')
    town = SelectField('Town', id='select_town')
    apply = SubmitField('Apply')
    clear = SubmitField('Clear')


class PropertyRuleForm(FlaskForm):
    rule_name = StringField('Rule Name', validators=[Optional()])
    county = SelectField('County', validators=[DataRequired()], id='select_county')
    town = SelectField('Town', id='select_town')
    village = SelectField('Village', id='select_village')
    submit = SubmitField('Create')
    cancel = SubmitField('Cancel')

    def validate_town(self, field):
        if self.submit.data:
            rs_q = PropertiesRules.query.filter_by(county=self.county.data)
            if field.data:
                rs_q = rs_q.filter_by(town=field.data)
            else:
                rs_q = rs_q.filter(PropertiesRules.town.is_(None))
            rule_set = rs_q.first()
            if rule_set and (self.village.data or None) == rule_set.village:
                raise ValidationError('Property Rule for specified county and town is already present')


class PropertyRuleEditForm(FlaskForm):
    pr_id = HiddenField('Property Rule ID')
    rule_name = StringField('Rule Name', validators=[Optional()])
    county = SelectField('County', id='select_county',
                         render_kw={'disabled': ''}, validators=[Optional()])
    town = SelectField('Town', id='select_town')
    village = SelectField('Village', id='select_village')
    adjustments_all = SelectMultipleField('ALL Adjustments',
                                          choices=list(zip(ALL_ADJUSTMENTS.keys(),
                                                           ALL_ADJUSTMENTS.keys())),
                                          render_kw={"multiple": "multiple"},
                                          validators=[Optional()])
    adjustments_required = SelectMultipleField('Required Adjustments',
                                               choices=list(zip(ALL_ADJUSTMENTS.keys(),
                                                                ALL_ADJUSTMENTS.keys())),
                                               render_kw={"multiple": "multiple"},
                                               validators=[Optional()])

    save = SubmitField('Save')
    cancel = SubmitField('Cancel')
    delete = SubmitField('Delete')

    def validate_town(self, field):
        if self.save.data:
            rs_q = PropertiesRules.query.filter_by(county=self.county.data)
            if field.data:
                rs_q = rs_q.filter_by(town=field.data)
            else:
                rs_q = rs_q.filter(PropertiesRules.town.is_(None))
            rule_set = rs_q.first()
            if rule_set and str(rule_set.id) != self.pr_id.data and (
                    self.village.data or None) == rule_set.village:
                raise ValidationError('Property Rule for specified county and town is already present')


class SelectionRuleForm(FlaskForm):
    proximity_range = FloatField('Proximity range', validators=[Optional()])
    proximity_range_inherited = HiddenField('Proximity range inherited',
                                            validators=[Optional()])
    proximity_range_included = BooleanField()

    sale_date_from = DateField('Sale days before assessment',
                               validators=[Optional()])
    sale_date_from_inherited = HiddenField('Sale days before assessment inherited',
                                           validators=[Optional()])
    sale_date_from_included = BooleanField()

    sale_date_to = DateField('Sale days after assessment',
                             validators=[Optional()])
    sale_date_to_inherited = HiddenField('Sale days after assessment inherited',
                                         validators=[Optional()])
    sale_date_to_included = BooleanField()

    percent_gla_lower = IntegerField('Percent GLA Lower', [Optional()])
    percent_gla_lower_inherited = HiddenField('Percent GLA Lower inherited', validators=[Optional()])
    percent_gla_lower_included = BooleanField()

    percent_gla_higher = IntegerField('Percent GLA Higher', [Optional()])
    percent_gla_higher_inherited = HiddenField('Percent GLA Higher inherited', validators=[Optional()])
    percent_gla_higher_included = BooleanField()

    percent_lot_size_lower = IntegerField('Percent Lot Size Lower', [Optional()])
    percent_lot_size_lower_inherited = HiddenField('Percent Lot Size Lower inherited', validators=[Optional()])
    percent_lot_size_lower_included = BooleanField()

    percent_lot_size_higher = IntegerField('Percent Lot Size Higher', [Optional()])
    percent_lot_size_higher_inherited = HiddenField('Percent Lot Size Higher inherited', validators=[Optional()])
    percent_lot_size_higher_included = BooleanField()

    percent_sale_lower = IntegerField('Percent Sale Lower', [Optional()])
    percent_sale_lower_inherited = HiddenField('Percent Sale Lower inherited', validators=[Optional()])
    percent_sale_lower_included = BooleanField()

    percent_sale_higher = IntegerField('Percent Sale Higher', [Optional()])
    percent_sale_higher_inherited = HiddenField('Percent Sale Higher inherited', validators=[Optional()])
    percent_sale_higher_included = BooleanField()

    same_property_class = BooleanField('Same property class')
    same_property_class_inherited = HiddenField('Same property class inherited',
                                                validators=[Optional()])
    same_property_class_included = BooleanField()

    same_one_family_types = BooleanField('Same Family Types')
    same_one_family_types_inherited = HiddenField('Same Family Types inherited',
                                                  validators=[Optional()])
    same_one_family_types_included = BooleanField()

    same_school_district = BooleanField('Same school district')
    same_school_district_inherited = HiddenField('Same school district inherited',
                                                 validators=[Optional()])
    same_school_district_included = BooleanField()

    same_town = BooleanField('Same town')
    same_town_inherited = HiddenField('Same town inherited',
                                      validators=[Optional()])
    same_town_included = BooleanField()

    same_street = BooleanField('Same street')
    same_street_inherited = HiddenField('Same street inherited',
                                        validators=[Optional()])
    same_street_included = BooleanField()

    same_property_style = BooleanField('Same property style')
    same_property_style_inherited = HiddenField('Same property style inherited',
                                                validators=[Optional()])
    same_property_style_included = BooleanField()

    submit_sr = SubmitField('Save Selection Rule')
