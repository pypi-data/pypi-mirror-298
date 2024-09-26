from setuptools import setup, find_packages

setup(
    name='task_5_syrkin',
    version='0.0.4',
    package_dir={'': 'src'},  # Указываем, что исходный код лежит в папке src
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'task_5_syrkin=task_5_SYRKIN.collection_app:main',  # Укажи правильный путь к функции main
        ],
    },
)
