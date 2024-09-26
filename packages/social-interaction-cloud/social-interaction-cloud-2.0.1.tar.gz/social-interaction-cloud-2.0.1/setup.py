from setuptools import setup, find_packages

requirements = ['numpy', 'redis', 'Pillow', 'six']

# dependencies for local machine
extras_require = {
    'local': [
        'opencv-python',
        'pyaudio',
        'pyspacemouse',
        'paramiko',
        'scp',
    ]
}

setup(
    name='social-interaction-cloud',
    version='2.0.1',
    author='Koen Hindriks',
    author_email='k.v.hindriks@vu.nl',
    packages=find_packages(),  # Automatically find packages
    install_requires=requirements,
    extras_require=extras_require,
)