from setuptools import setup, find_packages

setup(
    name='switch_audio_device',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pulsectl',
    ],
    entry_points={
        'console_scripts': [
            'switch_audio_device=switch_audio_device.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
)
