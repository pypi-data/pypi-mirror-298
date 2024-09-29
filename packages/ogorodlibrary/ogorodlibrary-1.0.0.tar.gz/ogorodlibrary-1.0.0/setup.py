from setuptools import setup, find_packages

setup(
    name='ogorodlibrary',  # имя вашей библиотеки
    version='1.0.0',   # версия вашего пакета
    author='fhghfhfhfh', # ваше имя
    author_email='maximdev@internet.ru',  # это ваш email
    description='Это библиотека с датами посадки с/х культур для моей бабушки',
    long_description=open('README.md', encoding='utf-8').read(),  # описание из README файла
    long_description_content_type='text/markdown',
    url='',  # URL на ваш репозиторий
    packages=find_packages(),  # автоматически находит пакеты
    classifiers=[
        'Programming Language :: Python :: 3',  # укажите необходимую версию Python
        'License :: OSI Approved :: MIT License',  # лицензия
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',  # минимальная версия Python
)