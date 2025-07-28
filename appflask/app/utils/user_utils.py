from flask_script import Manager, prompt, prompt_pass
from flask_security.utils import hash_password

import config
from app.database import db
from app.database.models import User, Role

# from app import Role

manager = Manager(usage="User operations")


@manager.command
def adduser():
    """Add new user"""

    COUNT_CHECK_EMAIL = 0
    COUNT_CHECK_PASSWORD = 0

    while COUNT_CHECK_EMAIL < 3:
        if prompt:
            email = prompt(name='Email [required]', default=False)

            if email is not False and email.find('@') != -1:
                if prompt:
                    username = prompt(name='Username', default=False)

                    if not username:
                        username = ''

                    if prompt:

                        roles_for_select = {}
                        iteration = 1
                        for role in config.USER_ROLES:
                            roles_for_select[iteration] = role
                            iteration += 1

                        print('Please select user role:')
                        for key in roles_for_select:
                            print(key, roles_for_select[key].title())

                        user_role = 'guest'
                        try:
                            user_role = roles_for_select[int(prompt(name='', default=False))]
                        except ValueError:
                            pass
                        except KeyError:
                            pass

                    while COUNT_CHECK_PASSWORD < 3:
                        if prompt:
                            password = prompt_pass(name='Password [required]', default=False)

                        if prompt:
                            password_confirm = prompt_pass(name='Password confirm [required]', default=False)

                        if password and password_confirm:
                            password = password.strip()
                            password_confirm = password_confirm.strip()

                            if password == password_confirm:
                                role = Role.query.filter_by(name=user_role).first()
                                new_user = User(
                                    email=email,
                                    password=hash_password(password),
                                    username=username,
                                    role_id=role.id,
                                    active=True
                                )
                                db.session.add(new_user)
                                try:
                                    db.session.commit()
                                    COUNT_CHECK_EMAIL += 3
                                    print('Create new user')
                                    break
                                except Exception as e:
                                    print('\n\n')
                                    print('Error !')
                                    print(e)

                                    COUNT_CHECK_PASSWORD += 3
                            else:
                                print('Password is not confirm')
                                COUNT_CHECK_PASSWORD += 1
                                COUNT_CHECK_EMAIL += 3

                        else:
                            COUNT_CHECK_PASSWORD += 1
                            COUNT_CHECK_EMAIL += 3
            else:
                print("It's not email")
                COUNT_CHECK_EMAIL += 1
