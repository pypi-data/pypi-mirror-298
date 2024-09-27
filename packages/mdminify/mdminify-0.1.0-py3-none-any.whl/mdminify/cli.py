import click

from mdminify.mdminify import process_markdown_file, restore_links_from_json


@click.group()
def cli():
    """CLI tool to remove and restore markdown links."""


@click.command()
@click.argument("input_md_file", type=click.Path(exists=True))
@click.argument("output_md_file", type=click.Path())
@click.argument("output_json_file", type=click.Path())
def remove(input_md_file, output_md_file, output_json_file):
    """
    Removes markdown links from the input file and saves the plain text (without links)
    to the output markdown file, while storing the extracted links in a JSON file.

    Args:
        input_md_file (str): Path to the markdown file that contains links.
        output_md_file (str): Path where the processed markdown (without links) will be saved.
        output_json_file (str): Path where the extracted links (as JSON) will be stored.

    Side Effects:
        - Creates or overwrites the output markdown file with the plain text (links removed).
        - Creates or overwrites the JSON file with the extracted links.

    Example:
        $ mdminify remove input.md output.md links.json

    This will process `input.md`, save the plain text (without links) to `output.md`,
    and store the extracted links in `links.json`.
    """
    process_markdown_file(input_md_file, output_md_file, output_json_file)
    click.echo(f"Processed markdown saved to {output_md_file}, links saved to {output_json_file}")


@click.command()
@click.argument("plain_md_file", type=click.Path(exists=True))
@click.argument("json_file", type=click.Path(exists=True))
@click.argument("output_md_file", type=click.Path())
def restore(plain_md_file, json_file, output_md_file):
    """
    Restores markdown links in the plain markdown file using the stored links
    from the JSON file, and saves the result to a new markdown file.

    Args:
        plain_md_file (str): Path to the plain markdown file (without links).
        json_file (str): Path to the JSON file that contains the extracted links.
        output_md_file (str): Path where the markdown file with restored links will be saved.

    Side Effects:
        - Creates or overwrites the output markdown file with the restored markdown (links reinserted).

    Example:
        $ mdminify restore output.md links.json restored.md

    This will restore links in `output.md` using `links.json`, and save the result to `restored.md`.
    """
    restore_links_from_json(plain_md_file, json_file, output_md_file)
    click.echo(f"Restored markdown with links saved to {output_md_file}")


# Add the commands to the CLI group
cli.add_command(remove)
cli.add_command(restore)

if __name__ == "__main__":
    cli()
