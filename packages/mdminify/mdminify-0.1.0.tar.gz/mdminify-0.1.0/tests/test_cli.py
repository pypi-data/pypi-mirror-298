import json

from click.testing import CliRunner

from mdminify.cli import cli


def test_remove_links_cli(tmp_path):
    runner = CliRunner()

    # Create a sample markdown file
    input_md = tmp_path / "input.md"
    input_md.write_text(
        "I am proficient in [Python](https://www.python.org/) and [JavaScript](https://www.javascript.com/)."
    )

    output_md = tmp_path / "output.md"
    output_json = tmp_path / "links.json"

    # Run the remove command
    result = runner.invoke(cli, ["remove", str(input_md), str(output_md), str(output_json)])

    assert result.exit_code == 0
    assert output_md.read_text() == "I am proficient in Python and JavaScript."
    with open(output_json) as f:
        assert json.load(f) == {
            "Python": "https://www.python.org/",
            "JavaScript": "https://www.javascript.com/",
        }


def test_restore_links_cli(tmp_path):
    runner = CliRunner()

    # Create a sample plain markdown file and JSON file
    plain_md = tmp_path / "plain.md"
    plain_md.write_text("I am proficient in Python and JavaScript.")

    links_json = tmp_path / "links.json"
    links_json.write_text(
        json.dumps(
            {
                "Python": "https://www.python.org/",
                "JavaScript": "https://www.javascript.com/",
            }
        )
    )

    output_md = tmp_path / "restored.md"

    # Run the restore command
    result = runner.invoke(cli, ["restore", str(plain_md), str(links_json), str(output_md)])

    assert result.exit_code == 0
    assert (
        output_md.read_text()
        == "I am proficient in [Python](https://www.python.org/) and [JavaScript](https://www.javascript.com/)."
    )
