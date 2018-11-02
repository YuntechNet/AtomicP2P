import click
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.formatted_text import ANSI

from LibreCisco import LibreCisco
from LibreCisco.utils import printText


@click.command()
@click.option('--role', default='core', help='role of peer.')
@click.option('--addr', default='127.0.0.1:8000', help='self addresss.')
@click.option('--target', default=None, help='target addresss.')
@click.option('--name', default='core', help='peer name.')
@click.option('--cert', default='data/libre_cisco.pem', help='Cert path.')
@click.option('--auto-start', default=True)
@click.option('--auto-join-net', default=False)
def main(role, addr, target, name, cert, auto_start, auto_join_net):

    dashboard_text = '==================== Dashboard ====================\n'
    peer_text = '====================    Peer   ====================\n'

    # dashboard_field = FormattedTextControl(ANSI(dashboard_text))
    dashboard_field = TextArea(text=dashboard_text)
    # peer_field = FormattedTextControl(ANSI(peer_text))
    peer_field = TextArea(text=peer_text)
    input_field = TextArea(height=1, prompt=' > ', style='class:input-field')

    libreCisco = LibreCisco(role=role, addr=addr, target=target, name=name,
                            cert=cert, dashboard_field=dashboard_field,
                            peer_field=peer_field, auto_start=auto_start,
                            auto_join_net=auto_join_net)

    left_split = HSplit([
        # Window(height=10, content=peer_field),
        peer_field,
        Window(height=1, char='-', style='class:line'),
        # Window(dashboard_field),
        dashboard_field,
        Window(height=1, char='-', style='class:line'),
        input_field
    ])
    # right_split = HSplit([
    # ])

    container = VSplit([left_split])  # , right_split])
    kb = KeyBindings()

    @kb.add('c-q')
    def _(event):
        libreCisco.stop()
        event.app.exit()

    @kb.add('c-c')
    def _(event):
        input_field.text = ''

    @kb.add('enter')
    def _(event):
        cmd = input_field.text.split(' ')
        if libreCisco.onProcess(cmd) is False:
            if cmd[0] == 'help':
                help_tips = 'peer help            - See peer\'s help\n'\
                            'monitor help        - See monitor\'s help\n'\
                            'exit/stop            - exit the whole program.\n'
                printText(help_tips, output=dashboard_field)
            elif cmd[0] == 'exit' or cmd[0] == 'stop':
                libreCisco.onProcess(['stop'])
                event.app.exit()
            else:
                error_tips = 'command error, input "help" to check function.'
                printText(error_tips, output=dashboard_field)
        input_field.text = ''

    prompt_style = Style([
        ('input_field', 'bg:#000000 #ffffff'),
        ('line', '#004400')
    ])

    application = Application(
        layout=Layout(container, focused_element=input_field),
        key_bindings=kb,
        style=prompt_style,
        full_screen=True
    )
    application.run()


if __name__ == '__main__':
    main()
