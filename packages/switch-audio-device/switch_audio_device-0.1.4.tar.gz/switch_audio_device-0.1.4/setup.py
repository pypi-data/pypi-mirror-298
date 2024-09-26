from setuptools import setup, find_packages
import os

setup(
    name='switch_audio_device',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'pulsectl',
    ],
    entry_points={
        'console_scripts': [
            'switch_audio_device=switch_audio_device.main:main',
        ],
    },
    long_description="Creates a [rofi](https://github.com/davatorium/rofi) menu to select primary audio device on machines running Pulse Audio for managing their audio. You need to have rofi installed on the system for this to work.",
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
)
