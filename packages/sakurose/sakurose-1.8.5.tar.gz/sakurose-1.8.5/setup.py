from setuptools import setup, find_packages

setup(
    name='sakurose',
    version='1.8.5',
    description='SakuRose: Simplifica la creación de códigos en Python3.9 o superior, de uso gratuito e ilimitado.',
    author='InsAnya606',
    author_email='insanyadev@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Pillow',
        'discord.py',
        'pytz',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)