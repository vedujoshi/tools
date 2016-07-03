Some useful tools
==========================================================
api-inspect.py:
    Helper script to do the commonly used Contrail API Server curl 
    requests

Example:
    python api-inspect.py vms
    python api-inspect.py virtual-machine-interface
    python api-inspect.py vmi/<UUID>
    python api-inspect.py virtual-machine-interface/<UUID>
    python api-inspect.py --debug vmi/<UUID>
    python api-inspect.py --oper DELETE vmi/<UUID>
    python api-inspect.py --api_server_ip 127.0.0.1 --api_server_port 8082 --token <TOKEN> vmi/<UUID>
    python api-inspect.py --api_server_ip 127.0.0.1 --api_server_port 8082 --token <TOKEN> vmi/<UUID>
    python api-inspect.py -c <conf_file> vmis --no_print_json
    python api-inspect.py -h
==========================================================
