from setuptools import setup, find_packages

setup(
    name='knw_kakaowork_api',
    version='0.1.8',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='archon.oh',
    author_email='archon.oh@knworks.co.kr',
    url='https://github.com/daumsong/knw_kakaowork_api',
    py_modules=['knw_kakaowork_api'],  #패키지폴더 안만들때! 파일을 선택할때 필수!!!
    install_requires=['requests',],
    packages=find_packages(exclude=[]),
    keywords=['knw','kakaowork', 'kakaoworkapi', 'work'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
)
