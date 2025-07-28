from flask import jsonify, request

from app.case_management.models import Application, PaymentType, PaymentStatus
from app.routing.errors import bad_request, not_found
from shopify_hooks.main import main


# @main.route('/', methods=['GET'])
# def index():
#     print(request)
#     return render_template('index.html')


def payment_verified(info, confirmed, status):
    if info and confirmed and status == 'paid':
        if info[0]:
            # must be 'application_id'
            name = info[0].get('name')

            # must be integer
            try:
                value = int(info[0].get('value'))
                if name == 'application_id' and value:
                    return True
            except ValueError:
                return False
    return False


@main.route('/shopify_hook', methods=['GET', 'POST'])
def index():
    print(request)

    json_data = None
    try:
        json_data = request.get_json()
    except Exception as e:
        print(e)

    if json_data:
        print(json_data['note_attributes'])
        print(json_data['confirmed'])
        print(json_data['financial_status'])

        info = json_data.get('note_attributes')
        confirmed = json_data.get('confirmed')
        status = json_data.get('financial_status')

        if not payment_verified(info, confirmed, status):
            return bad_request(message="Invalid payment")

        application_id = int(info[0].get('value'))
        application = Application.get(application_id)
        if not application:
            return not_found(message=f"Application with id={application_id} was not found")

        # update application payment info
        application.update_payment_info(payment_type_id=PaymentType.CARD, payment_status_id=PaymentStatus.PAID)
    else:
        print("no json data")
    #  print(request.get_data())
    print(request.headers)
    try:
        request.headers.get('X-Shopify-Hmac-SHA256')
    except Exception as e:
        print(e.args)
    return jsonify(success=True)
