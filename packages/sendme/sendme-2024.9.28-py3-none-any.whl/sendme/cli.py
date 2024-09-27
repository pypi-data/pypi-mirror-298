import click

@click.command()
@click.option("--base-url", default=None, type=click.STRING, help="Base URL")
@click.option("--username", default=None, type=click.STRING, help="Username")
@click.option("--password", default=None, type=click.STRING, help="Password")
@click.option("--custom-api", default=None, type=click.STRING, help="Custom API")
@click.option("--task-id", default=None, type=click.STRING, help="json报告回填所属任务id")
def cli(base_url, username, password, custom_api, task_id):
    from sendme.main import SendMe
    SendMe(base_url, username, password, custom_api).backfill(task_id)