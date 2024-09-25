from setuptools import setup, find_packages

setup(
    name='screen2text',
    version='1.0.2',
    packages=find_packages(),
    install_requires=['SpeechRecognition',
                      'pygame',
                      'gTTS',
                      'pyautogui'
                      'requests',
                      'pyaudio',
                      'distutils-pytest',
                      'pycaw',
                      'comtypes'
                      ],
    include_package_data=True,

    package_data={
        '': ['app.py'],
    },
    description='screen2text ai is a simple screen to text chatbot',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='petteer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
