from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

with open("LICENSE", 'r') as f:
    license = f.read()

project_urls = {
  'GitHub': 'https://github.com/sidqdev/saconfig',
  'Telegram': 'https://t.me/sidqdev'
}


setup(
    name='saconfig',
    version='0.0.2',
    author='Sidq',
    author_email='abba.dmytro@gmail.com',
    description='Flexible config module to manage env variables',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=license,
    project_urls=project_urls,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    python_requires='>=3.6',
)

