from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional


class MassCmaRunForm(FlaskForm):
    county = SelectField('County', id='mass_cma_select_county', validators=[DataRequired()])
    assessment = SelectField('Assessment', id='mass_cma_select_assessment',
                             validators=[DataRequired()])
    assessment_stage = IntegerField('Assessment Stage')
    village = SelectField('Village', id='mass_cma_select_village', validators=[Optional()])
    sale_dates_from = DateField('Sale Dates From',
                                format='%Y-%m-%d',
                                id='mass_cma_sale_dates_from',
                                validators=[Optional()],
                                )
    sale_dates_to = DateField('Sale Dates To',
                              format='%Y-%m-%d',
                              id='mass_cma_sale_dates_to',
                              validators=[Optional()],
                              )
    start = SubmitField('Start')
    stop = SubmitField('Stop')


class MassCmaSelectForm(FlaskForm):
    computed_mass_cma = SelectField('Computed Mass Cma', id='computed_mass_cma', validators=[DataRequired()])
    select = SubmitField('Select')


class MassCmaFilterForm(FlaskForm):
    county = SelectField('County', id='select_county', render_kw={'class': 'form_control'})
    town = SelectField('Town', id='select_town', render_kw={'class': 'form_control'})
    village = SelectField('Village', id='select_village', render_kw={'class': 'form_control'})
    section = StringField('Section', render_kw={'placeholder': 'Enter Section Number'})
    block = StringField('Block', render_kw={'placeholder': 'Enter Block Name'})
    lot = StringField('Lot', render_kw={'placeholder': 'Enter Lot Number'})
    street = StringField('Street Name', render_kw={'placeholder': 'Enter Street Name'})
    number = StringField('House Number', render_kw={'placeholder': 'Enter House Number'})
    school_district = IntegerField('School District',
                                   render_kw={'placeholder': 'Enter School District'},
                                   validators=[Optional()])
    saving_min = IntegerField('Saving Min', render_kw={'placeholder': 'Enter Minimum Saving'},
                              validators=[Optional()])
    saving_max = IntegerField('Saving Max', render_kw={'placeholder': 'Enter Maximum Saving'},
                              validators=[Optional()])
    subject_sale_min = IntegerField('Subject Sale Min', render_kw={'placeholder': 'Enter Minimum Subject Sale'},
                                    validators=[Optional()])
    subject_sale_max = IntegerField('Subject Sale Max', render_kw={'placeholder': 'Enter Maximum Subject Sale'},
                                    validators=[Optional()])
    market_value_min = IntegerField('Minimum Market Value',
                                    render_kw={'placeholder': 'Enter Minimum Market Value'},
                                    validators=[Optional()])
    market_value_max = IntegerField('Maximum Market Value',
                                    render_kw={'placeholder': 'Enter Maximum Market Value'},
                                    validators=[Optional()])
    apply = SubmitField('Apply')
    clear = SubmitField('Clear')
