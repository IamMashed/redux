import json
import requests
from datetime import datetime
from flask import Blueprint, make_response
from flask import request
from flask import jsonify
from flask import abort

from app.case_management.models import Note, NoteSender, NoteType, CaseEmail, Application, ApplicationStatus, Client

bp = Blueprint('bounce', __name__, url_prefix='/bounce')


@bp.route('/confirm_email', methods=['POST'])
def confirm_email():
    r = request.get_data()
    js = json.loads(r)
    # After successful creation of the subscription request
    if js.get("Type") == "SubscriptionConfirmation":
        subscribe_url = js["SubscribeURL"]
        requests.get(subscribe_url)

    try:
        subject = js['mail']['commonHeaders']['subject']
        email = js['mail']['commonHeaders']['to'][0]

        if subject == 'Welcome aboard!':
            email = CaseEmail.query.filter(CaseEmail.email_address == email).first()
            if not email:
                return abort(418)
            email.failed_at = datetime.now()
            email.save()

            # get all applications with the email address
            applications = Application.query.filter_by(email_id=email.id).all()

            # filter out 'fully rejected' and 'approved' applications
            applications = [
                app for app in applications if app.status_id not in (
                    ApplicationStatus.FULLY_REJECTED, ApplicationStatus.APPROVED
                )
            ]

            # Create an event for each application that is not in a final state
            if applications:
                for app in applications:
                    Note.create_system_note(
                        note_type=NoteType.EMAIL_BOUNCED,
                        note_sender=NoteSender.APPLICATION,
                        obj=app,
                        note_text='Email Bounce/Complaint',
                        attachment=r,
                        attachment_extension='.json',
                    )
            else:
                # Create an event for a client if there is no such application
                client = Client.get_by(email_id=email.id)
                if client:
                    Note.create_system_note(
                        note_type=NoteType.EMAIL_BOUNCED,
                        note_sender=NoteSender.CLIENT,
                        obj=client,
                        note_text='Email Bounce/Complaint',
                        attachment=r,
                        attachment_extension='.json',
                    )

    except (IndexError, KeyError):
        return abort(418)

    return make_response(jsonify(js))
