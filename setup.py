from setuptools import setup


setup(
    name='LayerClient',
    version='0.1.10',
    packages=['LayerClient'],
    description='Client for the Layer Platform API',
    url='https://github.com/Jana-Mobile/layer-python',
    maintainer='Jana',
    maintainer_email='opensource@jana.com',
    license='Apache 2.0',
    install_requires=[
        'python-dateutil',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
