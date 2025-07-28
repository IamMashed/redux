from collections import namedtuple
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from datetime import date

from my_logger import get_file_logger
from . import mail

EmailTuple = namedtuple('EmailTuple', ['title', 'template_path'])

logger = get_file_logger(__name__, log_file='sent_email.log')


class EmailToClient:
    # check = EmailTuple(title='Pay by check', template_path='email/pay_by_check')
    # credit_card = EmailTuple(title='Pay by credit card',
    #                          template_path='email/pay_by_credit_card')

    welcome = EmailTuple(title='Welcome aboard!',
                         template_path='email/welcome_aboard')
    sign_email = EmailTuple(title='Welcome aboard!',
                            template_path='email/sign_email')
    thank_you = EmailTuple(title='Your application was approved',
                           template_path='email/acknowledgement')
    thank_you_check = EmailTuple(title='Your application was approved',
                                 template_path='email/acknowledgement_check')
    thank_you_card_unpaid = EmailTuple(title='Your application was approved',
                                       template_path='email/acknowledgement_card_unpaid')
    rejected = EmailTuple(title='Your application has been rejected',
                          template_path='email/rejected')
    case_worked = EmailTuple(title='Your case has been worked up!',
                             template_path='email/great_news')
    case_submitted = EmailTuple(title='Your case has been submitted to your county!',
                                template_path='email/case_submitted')
    reduce_success = EmailTuple(title='Congratulations! Your property taxes have been reduced by ${} ({}%).',
                                template_path='email/success')
    reduce_failure = EmailTuple(title='Unfortunately, we weren’t able to reduce your property taxes this year',
                                template_path='email/failure')
    daily_email = EmailTuple(title="",
                             template_path='email/daily_email')
    # vab = EmailTuple(title="Your application was submitted to VAB",
    #                  template_path='email/vab')
    vab = EmailTuple(title="Petition successfully submitted",
                     template_path='email/vab')


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, email_to_client, attachment=None, invoice=None, template_extension='.html', **kwargs):
    """
    We may have two types of attachment. One could be application itself as attachment
    Second one could be the invoice when one selected to pay by check.
    """
    app = current_app._get_current_object()

    if not app.config['MAIL_ALLOWED']:
        return

    address = kwargs.get('address')

    # we may have multiple or single email receipients
    # multiple happens for the daily emails we send informing new applications count
    recipients = to if type(to) == list else [to]
    sender = app.config['MAIL_SENDER']

    msg = Message(email_to_client.title, sender=sender, recipients=recipients)
    logger.info(f'Sent an email from {sender} to {recipients} with subject {email_to_client.title}')

    if template_extension == '.html':
        msg.html = render_template(email_to_client.template_path + template_extension, **kwargs)
    else:  # means template extension is '.txt'
        msg.body = render_template(email_to_client.template_path + template_extension, **kwargs)

    if attachment:
        with app.open_resource(attachment) as fp:
            attachment_name = '-'.join(
                [
                    date.today().strftime('%m.%d.%y'),
                    'Redux Application',
                    f'{address}.pdf',
                ]
            )
            msg.attach(attachment_name, "application/pdf", fp.read())

    if invoice:
        with app.open_resource(invoice) as fp:
            attachment_name = '-'.join(
                [
                    date.today().strftime('%m.%d.%y'),
                    'Redux Filing Fee Invoice',
                    f'{address}.pdf',
                ]
            )
            msg.attach(attachment_name, "application/pdf", fp.read())

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def make_and_send_email(application, email_type, context):
    """
    Send application submission welcome email
    """
    import pdfkit

    # send email to recipient
    send_email(application.email.email_address, email_to_client=email_type, **context)

    # create html email pdf binary
    html_string = render_template(email_type.template_path + '.html', **context)

    # create a .pdf email file from html string
    pdf = pdfkit.from_string(html_string, False).decode('ISO-8859-1').encode('utf-8')

    return pdf
