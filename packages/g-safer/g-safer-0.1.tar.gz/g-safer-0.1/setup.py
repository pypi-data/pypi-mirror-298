from setuptools import setup, find_packages
import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    
    name='g-safer', # 모듈 이름
    version='0.1', # 버전
    long_description= long_description, # READ.md에 보통 모듈 해놓음
    long_description_content_type= 'text/markdown',

    description='safer package', 
    author='rirakang',
    author_email='rirakang@gachon.ac.kr',
    
    url='https://github.com/gachon-CCLab/SAFER_LIB.git',
    install_requires = ['pytorch','pandas','numpy','sklearn','json','pickle'],
    include_package_data=True,
    packages = setuptools.find_packages(),
    python_requires=">=3.9.13" #파이썬 최소 요구 버전


)