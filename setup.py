from setuptools import find_packages, setup

setup(
    name = 'aabi_g4',
    version = '0.0.10',
    description = 'Portfólio Grupo 4',
    packages = find_packages(where = "."),
    url='https://github.com/rezekiz/alg.avancados.bioinf/',
    author='Grupo4',
    install_requires=[
        "pandas>=2.2.1",
        "graphviz>=0.20.3",
    ],
    python_requires=">=3.10",
    test_suite='tests'
)




