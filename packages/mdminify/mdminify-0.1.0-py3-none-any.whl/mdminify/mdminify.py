from __future__ import annotations

import json
import re


# Function to remove hyperlinks from markdown text and store text-to-url mappings
def remove_links(markdown_text: str) -> tuple[str, dict[str, str]]:
    """
    Removes markdown links from a string and returns the plain text and a dictionary
    mapping link text to their respective URLs.

    Args:
        markdown_text (str): The input markdown text that may contain links in the form [text](url).

    Returns:
        tuple: A tuple containing:
            - plain_text (str): The markdown text with links removed.
            - links (dict): A dictionary mapping the link text (str) to its corresponding URL (str).

    Example:
        >>> remove_links("I am proficient in [Python](https://www.python.org/).")
        ("I am proficient in Python.", {"Python": "https://www.python.org/"})
    """
    # Regex pattern to find [text](url)
    link_pattern = re.compile(r"\[(.*?)\]\((.*?)\)")
    # Dictionary to store text-to-url mappings
    links: dict[str, str] = {}

    # Function to replace the links and store the mappings
    def replace_link(match: re.Match) -> str:
        text, url = match.groups()
        links[text] = url  # Store the mapping of text -> url
        return text  # Return just the plain text

    # Replace all markdown links with plain text
    plain_text = link_pattern.sub(replace_link, markdown_text)
    return plain_text, links


# Function to reinsert hyperlinks into text based on stored links
def reinsert_links(plain_text: str, links: dict[str, str]) -> str:
    """
    Reinserts markdown links into plain text using a dictionary that maps the link text to URLs.

    Args:
        plain_text (str): The input plain text without links.
        links (dict): A dictionary mapping the link text (str) to its corresponding URL (str).

    Returns:
        str: The text with links reinserted in markdown format.

    Example:
        >>> reinsert_links(
        ...     "I am proficient in Python.", {"Python": "https://www.python.org/"}
        ... )
        "I am proficient in [Python](https://www.python.org/)."
    """
    for text, url in links.items():
        # Replace the plain text with markdown-style link
        plain_text = plain_text.replace(text, f"[{text}]({url})")
    return plain_text


# Function to read markdown from file, remove links, and save plain text and links
def process_markdown_file(input_md_file: str, output_md_file: str, output_json_file: str) -> None:
    """
    Reads a markdown file, removes links, saves the plain text to another file,
    and stores the links in a JSON file.

    Args:
        input_md_file (str): Path to the input markdown file that contains links.
        output_md_file (str): Path to the output markdown file where plain text (without links) will be saved.
        output_json_file (str): Path to the JSON file where extracted links will be stored.

    Example:
        >>> process_markdown_file("input.md", "output.md", "links.json")
        # output.md will contain the plain text, and links.json will store the links in JSON format.
    """
    # Read markdown content from input file
    with open(input_md_file) as file:
        markdown_text = file.read()

    # Remove links from the markdown content
    plain_text, links = remove_links(markdown_text)

    # Save plain text to output markdown file
    with open(output_md_file, "w") as file:
        file.write(plain_text)

    # Save links to a JSON file
    with open(output_json_file, "w") as file:
        json.dump(links, file, indent=4)


# Function to restore links from JSON and plain markdown file, then save the restored markdown
def restore_links_from_json(plain_md_file: str, json_file: str, output_md_file: str) -> None:
    """
    Reads a plain markdown file and a JSON file containing links, then restores the links
    in the markdown file and saves the result.

    Args:
        plain_md_file (str): Path to the plain markdown file (without links).
        json_file (str): Path to the JSON file that contains the links as a dictionary.
        output_md_file (str): Path to the output markdown file where the restored markdown will be saved.

    Example:
        >>> restore_links_from_json("output.md", "links.json", "restored.md")
        # restored.md will contain the markdown text with links restored.
    """
    # Read plain text from markdown file
    with open(plain_md_file) as file:
        plain_text = file.read()

    # Load links from JSON file
    with open(json_file) as file:
        links: dict[str, str] = json.load(file)

    # Reinsert the links into the plain text
    restored_text = reinsert_links(plain_text, links)

    # Save the restored markdown content to output file
    with open(output_md_file, "w") as file:
        file.write(restored_text)
