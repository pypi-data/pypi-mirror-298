from setuptools import setup, find_packages

setup(
    name = 'infinite_context',
    version = '1.0.6',
    author = 'OPENSAPI',
    packages=find_packages(),
    install_requires=[
        'perpetual-context==1.1.2',
        'certifi==2024.2.2',
        'requests==2.31.0',
        'lxml==5.2.2',
        'pandas==2.2.2',
        'pillow==10.3.0',
        'numpy==1.25.2',
        'paddlepaddle==2.6.0',
        'paddleocr==2.7.3',
        'opencv-python==4.6.0.66',
        'moviepy==1.0.3',
        'SpeechRecognition==3.10.3',
        'ffmpeg-python==0.2.0',
        'pydub==0.25.1',
        'docx2txt==0.8'
    ],
    url = 'https://github.com/',
    license = 'Proprietary Software'
)
