from setuptools import setup, find_packages

setup(
    name='res_sum',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        "google-api-python-client",
        "google-auth",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        'PyMuPDF',
        'python-docx',
        'nltk',
        'GDriveOps',
        'voyageai',
        'langchain',
        'langchain-voyageai',
        'langchain-groq',
        'langchain-core',
        'langchain-community',
        'scikit-learn',
        'rouge-score',
        'ipywidgets ',
    ],
    dependency_links=[
        'https://pypi.org/simple/'
    ],
    entry_points={
        'console_scripts': [
            'res_sum=res_sum.research_summarizer:main',
        ],
    },
    author='Hammed A. Akande',
    author_email='akandehammedadedamola@gmail.com',
    description='A Python package Leveraging LLMs for Research Synthesis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/drhammed/res-sum',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)