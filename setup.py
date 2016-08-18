# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='WemooAgent',
    version='0.0.2',
    description='Aent for wemoo',
    url='https://github.com/wemoo/agent',
    author='Shawn Tien',
    author_email='hightian@gmail.com',
    license='MIT',
    packages=['wemoo_agent'],
    install_requires=['simplejson', 'requests', 'pymongo', 'daemonize'],
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'wemoo = wemoo_agent.wemoo_agent:main'
        ],
    })
