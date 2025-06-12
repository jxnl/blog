import os
import asyncio
import yaml
from typing import Generator, Tuple, Dict, Optional
from openai import AsyncOpenAI
import typer
from rich.console import Console
from rich.progress import Progress
import hashlib

console = Console()


def traverse_docs(
    root_dir: str = "docs",
) -> Generator[Tuple[str, str, str], None, None]:
    """
    Recursively traverse the docs folder and yield the path, content, and content hash of each file.

    Args:
        root_dir (str): The root directory to start traversing from. Defaults to 'docs'.

    Yields:
        Tuple[str, str, str]: A tuple containing the relative path from 'docs', the file content, and the content hash.
    """
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):  # Assuming we're only interested in Markdown files
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_dir)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                content_hash = hashlib.md5(content.encode()).hexdigest()
                yield relative_path, content, content_hash


async def summarize_content(client: AsyncOpenAI, path: str, content: str) -> str:
    """
    Summarize the content of a file.

    Args:
        client (AsyncOpenAI): The AsyncOpenAI client.
        path (str): The path of the file.
        content (str): The content of the file.

    Returns:
        str: A summary of the content.
    """
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {"role": "user", "content": content},
                {
                    "role": "user",
                    "content": "Please summarize the content in a few sentences so they can be used for SEO. Include core ideas, objectives, and important details and key points and key words",
                },
            ],
            max_tokens=4000,
        )
        return response.choices[0].message.content
    except Exception as e:
        console.print(f"[bold red]Error summarizing {path}: {str(e)}[/bold red]")
        return ""


async def generate_sitemap(
    root_dir: str, output_file: str, api_key: Optional[str] = None
) -> None:
    """
    Generate a sitemap from the given root directory.

    Args:
        root_dir (str): The root directory to start traversing from.
        output_file (str): The output file to save the sitemap.
        api_key (Optional[str]): The OpenAI API key. If not provided, it will be read from the OPENAI_API_KEY environment variable.
    """
    client = AsyncOpenAI(api_key=api_key)

    # Load existing sitemap if it exists
    existing_sitemap: Dict[str, Dict[str, str]] = {}
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as sitemap_file:
            existing_sitemap = yaml.safe_load(sitemap_file) or {}
        console.print(f"[blue]Loaded existing sitemap with {len(existing_sitemap)} entries[/blue]")
    else:
        console.print("[yellow]No existing sitemap found, will generate all summaries[/yellow]")

    sitemap_data: Dict[str, Dict[str, str]] = {}
    cached_count = 0
    generated_count = 0

    async def process_file(
        path: str, content: str, content_hash: str
    ) -> Tuple[str, Dict[str, str], bool]:
        if (
            path in existing_sitemap
            and existing_sitemap[path].get("hash") == content_hash
        ):
            return path, existing_sitemap[path], True  # True means cached
        summary = await summarize_content(client, path, content)
        return path, {"summary": summary, "hash": content_hash}, False  # False means generated

    files_to_process = list(traverse_docs(root_dir))
    console.print(f"[green]Found {len(files_to_process)} markdown files to process[/green]")

    with Progress() as progress:
        task = progress.add_task(
            "[green]Processing files...", total=len(files_to_process)
        )
        tasks = [
            process_file(path, content, content_hash)
            for path, content, content_hash in files_to_process
        ]
        results = await asyncio.gather(*tasks)
        for path, data, was_cached in results:
            if was_cached:
                cached_count += 1
            else:
                generated_count += 1
                console.print(f"[cyan]Generated new summary for: {path}[/cyan]")
            sitemap_data[path] = data
            progress.update(task, advance=1)

    with open(output_file, "w", encoding="utf-8") as sitemap_file:
        yaml.dump(sitemap_data, sitemap_file, default_flow_style=False)

    console.print(
        f"[bold green]Sitemap generated successfully![/bold green]"
    )
    console.print(
        f"[blue]📊 Summary: {cached_count} cached, {generated_count} newly generated[/blue]"
    )
    console.print(
        f"[green]💾 Saved to {output_file}[/green]"
    )


app = typer.Typer()


@app.command()
def main(
    root_dir: str = typer.Option("docs", help="Root directory to traverse"),
    output_file: str = typer.Option("sitemap.yaml", help="Output file for the sitemap"),
    api_key: Optional[str] = typer.Option(None, help="OpenAI API key"),
):
    """
    Generate a sitemap from the given root directory.
    """
    asyncio.run(generate_sitemap(root_dir, output_file, api_key))


if __name__ == "__main__":
    app()
