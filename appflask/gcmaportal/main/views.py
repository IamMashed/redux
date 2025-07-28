import urllib.parse
from datetime import datetime

from flask import render_template, abort, request, redirect

from app.case_management.models import CaseEmail, Note, NoteSender, NoteType, Application
from gcmaportal.main import main

REDUX_URL = 'https://www.redux.tax/pages/email-confirmed'


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/confirm_email/<token>')
def confirm_email(token):
    if not token:
        return abort(404)

    app_id = request.args.get('application_id')
    app = Application.get_by(id=app_id)
    if not app:
        return abort(404)

    # sample token = 'XZY2N2MC0P5DIY6GX4KP2F5P34TTIGH5'
    case_email = CaseEmail.get_by(confirm_token=token)
    if not case_email:
        return abort(404)

    # confirm email if not confirmed
    if not case_email.confirmed_at:
        case_email.confirmed_at = datetime.now()

        Note.create_system_note(
            NoteSender.CASE_EMAIL,
            case_email,
            "Validation email link clicked",
            NoteType.MANUAL
        )

    case_email.save()

    # If payment status = Paid or payment type is not credit card, then:
    if app.is_paid() or not app.is_credit_card_payment():
        to_url = REDUX_URL

    # If:
    # 1. the application has payment type = Credit Card
    # 2. payment status = Unpaid
    # 3. payment_link is not empty  (payment_link is a string inside application table)
    elif app.is_credit_card_payment() and not app.is_paid() and app.payment_link:
        to_url = REDUX_URL + f'?payment_url={urllib.parse.quote_plus(app.payment_link)}'
    else:
        to_url = REDUX_URL + '?payment_url=payment_url_address'

    return redirect(to_url)
