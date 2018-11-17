from LibreCisco import main
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('address', help='Service\'s host address.')
parser.add_argument('-t', '--target', default='127.0.0.1:8000',
                    help='A peer address in Net.', dest='target')
parser.add_argument('-c', '--cert', default='data/libre_cisco.pem',
                    help='Cert file path.', dest='cert')
parser.add_argument('-as', '--auto-start', action='store_true',
                    default=False, help='Auto start whole service.')
parser.add_argument('-ajn', '--auto-join-net', action='store_true',
                    default=False, help='Auto join a with Net address')
parser.add_argument('-lm', '--local-monitor', action='store_true',
                    default=False, help='Allow local monitor conntect')

args, left = parser.parse_known_args()

main(role='core', addr=args.address, target=args.target, name='core',
     cert=args.cert, auto_start=args.auto_start,
     auto_join_net=args.auto_join_net, local_monitor=args.local_monitor)
