import click
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea

from peer import Peer
from utils import printText


@click.command()
@click.option('--role' , default='core' , help='role of peer.')
@click.option('--addr' , default='0.0.0.0:8000' , help='self addresss.')
@click.option('--target' , default='0.0.0.0:8000' , help='target addresss.')
@click.option('--name' , default='core' , help='peer name.')
def main(role, addr, target, name): 
    """LibreCisco Test Version"""

    dashboard_text = '==================== Dashboard ====================\n'
    peer_text      = '====================    Peer   ====================\n'

    dashboard_field = TextArea(text=dashboard_text)
    peer_field = TextArea(text=peer_text, height=10)
    input_field = TextArea(height=1, prompt=' > ', style='class:input-field')
    

    addr = addr.split(':')
    services = {
        'peer': Peer(host=addr, name=name, role=role, output_field=[dashboard_field, peer_field]),
        'watch_dog': None
    }
    peer = services['peer']
    watch_dog = services['watch_dog']
    
    peer.start()  

    if (target != '0.0.0.0:8000'):
        peer.sendMessage((target.split(':')[0], target.split(':')[1]), 'join')
    else:
        printText('you are first peer.', output=[dashboard_field, peer_field])

    left_split = HSplit([
        peer_field,
        Window(height=1, char='-', style='class:line'),
        dashboard_field,
        Window(height=1, char='-', style='class:line'),
        input_field
    ])
    #right_split = HSplit([
    #    
    #])

    container = VSplit([left_split])#, right_split])
    kb = KeyBindings()

    @kb.add('c-q')
    def _(event):
        peer.stop()
        event.app.exit()

    @kb.add('c-c')
    def _(event):
        input_field.text = ''

    @kb.add('enter')
    def _(event):
        cmd = input_field.text.split(' ')
        if cmd[0] in services:
            services[cmd[0]].onProcess(cmd[1:])
        elif cmd[0] == 'help':
            helptips = '''
peer [cmd]
    - send [ip:port] [msg]           send a msg to host.
    - broadcast [role/all] [msg]     send a broadcast msg to role.
    - list                           list all peer.
exit
'''
            printText(helptips, output=dashboard_field)
        elif cmd[0] == 'exit':
            peer.stop()
            event.app.exit()
        else:
            printText('command error , input "help" to check the function.', output=dashboard_field)
        input_field.text = ''

    style = Style([
        ('input_field', 'bg:#000000 #ffffff'),
        ('line', '#004400')
    ])

    application = Application(
        layout=Layout(container, focused_element=input_field),
        key_bindings=kb,
        style=style,
        full_screen=True
    )
    application.run()

if __name__ == '__main__' :
    main()
