import click
from prompt_toolkit.widgets import TextArea
from LibreCisco import LibreCisco


@click.command()
@click.option('--role', default='core', help='role of peer.')
@click.option('--addr', default='127.0.0.1:8000', help='self addresss.')
@click.option('--target', default=None, help='target addresss.')
@click.option('--name', default='core', help='peer name.')
@click.option('--cert', default='data/libre_cisco.pem', help='Cert path.')
@click.option('--auto-start', type=bool, default=True)
@click.option('--auto-join-net', type=bool, default=False)
def main(role, addr, target, name, cert, auto_start, auto_join_net):

    dashboard_text = '==================== Dashboard ====================\n'
    peer_text = '====================    Peer   ====================\n'

    dashboard_field = TextArea(text=dashboard_text)
    peer_field = TextArea(text=peer_text)
    libreCisco = LibreCisco(role=role, addr=addr, name=name,
                            cert=cert, dashboard_field=dashboard_field,
                            peer_field=peer_field)

    if auto_start is True:
        libreCisco.start()
    if auto_join_net is True and target is not None:
        if auto_start is False:
            libreCisco.start()
        libreCisco.onProcess(['peer', 'join', target])


main()
