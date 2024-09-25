from setuptools import setup, find_packages

setup(
    name = 'perpetual_context',
    version = '1.1.1',
    author = 'OPENSAPI',
    packages=find_packages(),
    install_requires=[
        'count-tokens==0.7.0',
        'requests==2.31.0',
        'numpy==1.25.2',
        'openpyxl==3.1.3',
        'pandas==2.2.2',
        'statistics==1.0.3.5',
        'certifi==2024.2.2',
        'tabulate==0.9.0',
        'PyPDF2==3.0.1',
        'PyMuPDF==1.24.5',
        'python-docx==1.1.0',
        'python-pptx==0.6.23',
        'beautifulsoup4==4.12.3',
        'youtube-search-python==1.6.6',
        'youtube-transcript-api==0.6.2',
        'pillow==10.3.0',
        'easyocr==1.7.1',
        'torch==2.3.0',
        'torchvision==0.18.0',
        'webcolors==1.13',
        'scikit-learn==1.5.0',
        'pydub==0.25.1',
       ' SpeechRecognition==3.10.3'
    ],
    url = 'https://github.com/',
    license = 'Proprietary Software'
)
