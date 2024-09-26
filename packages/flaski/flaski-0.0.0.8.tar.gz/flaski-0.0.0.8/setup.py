from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as f:
        # Devuelve una lista de paquetes, eliminando líneas vacías y comentarios
        return [line.strip() for line in f if line and not line.startswith('#')]

setup(
    name='flaski',
    version='0.0.0.8',
    packages=['flask_crud'],
    # packages=find_packages(),
    include_package_data=True,  # Incluye archivos de templates y estáticos
    description='Administra vistas con un enfoque diferente en flask.',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    # long_description=open('README.md').read(),
    author='Jodriz Dev',
    author_email='jrodriguez7603@utm.edu.ec',
    url='https://github.com/jrodre/flask_crud.git',
    install_requires=read_requirements(),
    # install_requires=[
    # "Flask",
    # "Flask-MySQLdb",
    # ],
    
)
