from setuptools import setup, find_packages

setup(
    name='jtml-compiler',
    version='1.0.0',
    description='JTML Compiler for building decentralized applications',
    author='NEON VORTICES J. HOLDINGS UNIPESSOAL LDA., Portugal',
    author_email='joao@j4.computer',
    url='https://github.com/mrjohnnyrocha-j/jtml',
    packages=find_packages(),
    install_requires=[
        'rjsmin',
        'csscompressor',
    ],
    entry_points={
        'console_scripts': [
            'jtml-compile=jtml_compile.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
