## Creating the Python pip package (personal notes)

After creating and testing the code, make a Python pip package as follows:

Update the file ``setup.py`` and update version number.

In the library folder, create the package

``python3 setup.py sdist bdist_wheel``

Before uploading the package to Pypi it is wise to test the package on your system.

Load the package to the system with:

``pip install .``

After you've checked that everything is worknig correctly, then use the following command to upload to Pypi.
You'll have to install twine for this (``pip install twine`` or ``sudo apt install twine``)

When you get the error:

```
ImportError: cannot import name 'appengine' from 'requests.packages.urllib3.contrib' (/home/user/.local/lib/python3.10/site-packages/urllib3/contrib/__init__.py)
```

You should do a ``pip install --upgrade twine requests-toolbelt``.

### Before uploading

```
# Check first

twine check dist/*

# Test upload first

twine upload -r testpypi dist/*

# Upload to Pypi

twine upload dist/*
```

Note: uploading new versions requires to delete the older versions from the /dist folder.

Another option is to use the ``--skip-existing`` option like this:

```
# Testpypi
twine upload -r testpypi dist/* --skip-existing 

# ProductionPypi
twine upload -r pypi dist/* --skip-existing
```

### Uploading with 2FA enabled

First create an API token (at https://test.pypi.org/manage/account/token/).

Create a file .pypirc in your home folder (e.g. ``nano $HOME/.pypirc``)

Add the given token to the file like this:

```
[testpypi]
  username = __token__
  password =
pypi-AgENdGVzdC5weXtMjBjOS00ZjgxLWIyZDMtYWViMDAwOTk3MWZmAAIqWzMsImU3YjkzMGVmLWQzMGItNGFhYi1iNB6NZ-rSrzc8UXHRmWp5fzZwP


[pypi]
  username = __token__
  password =
pypi-AgEIcHlwaS5vcmcCJDgxYWFiYjYwLTMxYmUtNDczZC1hNjBhLTU0MDJhNmQ2NmZhMgAQ3NTAtOGVkNy0xN2U0NmU0MjEzMQFAYWNj0FcsP-Slnj9-wkEWWwQXkaw
```

Save the file and reload environment if necessary.

Now you an upload libraries without having to use the password.