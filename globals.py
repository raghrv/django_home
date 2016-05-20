import os

proj_dir = os.getcwd()

log_file_name		= proj_dir + os.path.sep + 'cli_cluster_mgmt.log'
server_ip_port_file 	= proj_dir + os.path.sep + 'server_ip_port.txt'

add_node_cargs 		= ['--node_name', '--node_type', '--ip', '--username', '--password', '--interval', '--tags']
add_tags_cargs 		= ['--node_name', '--tags']
set_interval_cargs 	= ['--node_name', '--interval']
set_server_ip_cargs 	= ['--ip', '--port']
node_name_cargs		= ['--node_name']
node_type_ar		= ['Linux', 'Windows', 'VCenter', 'MS-SQL']

default_ip		= 'localhost'
default_port 		= '8000'
rest_api_url 		= 'http://%s:%s/api/node'
