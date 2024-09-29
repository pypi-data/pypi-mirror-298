#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2023
#

from setuptools import setup, find_packages
from sciveo.version import __version__

extras_require = {
      'mon': [
        'psutil>=0.0.0',
      ],
      'net': [
        'netifaces>=0.0.0',
        'scapy>=0.0.0',
      ],
      'media': [
        'scikit-learn', 'scipy', 'scikit-video', 'scikit-image', 'pycryptodome', 'exifread', 'qrcode[pil]',
        'boto3', 'pandas', 'pika', 'regex', 'matplotlib', 'joblib', 'tqdm',
        'ffmpeg-python', 'opencv-python-headless', 'opencv-contrib-python-headless',
      ],
      'media-server': ['fastapi', 'uvicorn[standard]'],
      'media-ml': [
        'tensorflow', 'keras', 'torch', 'torchvision', 'diffusers', 'transformers', 'accelerate', 'annoy',
      ]
}

extras_require['all'] = extras_require['mon'] + extras_require['net']
extras_require['media-all'] = extras_require['all'] + extras_require['media'] + extras_require['media-server'] + extras_require['media-ml']

setup(
    name='sciveo',
    version=__version__,
    packages=find_packages(),
    install_requires=[
      'numpy>=0.0.0',
      'requests>=0.0.0',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    extras_require=extras_require,
    py_modules=['sciveo'],
    entry_points={
      'console_scripts': [
        'sciveo=sciveo.cli:main',
      ],
    },
)
