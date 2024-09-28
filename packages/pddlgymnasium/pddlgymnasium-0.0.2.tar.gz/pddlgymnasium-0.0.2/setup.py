from setuptools import setup, find_packages

setup(name='pddlgymnasium',
      version='0.0.2',
      description='Gym environment based PDDL problem description',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      install_requires=[
            'matplotlib',
            'pillow>=8,<10',
            'gymnasium<1.0.0',
            'imageio',
            'networkx',
            'scikit-image',
      ],
      python_requires='>=3.8',
      packages=find_packages(),
      package_data={'pddlgymnasium': ['rendering/assets/*', '**/*.pddl']},
      include_package_data=True,
)
