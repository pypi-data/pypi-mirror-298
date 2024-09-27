from setuptools import setup, find_packages

setup(
    name='AI-DSTK',  # Use hyphens instead of underscores
    version='0.1.0',
    description='A modular and flexible AI library for processing text data',
    author='Alex Mendoza',
    author_email='alexander.mendoza.am@gmail.com',
    url='https://github.com/amendoxa/AI-DSTK',
    packages=find_packages(),
    install_requires=[
        'langchain_community',
        'pandas',
        'tqdm',
        # Add other dependencies if necessary
    ],
    include_package_data=True,
    package_data={
        'AI-DSTK': ['prompts/*.txt', 'configs/*.json'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)