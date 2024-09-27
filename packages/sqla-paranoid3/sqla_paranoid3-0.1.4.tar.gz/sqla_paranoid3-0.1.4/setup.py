from setuptools import find_packages, setup


with open('README.rst', 'r') as f:
    setup(
        name='sqla-paranoid3',
        version='0.1.4',
        description='Brings transparent soft delete to SQLAlchemy ORM',
        long_description=f.read(),
        long_description_content_type='text/x-rst',
        author='Sasha Hilton',
        author_email='sashahilton00@gmail.com',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
          'sqlalchemy',
          'Flask-SQLAlchemy',
        ],
        tests_require=[
          'psycopg2',
        ],
        test_suite="paranoid.tests",
        license='MIT',
    )
