from flask_script import Manager

from app import create_app

app = create_app()
manager = Manager(app)

from app.utils.database_utils import manager as database_manager  # noqa
from app.utils.user_utils import manager as users_manager  # noqa
from app.utils.babel_utils import manager as babel_manager  # noqa

manager.add_command('db', database_manager)
manager.add_command('user', users_manager)
manager.add_command("babel", babel_manager)

if __name__ == "__main__":
    manager.run()
