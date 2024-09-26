from setuptools import setup, find_packages

setup(
    name='task_5_syrkin',
    version='0.0.6',
    packages=find_packages(where='src'),  # Указываем, что пакеты находятся в папке src
    package_dir={'': 'src'},  # Корневой каталог кода
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'task_5_syrkin=task_5_SYRKIN.collection_app:main',  # Путь к функции main в твоем коде
        ],
    },
)
