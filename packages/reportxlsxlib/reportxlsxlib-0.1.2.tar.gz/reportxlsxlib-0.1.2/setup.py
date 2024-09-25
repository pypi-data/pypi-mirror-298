from setuptools import setup, find_packages
# 确定操作系统

setup(
    name='reportxlsxlib',
    version='0.1.2',
    packages=find_packages(),
    package_data={
        'reportxlsxlib': ['resources/windows/*.dll','resources/linux/*.dll'],
    },
    include_package_data=True,
    install_requires=[
        'pandas','openpyxl','pythonnet','aspose-cells==24.5.0'
    ],
    description='这是一个操作xlsx的库,win和linux都适配',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bailulue',
    author='bailu',
    author_email='yabailu@chinatelecom.cn'
)
