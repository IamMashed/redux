from flask_script import Manager, prompt, prompt_bool

import config

manager = Manager(usage='Perform babel operations')


@manager.command
def help():
    """Babel help"""
    print('Important !')
    print('For each language that supports a globalcma')
    print('its own language pack is required,')
    print('if the client’s default language is different from the application language,')
    print('then lines may be displayed not from the messages.po file,')
    print('but directly from the HTML template or source code.')
    print('\n\n')
    print('For create translations you need create messages.pot file')
    print('Use python manage.py babel create_pot')
    print('\n')
    print('After create a messages.pot file you need create translations')
    print('Use python manage.py babel create_translations for create translations')
    print('\n')
    print("""After create translations you can edit them in
/app/translations/your language code (en)/LC_MESSAGES/messages.po""")
    print('Example:')
    print('#: app/templates/hello.html:1')
    print('msgid "Hello"')
    print('msgstr "" there should be a line that appears in the user interface instead msgid')
    print('\n')
    print('After edit messages.po')
    print('Use python manage.py babel compile_translations')
    print('Restart Globalcma')
    print('\n')
    print('If change any string on Globalcma you can just update messages.po without lost previos settings')
    print('For update first create new messages.pot')
    print('Use python manage.py babel create_pot')
    print('And update translation')
    print('Use python manage.py babel update_translations')
    print('Restart Globalcma')


@manager.command
def create_pot():
    'Create a .pot file'
    import os
    os.system('pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .')
    del os
    print('\n\n')
    print('Create .pot file complete')


@manager.command
def update_translations():
    'Update translations if add or remove strings'
    import os
    os.system('pybabel update -i messages.pot -d app/translations')
    del os
    print('\n\n')
    print('Update translations complete')


@manager.command
def create_translations():
    'Create translations'

    if prompt_bool('''Are you sure you want to create translation (if there is an old translation then it will be lost)
you can user manage.py babel update_translations for update if you did not want lose all strings'''):

        languages_for_select = {}
        iteration = 1
        for lang in config.LANGUAGES:
            languages_for_select[iteration] = lang
            iteration += 1

        print('Pleese enter number of language for translation')
        for key in languages_for_select:
            print(key, languages_for_select[key])

        language = prompt(name='', default=False)

        if language is False:
            language = config.BABEL_DEFAULT_LOCALE
        else:
            try:
                language = languages_for_select[int(language.strip())]
            except ValueError:
                language = config.BABEL_DEFAULT_LOCALE

        import os
        os.system('pybabel init -i messages.pot -d app/translations -l {}'.format(language))
        del os
        print('\n\n')
        print('Create translation {} complete'.format(language))
        print('''Now edit the {}/translations/{}/LC_MESSAGES/messages.po file as needed.
Check out some gettext tutorials if you feel lost.'''.format(config.APP_ROOT, language))


@manager.command
def compile_translations():
    'Compile translations'

    import os
    os.system('pybabel compile -d app/translations')
    del os
    print('\n\n')
    print('Compile translations complete')
    print('Pleese restart Globalcma application')
