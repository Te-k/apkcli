from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='apkcli',
    version='0.1.3',
    description='Another APK info tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Te-k/apkcli',
    author='Tek',
    author_email='tek@randhome.io',
    keywords='malware',
    include_package_data=True,
    install_requires=['androguard==3.3.5', 'ipython', 'yara-python==4.1.0', 'lxml>=4.2.6'],
    license='MIT',
    python_requires='>=3.5',
    packages=['apkcli', 'apkcli.plugins', 'apkcli.lib', 'apkcli.data'],
    package_dir={'apkcli.lib': 'apkcli/lib'},
    package_data={'apkcli': ['apkcli/data/*.csv']},
    entry_points={
        'console_scripts': ['apkcli=apkcli.main:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
