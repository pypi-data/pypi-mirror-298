from setuptools import setup, find_packages

setup(
    name='fpessoa-mypackage',  # Nome do pacote
    version='1.0.3',  # Versão inicial
    packages=find_packages(),  # Encontra automaticamente pacotes Python no diretório
    install_requires=[],  # Dependências, se houver
    author='Fernando Pessoa',
    author_email='fernando.pessoa@segment.net.br',
    description='Um pacote de exemplo',
    url='https://github.com/fpessoa64/myproject',  # Repositório do GitHub
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versão mínima do Python
)