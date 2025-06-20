#!/usr/bin/env python3
"""
CLI tool to create Dub shortlinks for a given URL using Typer.
Usage:
    python scripts/shortlinks.py create <url> [--title "Title"] [--desc "Description"] [--tags tag1,tag2] [--external-id id]

Requires DUB_API_KEY environment variable.
"""
import os
import sys
import dub
import typer
from typing import Optional

app = typer.Typer(help="Create Dub shortlinks for URLs.")

@app.command()
def create(
    url: str = typer.Argument(..., help="The URL to shorten."),
    title: Optional[str] = typer.Option(None, help="Title for the shortlink."),
    desc: Optional[str] = typer.Option(None, help="Description for the shortlink."),
    tags: Optional[str] = typer.Option(None, help="Comma-separated tags."),
    external_id: Optional[str] = typer.Option(None, help="External ID for the link."),
    blog_tag: Optional[str] = typer.Option(None, help="Blog tag to associate with this shortlink."),
):
    """Create a Dub shortlink for a given URL."""
    api_key = os.environ.get("DUB_API_KEY")
    if not api_key:
        typer.secho("❌ Error: DUB_API_KEY environment variable not set.", fg=typer.colors.RED)
        raise typer.Exit(1)

    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    if blog_tag:
        tag_list.append(blog_tag)

    client = dub.Dub(token=api_key)

    try:
        res = client.links.create(request={
            "url": url,
            "title": title,
            "description": desc,
            "tags": tag_list if tag_list else None,
            "external_id": external_id,
        })
        typer.secho(f"✅ Shortlink created: {res.short_link}", fg=typer.colors.GREEN)
        typer.echo(f"  Original: {url}")
        typer.echo(f"  Title: {res.title}")
        typer.echo(f"  Description: {res.description}")
        typer.echo(f"  Tags: {res.tags}")
        typer.echo(f"  External ID: {res.external_id}")
        typer.echo(f"  Link ID: {res.id}")
    except Exception as e:
        typer.secho(f"❌ Failed to create shortlink: {e}", fg=typer.colors.RED)
        raise typer.Exit(2)

if __name__ == "__main__":
    app() 