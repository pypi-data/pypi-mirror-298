import json

import pytest
from typer.testing import CliRunner

from SecurePassX import (
    DB_READ_ERROR,
    SUCCESS,
    SecurePassX,
    __app_name__,
    __version__,
    cli,
)

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
    secret = [{"Title": "Get some milk.", "Username": "admin", "Password": "password"}]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(secret, db, indent=4)
    return db_file

test_data1 = {
    "title": ["AWS", "IAM", "User"],
    "username": "username",
    "password": "password",
    "secret": {
        "Title": "AWS IAM User.",
        "Username": "username",
        "Password": "gAAAAABm8lxnf5fc6M0zoHs4rqlp1nzpk3mukcQI01Z9cBowh10YteRnK9Gvhosgif1ItBveec7BlAo_3gMux5FQri41L4XaPA==",
    },
}
test_data2 = {
    "title": ["Microsoft AD User"],
    "username": "username",
    "password": "password",
    "secret": {
        "Title": "Microsoft AD User.",
        "Username": "username",
        "Password": "gAAAAABm8lxnf5fc6M0zoHs4rqlp1nzpk3mukcQI01Z9cBowh10YteRnK9Gvhosgif1ItBveec7BlAo_3gMux5FQri41L4XaPA==",
    },
}

@pytest.mark.parametrize(
    "title, username, password, expected",
    [
        pytest.param(
            test_data1["title"],
            test_data1["username"],
            test_data1["password"],
            (test_data1["secret"], SUCCESS),
        ),
        pytest.param(
            test_data2["title"],
            test_data2["username"],
            test_data2["password"],
            (test_data2["secret"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, title, username, password, expected):
    secreter = SecurePassX.SecPassSecret(mock_json_file)
    secreter.add(title, username, password)
    read = secreter._db_handler.read_secert()
    assert len(read.secret_list) == 2