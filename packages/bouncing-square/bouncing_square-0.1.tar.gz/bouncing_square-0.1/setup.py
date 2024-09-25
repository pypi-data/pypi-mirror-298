from setuptools import setup, find_packages

setup(
    name='bouncing_square',  # Nome do pacote
    version='0.1',  # Versão inicial
    description='A simple 2D bouncing square game',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seu_usuario/bouncing_square',  # Link para o repositório
    author='Seu Nome',
    author_email='seu_email@example.com',
    license='MIT',
    packages=find_packages(),  # Encontrar automaticamente os pacotes
    install_requires=[
        'pygame',  # Dependência necessária para rodar o jogo
    ],
    entry_points={
        'console_scripts': [
            'bouncing-square=bouncing_square.game:main',  # Comando para rodar o jogo no terminal
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    include_package_data=True,  # Incluir arquivos extras no pacote
)
