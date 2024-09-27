from setuptools import setup, find_packages

setup(
    name='opensdpc',
    version='1.0.0',
    description='Python library for processing whole slide images (WSIs) in sdpc format',
    license='MIT License',
    author='Jiawen Li',
    author_email='jw-li24@mails.tsinghua.edu.cn',
    packages=find_packages(),
    include_package_data=True,
    platforms=['Linux'],
    install_requires=[
        'numpy',
        'Pillow',
        'opencv-python'
    ]
)