from setuptools import setup,find_packages


setup(
    name='typeidea',
    version='${version}',
    description='Blog System base on Django',
    author='wuyizhen',
    author_email='992985608@qq.com',
    url='http://127.0.0.1:8080',
    license='MIT',
    packages=find_packages('typeidea'),
    package_dir={'':'typeidea'},
    # package_data={'':[
    #     'themes/*/*/*/*',
    # ]},
    include_package_data=True,
    install_requires=[
        'django == 1.11',
        'gunicorn==19.8.1',
        'supervisor==4.0.0dev0',
        'xadmin==0.6.1',
        'mysqlclient==1.3.12',
        'django-ckeditor==5.4.0',
        'django-rest-framework==3.8.2',
        'django-redis==4.9.0',
        'django-autocomplete-light==3.2.10',
        'mistune==0.8.4',
        'Pillow==5.1.0',
        'coreapi==2.3.3',
        'hiredis==0.2.0',
        'django-debug-toolbar==1.9.1',
        'django-silk==3.0.0',
    ],
    # extras_require={
    #     'ipython':['ipython==6.2.1']
    # },
    scripts=[
        'typeidea/manage.py',
        'typeidea/typeidea/wsgi.py',
    ],
    entry_points={
        'console_scripts':[
            'typeidea_manage = manage:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Blog :: Django Blog',


        'License :: OSI Approved :: MIT License',


        'Programming Language :: Python :: 3.6',
    ],
)
