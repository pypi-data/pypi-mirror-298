from setuptools import setup, find_packages
import os
import dessin_snt
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name = 'dessin_snt',
      version = dessin_snt.__version__,
      author = 'Christophe Viroulaud',
      author_email = 'christophe.viroulaud@ac-bordeaux.fr',
      keywords = 'dessin SNT Python',
      classifiers = ['Topic :: Education', 'Topic :: Games/Entertainment', 'Programming Language :: Python'],
      packages = ['dessin_snt'],
      description = 'Débuter la programmation en dessinant',
      long_description_content_type="text/markdown",
      long_description = long_description,
      license = 'GPL V3',
      platforms = 'ALL',
     )
