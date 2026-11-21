import os

import pytest

import pdfkit


def make_executable(directory):
    name = 'wkhtmltopdf.exe' if os.name == 'nt' else 'wkhtmltopdf'
    executable = directory / name
    executable.write_bytes(b'placeholder for discovery only')
    executable.chmod(0o755)
    return executable


def test_find_executable_without_external_lookup_tools(tmp_path, monkeypatch):
    executable = make_executable(tmp_path)
    monkeypatch.setenv('PATH', str(tmp_path))
    if os.name == 'nt':
        monkeypatch.setenv('PATHEXT', '.EXE')

    def reject_lookup_process(*args, **kwargs):
        raise AssertionError('executable discovery must not launch a helper process')

    monkeypatch.setattr('subprocess.Popen', reject_lookup_process)
    configuration = pdfkit.configuration()

    assert os.path.samefile(configuration.wkhtmltopdf, str(executable))


def test_missing_executable_has_installation_guidance(tmp_path, monkeypatch):
    monkeypatch.setenv('PATH', str(tmp_path))

    with pytest.raises(IOError, match='No wkhtmltopdf executable found') as error:
        pdfkit.configuration()

    assert 'Installing-wkhtmltopdf' in str(error.value)


def test_explicit_executable_does_not_require_path_lookup(tmp_path, monkeypatch):
    executable = make_executable(tmp_path)
    monkeypatch.setenv('PATH', '')

    configuration = pdfkit.configuration(wkhtmltopdf=str(executable))

    assert configuration.wkhtmltopdf == str(executable)
