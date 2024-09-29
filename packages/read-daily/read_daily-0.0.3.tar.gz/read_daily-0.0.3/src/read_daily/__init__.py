from pathlib import Path

import click
from click import STRING, secho

APP_DATA_DIR = Path.home().joinpath('.local', 'rdf')
APP_DATA_DIR.mkdir(exist_ok=True, parents=True)

APP_SOURCE_FILE = 'sources.txt'
APP_DATA_DIR.joinpath(APP_SOURCE_FILE).touch()


@click.group()
@click.pass_context
@click.version_option()
def cli(ctx):
    pass


@click.command()
@click.option('--limit', type=int, help='Limit source list results to this number')
@click.option('--all_items', required=False, is_flag=True, default=True, help='Show all source list')
def sources(limit, all_items):
    """Show and setting news/information source list."""
    with open(APP_DATA_DIR.joinpath(APP_SOURCE_FILE), mode='r', encoding='utf-8') as f:
        source_list = f.read().splitlines()

    total = len(source_list)
    if limit:
        source_list = source_list[:limit]
    click.secho(f'There are {len(source_list)} source item, total: {total}.', bold=True, bg='blue', fg='white')
    for index, source_item in enumerate(source_list, start=1):
        click.secho(f'{index} - {source_item}')


@click.command()
@click.option('--src', required=True, type=STRING, help='Which source do you want to read')
def read(src):
    """Read a source information."""
    if src == 'bilibili':
        from .spider import bilibili
        scrap_res = bilibili.scrap()
        res = bilibili.parse(scrap_res)
        for index, item in enumerate(res, start=1):
            title = item['title']
            publish_datetime = item['publish_datetime']
            description = item['description'].replace('\n', ' ')
            item_msg = f'[index]: {index} [title]: {title} [publish_datetime]: {publish_datetime}'

            secho(item_msg, bg='blue', fg='white')
            secho(description)
            secho(f'url: {item["url"]}')
            secho('\n')
    else:
        secho(f'Unknown source: {src}', fg='red')


cli.add_command(sources)
cli.add_command(read)
