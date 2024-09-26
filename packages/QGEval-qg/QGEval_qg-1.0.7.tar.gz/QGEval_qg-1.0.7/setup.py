from setuptools import setup, find_packages  
  
setup(  
    name='QGEval_qg',  
    version='1.0.7',  
    author='WeipingFu',  
    author_email='fuweiping1993@foxmail.com',  
    description='A tool for question generation based on LMs',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/WeipingFu/QGEval/tree/main',  
    packages=find_packages(),  
    classifiers=[  
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',  
        'Programming Language :: Python',  
        'Programming Language :: Python :: 3',  
        'Programming Language :: Python :: 3.7',  
        'Programming Language :: Python :: 3.8',  
        'Programming Language :: Python :: 3.9',  
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Database',  
    ],  
    python_requires='>=3.7',  
    install_requires=open('requirements.txt').read().splitlines(),  
)