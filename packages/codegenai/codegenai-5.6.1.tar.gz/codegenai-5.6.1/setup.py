from setuptools import setup, find_packages

setup(name = 'codegenai',
      version = '5.6.1',
      description = "AI Algorithms And Computer Network Related Code",
      author = 'Anonymus',
      package_data={'':['licence.txt', 'README.md', 'Notebooks\\*']},
      include_package_data=True,
      install_requires = ['networkx','matplotlib','tqdm'],
      packages = find_packages(),
      zip_safe = False)