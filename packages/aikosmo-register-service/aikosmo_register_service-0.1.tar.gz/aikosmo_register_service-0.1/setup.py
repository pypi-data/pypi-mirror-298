from setuptools import setup, find_packages

setup(
    name='aikosmo_register_service',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'supabase',
    ],
    author='Giulio Zani',
    author_email='giulio.zani@gmail.com',
    description='A package to register Cloud Run services with Supabase',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url='https://github.com/yourusername/aikosmo_register_service',
)
