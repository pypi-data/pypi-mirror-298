import json

from mdminify import mdminify


# Test removing a single markdown link
def test_remove_single_link():
    markdown_text = "I am proficient in [Python](https://www.python.org/)."
    expected_plain_text = "I am proficient in Python."
    expected_links = {"Python": "https://www.python.org/"}

    plain_text, links = mdminify.remove_links(markdown_text)

    assert plain_text == expected_plain_text, "Plain text did not match expected output"
    assert links == expected_links, "Links dictionary did not match expected output"


# Test removing multiple markdown links
def test_remove_multiple_links():
    markdown_text = (
        "I am proficient in [Python](https://www.python.org/) and [JavaScript](https://www.javascript.com/)."
    )
    expected_plain_text = "I am proficient in Python and JavaScript."
    expected_links = {
        "Python": "https://www.python.org/",
        "JavaScript": "https://www.javascript.com/",
    }

    plain_text, links = mdminify.remove_links(markdown_text)

    assert plain_text == expected_plain_text, "Plain text did not match expected output for multiple links"
    assert links == expected_links, "Links dictionary did not match expected output for multiple links"


# Test reinserting a single markdown link
def test_reinsert_single_link():
    plain_text = "I am proficient in Python."
    links = {"Python": "https://www.python.org/"}
    expected_restored_text = "I am proficient in [Python](https://www.python.org/)."

    restored_text = mdminify.reinsert_links(plain_text, links)

    assert restored_text == expected_restored_text, "Restored text did not match expected output for single link"


# Test reinserting multiple markdown links
def test_reinsert_multiple_links():
    plain_text = "I am proficient in Python and JavaScript."
    links = {
        "Python": "https://www.python.org/",
        "JavaScript": "https://www.javascript.com/",
    }
    expected_restored_text = (
        "I am proficient in [Python](https://www.python.org/) and [JavaScript](https://www.javascript.com/)."
    )

    restored_text = mdminify.reinsert_links(plain_text, links)

    assert restored_text == expected_restored_text, "Restored text did not match expected output for multiple links"


# Test plain text with no markdown links
def test_no_links():
    plain_text = "I am proficient in Python and JavaScript."
    links = {}
    expected_restored_text = plain_text  # No changes expected

    restored_text = mdminify.reinsert_links(plain_text, links)

    assert restored_text == expected_restored_text, "Text with no links should remain unchanged"


# Test process_markdown_file
def test_process_markdown_file(tmp_path):
    # Input markdown text with links
    markdown_content = (
        "I am proficient in [Python](https://www.python.org/) and [JavaScript](https://www.javascript.com/)."
    )

    # Paths for input, output markdown, and output JSON
    input_md = tmp_path / "input.md"
    output_md = tmp_path / "output.md"
    output_json = tmp_path / "links.json"

    # Write the input markdown content to a file
    input_md.write_text(markdown_content)

    # Run the function to process the markdown file
    mdminify.process_markdown_file(input_md, output_md, output_json)

    # Verify that the plain markdown (without links) is written correctly
    expected_plain_text = "I am proficient in Python and JavaScript."
    assert output_md.read_text() == expected_plain_text, "Plain markdown output is incorrect"

    # Verify that the links are saved correctly in the JSON file
    expected_links = {
        "Python": "https://www.python.org/",
        "JavaScript": "https://www.javascript.com/",
    }
    with open(output_json) as f:
        links_data = json.load(f)
    assert links_data == expected_links, "Links JSON output is incorrect"


# Test restore_links_from_json
def test_restore_links_from_json(tmp_path):
    # Input plain markdown text and corresponding JSON with links
    plain_markdown_content = "I am proficient in Python and JavaScript."
    links_data = {
        "Python": "https://www.python.org/",
        "JavaScript": "https://www.javascript.com/",
    }

    # Paths for plain markdown, JSON with links, and restored markdown
    plain_md = tmp_path / "plain.md"
    links_json = tmp_path / "links.json"
    restored_md = tmp_path / "restored.md"

    # Write the plain markdown content to a file
    plain_md.write_text(plain_markdown_content)

    # Write the links data to a JSON file
    with open(links_json, "w") as f:
        json.dump(links_data, f, indent=4)

    # Run the function to restore the links
    mdminify.restore_links_from_json(plain_md, links_json, restored_md)

    # Verify that the restored markdown is correct
    expected_restored_text = (
        "I am proficient in [Python](https://www.python.org/) and [JavaScript](https://www.javascript.com/)."
    )
    assert restored_md.read_text() == expected_restored_text, "Restored markdown output is incorrect"
