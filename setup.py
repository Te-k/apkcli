from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='apk',
    version='0.1.1',
    description='Another APK info tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Te-k/apk',
    author='Tek',
    author_email='tek@randhome.io',
    keywords='malware',
    include_package_data=True,
    install_requires=['androguard==3.3.5', 'ipython'],
    license='MIT',
    python_requires='>=3.5',
    packages=['apk', 'apk.plugins', 'apk.lib'],
    package_dir={'apk.lib': 'apk/lib'},
    entry_points= {
        'console_scripts': [ 'apk=apk.main:main' ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
