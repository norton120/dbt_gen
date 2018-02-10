from setuptools import setup

setup(name= 'dbt_gen',
    version='0.1',
    description='Template generator for DBT using snowflake',
    url='https://github.com/norton120/dbt_gen',
    author='Ethan Knox',
    author_email='ethan.m.knox@gmail.com',
    licence='MIT',
    keywords='DBT data sql generator'
    packages=['dbt_gen'],
    install_requires=['dbt>=0.9.1',
                      'snowflake-connector-python>=1.4.15',
                      'PyYAML>=3.11',
                      'GitPython>=2.1.8',  
                     ],
    zip_safe=False)
