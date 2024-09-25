# Packaging

## Publishing the package

    poetry config keyring.enabled false

    poetry config pypi-token.pypi <toke>

## Authentication

    ~/.config/pypoetry/auth.toml

## Using this token

    $HOME/.pypirc

    [pypi]
    username = __token__
    password = pypi-AgEIcHlwaS5vcmcCJDgwMDA0OTE0LWIzNGEtNDg4Ni05OGU5LTg3ZWU2NjViYTg1ZgACKlszLCIzYzRlM2J
