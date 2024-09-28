from setuptools import find_packages,setup
setup(
    name = 'WGameEngine',
    version = '2023.8.1',
    author = 'JinyuFan Seven WangHaijie',
    install_requires = ['pygame', 'pymunk', 'pytmx'],
    packages = find_packages(),
    include_package_data=True,
    zip_safe = False,
    package_data = {
        '':['*.*'],
        'static':['*.*']
    }
)
