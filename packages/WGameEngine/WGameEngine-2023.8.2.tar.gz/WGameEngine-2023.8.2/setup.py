from setuptools import find_packages,setup

def main():
    with open('requirements.txt', 'r') as fs:
        required = fs.read().splitlines()
    setup(
        name = 'WGameEngine',
        version = '2023.8.2',
        author = 'JinyuFan Seven WangHaijie',
        install_requires = required,
        packages = find_packages(),
        include_package_data=True,
        zip_safe = False,
        package_data = {
            '':['*.*'],
            'static':['*.*']
        }
    )


if __name__ == '__main__':
    main()