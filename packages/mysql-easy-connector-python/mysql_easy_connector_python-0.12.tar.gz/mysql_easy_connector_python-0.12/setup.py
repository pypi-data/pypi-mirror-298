from setuptools import setup, find_packages

setup(
    name='mysql-easy-connector-python',
    version='0.12',
    packages=find_packages(),
    install_requires=["mysql-connector-python"],  # وابستگی‌ها را اضافه کنید
    description='Easy Mysql ',
    author='mdev2007',
    author_email='m.programmer20070@gmail.com',
)
