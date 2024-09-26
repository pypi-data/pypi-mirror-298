from setuptools import setup, find_packages


setup(
    name='frasco',
    version='3.5.2',
    url='http://github.com/frascoweb/frasco',
    license='MIT',
    author='Maxime Bouroumeau-Fuseau',
    author_email='maxime.bouroumeau@gmail.com',
    description='Set of extensions for Flask to develop SaaS applications',
    packages=find_packages(),
    package_data={
        'frasco': [
            'api/templates/*.html',
            'assets/*.js',
            'assets/*.html',
            'billing/invoicing/emails/*',
            'billing/stripe/emails/*',
            'mail/templates/*.html',
            'mail/templates/layouts/*',
            'push/static/*.js',
            'templating/*.html',
            'templating/bootstrap/*.html',
            'users/emails/users/*',
            'users/templates/users/*.html'
        ],
    },
    zip_safe=False,
    platforms='any',
    install_requires=[
        'ago~=0.0.93',
        'apispec~=5.1.1',
        'authlib~=0.15.5',
        'boto3~=1.21.4',
        'eventlet~=0.33.0',
        'Flask~=2.1.2',
        'Flask-Assets==2.0',
        'Flask-Babel~=2.0.0',
        'Bcrypt-Flask~=1.0.2',
        'Flask-Login~=0.6.0',
        'Flask-Mail~=0.9.1',
        'Flask-Migrate~=3.1.0',
        'Flask-RQ2~=18.3',
        'Flask-SQLAlchemy~=2.5.1',
        'Flask-WTF~=1.0.0',
        'geoip2~=4.5.0',
        'glob2~=0.7.0',
        'inflection~=0.5.1',
        'jinja2>=3.1.0',
        'jinja-layout~=0.3',
        'jinja-macro-tags~=0.2',
        'Markdown~=3.3.6',
        'premailer~=3.10.0',
        'psycopg2-binary~=2.9.3',
        'pyotp~=2.6.0',
        'python-dateutil~=2.8.2',
        'python-slugify~=6.1.0',
        'python-socketio~=5.5.2',
        'PyYAML',
        'redis~=4.1.4',
        'requests~=2.27.1',
        'suds-py3~=1.4.1.0',
        'speaklater~=1.3',
        'stripe~=2.66.0',
        'werkzeug<2.2.0', # need to refactor frasco.ctx to update
        'rq<1.13.0' # need to refacto frasco.push
    ],
    entry_points='''
        [console_scripts]
        frasco=flask.cli:main
    '''
)
