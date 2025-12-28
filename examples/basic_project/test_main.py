import pytest
from click.testing import CliRunner
from main import hello, fetch_github_user


def test_hello_default():
    """Test hello command with default name."""
    runner = CliRunner()
    result = runner.invoke(hello)
    assert result.exit_code == 0
    assert 'Hello World!' in result.output


def test_hello_custom_name():
    """Test hello command with custom name."""
    runner = CliRunner()
    result = runner.invoke(hello, ['--name', 'Alice'])
    assert result.exit_code == 0
    assert 'Hello Alice!' in result.output


def test_hello_multiple_greetings():
    """Test hello command with multiple greetings."""
    runner = CliRunner()
    result = runner.invoke(hello, ['--count', '3'])
    assert result.exit_code == 0
    assert result.output.count('Hello World!') == 3
