import click
from prompt_toolkit.widgets import TextArea
from LibreCisco import LibreCisco
from LibreCisco.local_monitor import LocalMonitor
from LibreCisco.utils.logging import getLogger


@click.command()
@click.option('--role', default='core', help='role of peer.')
@click.option('--addr', default='127.0.0.1:8000', help='self addresss.')
@click.option('--target', default=None, help='target addresss.')
@click.option('--name', default='core', help='peer name.')
@click.option('--cert', default='data/libre_cisco.pem', help='Cert path.')
@click.option('--auto-start', type=bool, default=True)
@click.option('--auto-join-net', type=bool, default=False)
@click.option('--local-monitor', type=bool, default=False)
def main(role, addr, target, name, cert, auto_start, auto_join_net,
         local_monitor):

    dashboard_text = '==================== Dashboard ====================\n'
    peer_text = '====================    Peer   ====================\n'

    dashboard_field = TextArea(text=dashboard_text)
    peer_field = TextArea(text=peer_text)

    logger = getLogger(add_monitor=local_monitor)
    libreCisco = LibreCisco(role=role, addr=addr, name=name,
                            cert=cert, dashboard_field=dashboard_field,
                            peer_field=peer_field)

    if local_monitor is True:
        local_monitor = LocalMonitor(libreCisco)
        libreCisco.services['local_monitor'] = local_monitor

    if auto_start is True:
        libreCisco.start()
    if auto_join_net is True and target is not None:
        if auto_start is False:
            libreCisco.start()
        libreCisco.onProcess(['peer', 'join', target])


main()
