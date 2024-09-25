from setuptools import setup

name = "types-jwcrypto"
description = "Typing stubs for jwcrypto"
long_description = '''
## Typing stubs for jwcrypto

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`jwcrypto`](https://github.com/latchset/jwcrypto) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`jwcrypto`.

This version of `types-jwcrypto` aims to provide accurate annotations
for `jwcrypto==1.5.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/jwcrypto. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`6cddd30ff2a64f6a3e509c992684c4a0a357fe71`](https://github.com/python/typeshed/commit/6cddd30ff2a64f6a3e509c992684c4a0a357fe71) and was tested
with mypy 1.11.1, pyright 1.1.381, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="1.5.0.20240925",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/jwcrypto.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['cryptography'],
      packages=['jwcrypto-stubs'],
      package_data={'jwcrypto-stubs': ['__init__.pyi', 'common.pyi', 'jwa.pyi', 'jwe.pyi', 'jwk.pyi', 'jws.pyi', 'jwt.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
