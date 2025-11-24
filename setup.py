
from setuptools import setup, find_packages

setup(
    name='viber-dev-environment',
    version='0.1.0',
    author='Jericho',
    author_email='',
    description='A suite of tools for AI-driven software development.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/viber',  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        'lancedb',
        'pandas',
        'pyarrow',
        'sentence-transformers',
        'torch',
        'transformers',
        'PyQt5',
        'black'
    ],
    entry_points={
        'console_scripts': [
            'viber-agent = agent:main',
            'viber-gui = projects.llm_os_gui.gui.main_window:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Build Tools',
    ],
)
