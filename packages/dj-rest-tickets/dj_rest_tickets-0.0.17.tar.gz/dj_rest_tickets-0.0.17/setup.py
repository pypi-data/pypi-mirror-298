from setuptools import setup, find_packages

setup(
    name='dj-rest-tickets',  # The name of your library
    version='0.0.17',
    packages=find_packages(),  # Automatically finds packages
    include_package_data=True,
    license='MIT',  # License type
    description='A reusable Django app for XYZ functionality',
    long_description=open('README.md').read(),  # Long description from README.md
    long_description_content_type='text/markdown',
    url='https://github.com/AymaneNahji/dj-rest-tickets',  # Project URL
    author='Aymane Nahji',
    author_email='aymanenahjidev@gmail.com',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'Django==5.1.1',
        'django-cors-headers==4.4.0',
        'django-filter==24.3',
        'djangorestframework==3.15.2',
    ],
)

# rm -r dist build dj_rest_tickets.egg-info
# python setup.py sdist bdist_wheel #path('admin/', admin.site.urls),
# twine upload dist/* --skip-existing