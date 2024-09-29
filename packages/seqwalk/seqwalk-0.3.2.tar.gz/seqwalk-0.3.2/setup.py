# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['seqwalk', 'seqwalk.prebuilt_libs']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.0,<2.0.0']

setup_kwargs = {
    'name': 'seqwalk',
    'version': '0.3.2',
    'description': 'Design orthogonal DNA sequences',
    'long_description': '# seqwalk\n\n`seqwalk` is a package for designing orthogonal DNA sequence libraries. It can efficiently generate libraries of sequences that satisfy sequence symmetry minimization constraints (i.e. minimizing longest common substrings). `seqwalk` additionally includes off-the-shelf orthogonal sequence libraries, as well as some tools for analyzing orthogonal sequence libraries. \nA code-free, interactive version of `seqwalk` can be found [here](https://colab.research.google.com/drive/1eVbcn_b5EE5FcL9NL5EyxeFAqNoImNSa?usp=sharing).\n\nFor more details, see the [paper](https://www.biorxiv.org/content/10.1101/2022.07.11.499592v1.abstract).\n\n## Installation\n\n```bash\n$ pip install seqwalk\n```\n\n## Usage\n\n### Designing a set of barcodes with minimal sequence symmetry\n\nIf you want a certain number of barcodes with maximum orthogonality, you can use the `max_orthogonality` function from the `design` module. You must specify the length of desired sequences (L) and the number of desired sequences (N). Optionally, specify the prevention of reverse complementary sequences, GC content limits, allowable alphabet, and specific prevented patterns. By default, reverse complementary sequences are allowed, there are no GC content constraints, a 3 letter (A/C/T, no G) code is used and any 4N sequence is prevented.\n\nFor example, if you want 100 barcodes with length 25, with prevented reverse complements, and a 4 letter alphabet, and between 10 and 15 G/C bases, you can use the following code:\n\n```python\nfrom seqwalk import design\n\nlibrary = design.max_orthogonality(100, 25, alphabet="ACGT", RCfree=True, GClims=(10, 15))\n```\n\nThis will generate a library of at least the specified size, with the strongest possible sequence symmetry constraint.\n\n### Designing a set of orthogonal barcodes with maximum size\n\nIf you have an orthogonality constraint in mind, you can use the `max_size` function from the `design` module to generate a maximally sized library with the given sequence symmetry minimization k values. That is, the shortest k for which no substring of length k appears twice.\n\nIf you want sequences that satisfy SSM for k=12, and you want barcodes of length 25, without considering reverse complementarity, and using a 4 letter alphabet, with no GC constraints, you can use the following code:\n\n```python\nfrom seqwalk import design\n\nlibrary = design.max_size(25, 12, alphabet="ACGT")\n```\n\n### Importing "off-the-shelf" experimentally characterized libraries\n\nThe `io` module provides the ability to import libraries that have been previously experimentally characterized, using code of the following format.\n\n```python\nfrom seqwalk import io\n\nPERprimers = io.load_library("kishi2018")\n```\n\nWe provide the following libraries, accessible with the identifier tag.\n\n| identifier | # of seqs | seq length | original use case | ref |\n|------------|-----------|------------|-------------------|-----|\n| `kishi2018` | 50 | 9nt | PER primers | [Kishi et al, 2018](https://www.nature.com/articles/nchem.2872) |\n\nIf you have an orthogonal library you would like to add, please submit a PR!\n\n### Quality control using pairwise comparisons\n\nOnce you have a library in the form of a list of sequences, you can use the `analysis` module to perform additional quality control. For example, we provide a function to compute pairwise Hamming distances.\n\n```python\nfrom seqwalk import analysis\n\nh_crosstalk = analysis.hamming_matrix(seqs)\n```\n\nSince sequence symmetry minimization does not explicitly guarantee low off-target hybridization strength, a simple function for using NUPACK to identify "bad" sequences is included in the `analysis.py` file. However, it is commented out to avoid the NUPACK dependency in the package (problematic due to NUPACK licensing).\n\n## License\n\n`seqwalk` is licensed under the terms of the MIT license.\n\n## Credits\n\n`seqwalk` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Gokul Gowri',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
