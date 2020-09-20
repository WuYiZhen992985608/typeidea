from setuptools import setup,find_packages


setup(
    name='typeidea',
    version='0.1',
    description='Blog System base on Django',
    author='wuyizhen',
    url='http://www.wuyizhen.com',
    license='MIT',
    packages=find_packages('typeidea'),
    package_dir={'':'typeidea'},
    # package_data={'',[
    #     'themes/*/*/*/*',
    # ]},
    include_packages_data=True,
    install_requires=[
        'django==1.11',
    ],
    extras_require={
        'ipython':['ipython==7.16.1']
    },
    scripts=[
        'typeidea/manage.py',
    ],
    entry_points={
        'console_scripts':[
            'typeidea_manage = manage:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

)