from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='Flastel',
  version='0.0.13a1',
  author='DepyXa',
  author_email='dere96632@gmail.com',
  description='Flastel – New core to Telegram Bot API.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/DepyXa/Flastel',
  packages=find_packages(),
  install_requires=[
    'requests>=2.25.1',
    'aiohttp>=3.8.6'
  ],
  keywords='Telegram Bot API bot python',
  project_urls={
    'GitHub': 'https://github.com/DepyXa/Flastel'
  },
  python_requires='>=3.6'
)