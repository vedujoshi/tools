import sys
from subprocess import check_output, PIPE, CalledProcessError, STDOUT, Popen
import argparse
import ConfigParser

oper = sys.argv

mymap = {
'vmi' : 'virtual-machine-interface',
'vmis': 'virtual-machine-interfaces',
'vn' : 'virtual-network',
'vns' : 'virtual-networks',
'vm' : 'virtual-machine',
'vms' : 'virtual-machines',
'sg'    : 'security-group',
'sgs'    : 'security-groups',
'gvc'   : 'global-vrouter-config',
'gvcs'   : 'global-vrouter-configs',
'fc'   : 'forwarding-class',
'fcs'   : 'forwarding-classs',
}

def parse_args():
    '''
    Examples of usage:
    python api-inspect.py vms
    python api-inspect.py virtual-machine-interface
    python api-inspect.py vmi/<UUID>
    python api-inspect.py virtual-machine-interface/<UUID>
    python api-inspect.py --debug vmi/<UUID>
    python api-inspect.py --oper DELETE vmi/<UUID>
    python api-inspect.py --api_server_ip 127.0.0.1 --api_server_port 8082 --token <TOKEN> vmi/<UUID>
    python api-inspect.py --api_server_ip 127.0.0.1 --api_server_port 8082 --token <TOKEN> vmi/<UUID>
    python api-inspect.py -c <conf_file> vmis --no_print_json
    '''

    args_str = ' '.join(sys.argv[1:])
    conf_parser = argparse.ArgumentParser(add_help=False)
    conf_parser.add_argument("-c", "--conf_file",
                             help="Specify config file", metavar="FILE")
    args, remaining_argv = conf_parser.parse_known_args(args_str.split())

    defaults = {
        'api_server_ip': '127.0.0.1',
        'api_server_port': '8095',
        'oper': 'GET',
        'admin_username' : 'admin',
        'admin_password' : 'contrail123',
        'token' : None
    }
    if args.conf_file:
        config = ConfigParser.SafeConfigParser()
        config.read([args.conf_file])
        defaults.update(dict(config.items("DEFAULTS")))

    # Override with CLI options
    # Don't surpress add_help here so it will handle -h
    parser = argparse.ArgumentParser(
        # Inherit options from config_parser
        parents=[conf_parser],
        # print script description with -h/--help
        description=__doc__,
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.set_defaults(**defaults)


    parser.add_argument(
        "--oper", default='GET',
        help="operation GET or DELETE. Default is GET")
    parser.add_argument(
        "--admin_user", help="Name of keystone admin user(admin)")
    parser.add_argument(
        "--admin_password", help="Password of keystone admin user(contrail123)")
    parser.add_argument(
        "--api_server_ip", help="API Server IP(127.0.0.1)")
    parser.add_argument(
        "--api_server_port", help="API Server port(8095)")
    parser.add_argument(
        'obj', help='url suffix, Options: %s' % (mymap))
    parser.add_argument(
        '--debug', action='store_true', default=False, help='Show debug info( False)')
    parser.add_argument(
        '--no_print_json', action='store_true', default=False, help='Show json formatted output( True )')
    parser.add_argument(
        '--token', help='Token from keystone auth (not set by default)')

    args = parser.parse_args(remaining_argv)
    return args
# end parse_pargs

args = parse_args()
obj = args.obj

if '/' in args.obj:
    for k,v in mymap.iteritems():
        if k in args.obj:
            obj = obj.replace(k, mymap[k])
else:
    try:
        obj = mymap[args.obj]
    except KeyError:
        obj = args.obj

cmd = '-u %s:%s -X %s http://%s:%s/%s' % (
            args.admin_username, args.admin_password,
            args.oper, args.api_server_ip,
            args.api_server_port,
            obj)

if args.token:
    cmd = '-H "X-AUTH-TOKEN:%s" %s' % (args.token, cmd)
cmd = 'curl %s ' % (cmd)

if not args.no_print_json and args.oper == 'GET':
    cmd = '%s | python -m json.tool' % (cmd)

if args.debug:
    print 'Command : %s' % (cmd)
    args.no_print_json = True
try:
    output = check_output(cmd, stderr=PIPE, shell=True)
    print output
except CalledProcessError,e:
    print 'Error occured'
    print '%s' % (e.output)
