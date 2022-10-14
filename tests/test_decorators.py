from owid.datautils.decorators import enable_file_download
from pytest import raises

from unittest import mock
from typing import Any
from .mocks import MockResponse


class TestEnableDownload:
    def test_local_args(self, tmpdir):
        """Test that the enable_download decorator works."""
        # Create local file
        text_init = "test"
        file_name = _write_local_file(tmpdir, text=text_init)
        # Build wrapped function (with decorator)
        func = enable_file_download(path_arg_name="path")(_test_local_file)
        text_final = func(file_name)
        assert text_init == text_final

    def test_local_kwargs(self, tmpdir):
        """Test that the enable_download decorator works."""
        # Create local file
        text_init = "test"
        file_name = _write_local_file(tmpdir, text=text_init)
        # Build wrapped function (with decorator)
        func = enable_file_download(path_arg_name="path")(_test_local_file)
        text_final = func(path=file_name)
        assert text_init == text_final

    def test_local_error(self, tmpdir):
        # Create local file
        text_init = "test"
        file_name = _write_local_file(tmpdir, text=text_init)
        # Build wrapped function (with decorator)
        func = enable_file_download(path_arg_name="path2")(_test_local_file)
        with raises(ValueError):
            _ = func(path=file_name)

    @mock.patch("owid.datautils.web.download_file_from_url", return_value=None)
    @mock.patch(
        "requests.Session.get", return_value=MockResponse({"key": "value"}, 200)
    )
    def test_download_kwargs(self, mock_download, mog_session_get):
        func = enable_file_download(path_arg_name="path")(_test_local_file)
        func(path="https://example.com/file.json")

    @mock.patch("owid.datautils.web.download_file_from_url", return_value=None)
    @mock.patch(
        "requests.Session.get", return_value=MockResponse({"key": "value"}, 200)
    )
    def test_download_args(self, mock_download, mog_session_get):
        func = enable_file_download(path_arg_name="path")(_test_local_file)
        func("https://example.com/file.json")


def _test_local_file(path):
    with open(path, "r") as f:
        text = f.read()
    return text


def _write_local_file(directory: Any, text: str = "test") -> Any:
    file_name = directory / "test.txt"
    with open(file_name, "w") as f:
        f.write(text)
    return file_name