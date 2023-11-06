from setuptools import setup, find_packages

setup(
    name='objtracker',
    version='1.1.0',
    description='The modified version of sort tracking (https://github.com/abewley/sort) compatible with the Yolo Series',
    author='amish0',
    author_email='amishkumar562@gmail.com',
    url='https://github.com/amish0/Tracking',
    # packages=find_packages(),
    include_package_data=True,
    # package_dir={'': 'tracker'},
    package_data={'': ['cfg/*.yaml']}, # include all *.yaml files
    install_requires=[
        'numpy',
        'PyYAML',
        'filterpy',
        'scikit-image',
        'lapx',
        'opencv-python',
    ],
    packages=['tracker', 'tracker.Sort_Tracker', 'tracker.basic_utils', 'tracker.Bot_Tracker', 'tracker.BYTE_Tracker', 'tracker.tracker_utils'],
)
