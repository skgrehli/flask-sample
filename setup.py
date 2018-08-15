from setuptools import setup

setup(
    name='jobwork.io',
    version='2018.3.6.6',
    packages=['build.lib.jobwork', 'build.lib.jobwork.auth', 'build.lib.jobwork.auth.settings',
              'build.lib.jobwork.conf', 'build.lib.jobwork.utils', 'build.lib.jobwork.views',
              'build.lib.jobwork.models', 'build.lib.jobwork.routes', 'build.lib.jobwork.middleware', 'jobwork',
              'jobwork.auth', 'jobwork.auth.settings', 'jobwork.conf', 'jobwork.utils', 'jobwork.views',
              'jobwork.models', 'jobwork.routes', 'jobwork.templates', 'jobwork.templates.emailTemplates',
              'jobwork.templates.front_saveonjobs', 'jobwork.middleware'],


    include_package_data=True,
    url='',
    license='',
    author='BALRAJ SINGH',
    author_email='',
    description=''
)
