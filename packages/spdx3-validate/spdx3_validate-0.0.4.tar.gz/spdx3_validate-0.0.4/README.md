# SPDX 3 Validation Tool

Validates SPDX 3 documents

While standalone tools like `pyshacl` and `check-jsonschema` can use used to
validation SPDX 3 documents, there are a few context aware checks that can be
useful. This includes:

1. Ignored SHACL errors for missing `SpdxIds` if they are defined in an
   `ExternalMap`
2. Validation that any `SpdxIds` defined in an `ExternalMap` are _not_ present
   in the document
3. SHACL Validation of merged documents (in this way, if you reference an
   `SpdxId` from an `ExternalMap` and then pass the document that provides that
   `SpdxId`, the type can be validated
4. (Hopefull) More useful JSON schema error output


## Installation

`spdx3-validate` can be installed using `pip`:

```shell
python3 -m pip install spdx3-validate
```

## Developing

Developing on `spdx3-validate` is best done using a virtual environment. You
can configure one and install spdx3-validate in editable mode with all
necessary development dependencies by running:

```shell
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

## TODO

* Option to automatically download dependencies based on `locationHint`
* Offline validation?

``
