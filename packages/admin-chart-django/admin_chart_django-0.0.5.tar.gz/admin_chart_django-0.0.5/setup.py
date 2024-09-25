from setuptools import setup, find_packages

setup(
    name='admin_chart_django',
    version='0.0.5',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django package for chart/graph',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rimalsparsha/django_chart.git',  # URL of your package repository
    author='Sparsha Rimal',
    author_email='sparsharimal@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 3.2',  
    ],
    install_requires=[
        'Django>=3.2',
    ],
)
