from setuptools import setup, find_packages


with open("README.md", "r") as f:
  description = f.read()


setup(
  name='open_observe_tracking_django',
  version='0.2.1',
  packages= find_packages(),
  install_requires=[
    'requests',
    'Django>=4.1.6',
    'celery',

  ],
  long_description=description,
  long_description_content_type="text/markdown"
  

)