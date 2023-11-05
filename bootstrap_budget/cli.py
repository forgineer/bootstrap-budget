import click


@click.command('bootstrap-init')
@click.option('-db', default='sqlite', help='Initialize bootstrap-budget application.')
@click.option('-admin-passwd', default='admin', help='Set admin password.')
def bootstrap_init(db, admin_passwd):
    click.echo('Bootstrap has been initialized.')


if __name__ == '__main__':
    pass
