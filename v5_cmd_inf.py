import cmd
import sys
import shlex
import ipaddr
import readline

from time import sleep
from datetime import datetime

import requests
import json

log_file_name = 'cli_cluster_mgmt.log'

add_node_cargs = ['--name_name', '--node_type', '--ip', '--username', '--password', '--interval', '--tags']
add_tags_cargs = ['--node_name', '--tags']
set_interval_cargs = ['--node_name', '--interval']
node_name_cargs = ['--node_name']
node_type_ar = ['linux', 'windows', 'vcenter', 'my-sql']

ip_addr = '10.81.0.28'
port_no = '8000'
http_link = 'http://%s:%s' % (ip_addr, port_no)

nodes_info_url = http_link+ '/api/node'

def get_http_response(url, data='{}'):  
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    #data = payload = {'username': 'bob', 'email': 'bob@bob.com'}
    response = requests.get(url, data=data, headers=headers)
    rest_data_dict = {}
    if response.ok:
        rest_data_dict = json.loads(response.content)
    else:
        #response.raise_for_status()
        print 'Error Connecting %s Error Code %s ' % (url, str(response.status_code))
    return rest_data_dict

class monitor_cli(cmd.Cmd):

    def __init__(self, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)
        self.intro = '#### Maple Labs Cluster Management ####\n'
        self.prompt = '$ '
        self.refresh_node_info()
        self.node_info_dict = {}
	self.nodes = []
        self.get_nodes_info()

    def refresh_node_info(self):
        self.all_cmd_dict = {
                            'add':{
                                'node': {
                                        add_node_cargs[0]:{
                                        add_node_cargs[1]:{
                                        add_node_cargs[2]:{
                                        add_node_cargs[3]:{
                                        add_node_cargs[4]:{
                                        add_node_cargs[5]:{
                                        add_node_cargs[6]:{
                                        }}}}}}}
                                        },
                                'tags': {
					add_tags_cargs[0]:{
					add_tags_cargs[1]:{
					}}
					},
                                    },
                            'del':{
                                'node': {
					node_name_cargs[0]:{},
					},
                                'tags': {
					add_tags_cargs[0]:{
					add_tags_cargs[1]:{
					}}
					},
                                    },
                            'start':{
                                'poll': {
					node_name_cargs[0]:{},
					},
                                      },
                            'stop':{
                                'poll': {
					node_name_cargs[0]:{},
					},
                                      },
                            'set':{
                                'interval': {
					set_interval_cargs[0]:{
					set_interval_cargs[1]:{
					}}
					},
                                    },
                            'show':{
                                'node': {
					node_name_cargs[0]:{},
					},
                                'nodes': {},
                                    },
                            }
        return

    def get_nodes_info(self):
        res_ar = get_http_response(nodes_info_url)
        if res_ar:
             for res_dict in res_ar:
                 name = res_dict.get('name', '')
                 self.node_info_dict[name] = res_dict
        self.nodes = self.node_info_dict.keys()

    def display_node_info(self, node_name=''):
        hlines = ['Name', 'Type', 'IP Address', 'User Name', 'Interval', 'State', 'Port', 'ID', 'Tags']
        disp_dict = {}
        if not node_name:
            res_ar = get_http_response(nodes_info_url)
	    #[u'info', u'updated', u'name', u'tags', u'interval', u'created', u'state', u'type', u'id']
            #{u'username': u'user', u'password': u'password', u'ip_addr': u'10.11.0.123', u'port': 442}
            if res_ar:
                 for res_dict in res_ar:
                     name = res_dict.get('name', '')
                     tags = ', '.join(map(str, res_dict.get('tags', [])))
                     interval = res_dict.get('interval', '')
                     state = res_dict.get('state', '')
                     ntype = res_dict.get('type', '')
                     nid = res_dict.get('id', '')
                
                     username = res_dict.get('info', {}).get('username', '')
                     password = res_dict.get('info', {}).get('password', '')
                     p_addr = res_dict.get('info', {}).get('ip_addr', '')
                     port = res_dict.get('info', {}).get('port', '')
                     dres_ar = map(str, [name, ntype, p_addr, username, interval, state, port, nid, tags])
                     self.node_info_dict[name] = dres_ar
            disp_dict = self.node_info_dict
        else:
            disp_dict = self.node_info_dict[node_name]

        self.nodes = self.node_info_dict.keys()

        if disp_dict:
            line_fstr = '\n' + '_ ' * 55 + '\n'
            print 
            for i,hl in enumerate(hlines[:-1]):
                print '{:15}|'.format(hl),
            print '{:15}'.format(hlines[-1]),
            print line_fstr

            for name, vlines in disp_dict.items():
                for i, el in enumerate(vlines[:-1]):
                    print '{:15}|'.format(el),
                print '{:15}'.format(vlines[-1]),
                print 
            print line_fstr
            print 
        else:
            print 'No Nodes Found'

    def write_to_log(self):
        with open(log_file_name, 'a') as fp:
            if readline.get_current_history_length():
                fp.write(str(datetime.now()) + '\t' + readline.get_history_item(readline.get_current_history_length()) + '\n')
        
    def common_complete(self, text, line, begidx, endidx):
	line_cmds = shlex.split(line)
        ccmd = line_cmds[0]
        if (len(line_cmds) > 2):
	    if ('--' in line_cmds[-1]) and ('--' in line_cmds[-2]):
                return []

        self.refresh_node_info()
        c_dict = self.all_cmd_dict.get(ccmd, {})
        prev_dict = c_dict
        org_line_cmds = line_cmds[:]
        if '--' in line:
            new_line_cmds = []
            st_kw = 0
            for cmd in line_cmds:
                if ('--' not in cmd) and (not st_kw):
                    new_line_cmds.append(cmd)
                if '--' in cmd:
                    st_kw = 1
                    new_line_cmds.append(cmd)
            line_cmds = new_line_cmds 
           
        for cmd in line_cmds[:]:
            if ccmd == cmd:continue
            prev_dict = c_dict
            c_dict = c_dict.get(cmd, {})
            if not c_dict:
                break

        prev_cmds = prev_dict.keys()
        if not text:
            if (line_cmds[-1] in prev_cmds) and c_dict:
                completions = [f for f in c_dict.keys() if f.startswith(text)]
            else:
                if (line_cmds[-1] in prev_cmds) or ('--' in org_line_cmds[-1]):
                    completions = []
                else:
                    completions = prev_cmds
        elif line_cmds[-2] in prev_cmds:
            completions = [f for f in c_dict.keys() if f.startswith(text)]
        else:
            completions = [f for f in prev_cmds if f.startswith(text)]

        if '--' in org_line_cmds[-1]:
             completions = [x for x in completions if '--' not in x]

        if (not text and (line.split()[-1] == '--node_name')):
            completions = self.nodes
        elif (text and (line.split()[-2] == '--node_name')):
            completions = [f for f in self.nodes if f.startswith(text)]

        completions = [x+' ' for x in completions]
        return completions

    def precmd(self, line):
        newline=line.strip()
        is_cmt=newline.startswith('#')
        if is_cmt:
            return ('')
        return (line + ' ')

    def is_valid_ip(self, ip_add):
        try: 
            val_ip = ipaddr.IPAddress(ip_add)
        except ValueError:
            val_ip = 0
        return val_ip

    def do_add(self, arguments):
        'Add a Node/Tags.\nUsage: add node/tags ..'
        usage = self.do_add.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if not args:
            print usage
            return
        if 'tags' == args[0]:
            self.add_tags(args[1:])
        elif 'node' == args[0]:
            self.add_node(args[1:])
        else:
            print usage

    def complete_add(self, text, line, begidx, endidx):
        completions = self.common_complete(text, line, begidx, endidx)
        if (not text and (line.split()[-1] == '--node_type')):
            completions = [f+' ' for f in node_type_ar]
        elif (text and (line.split()[-2] == '--node_type')):
            completions = [f+' ' for f in node_type_ar if f.startswith(text)]
        return completions

    def add_node(self, args):
        'Add a Node.\n'
        usage = 'add node <node name> <node type> <ip addr> <username> <password> <interval time> [tag list]\n\tOr\n'
        usage += 'add node --name_name <node name> --node_type <node type> --ip <ip addr> --username <username> --password <password> --interval <interval time> --tags [tag list]'
        usage += '\nNote: --node_type <node type> options: ' + ', '.join(node_type_ar)
        #usage = 'Usage: add node ' + ' '.join(map(lambda x:'<'+x.strip('--')+'>', add_node_cargs)) + '\n\tOr\nadd node ' + ' '.join(map(lambda x:x + ' <'+x.strip('--')+'>', add_node_cargs))
        org_args = args[:]
        cargs = [x for x in args if '--' in x]
        args = [x for x in args if '--' not in x]
        missed_args = set(add_node_cargs) - set(cargs)
        if org_args and org_args[-1] in 'help':
            print usage
        elif len(args) >= len(add_node_cargs) and (not missed_args or len(missed_args) == len(add_node_cargs)):
            name, node_type, ip, username, password, interval = args[:6]
            tags = args[6:]
            print 'tags ', tags 

            v_f = 1
            try:
                interval = int(interval)
            except:
                v_f = 0
                print 'Invalid Interval value'
            if not self.is_valid_ip(ip):
                v_f  = 0
                print "Invalid Ip Address\n" + usage

            if v_f:
                if name in self.nodes:
                    print "Node name '%s' Already Exists" % args[0]
                else:
                    self.get_progress_char()
                    node_str = '\t'.join(args[:6]) + '\t' + ' '.join(tags) + '\n'
                    print "Successfully added", args
        else:
            #if len(missed_args) != len(add_node_cargs):
            #    print 'Missed arguments: ', list(missed_args), '\n'
            print usage
        self.write_to_log()

    def add_tags(self, args):
        'Add tags.'
        usage = 'Usage: add tags <node name> [tag list]\n\tOr\n'
        usage += 'Usage: add tags --node_name <node name> --tags [tag list]'
        org_args = args[:]
        cargs = [x for x in args if '--' in x]
        args = [x for x in args if '--' not in x]
        missed_args = set(add_tags_cargs) - set(cargs)
        if org_args and org_args[-1] in 'help':
            print usage
        elif len(args) >= len(add_tags_cargs) and (not missed_args or len(missed_args) == len(add_tags_cargs)):
            tags = args[1:]
            if args[0] in self.nodes:
                #### addtags
                self.get_progress_char()
                print "Tags '%s' added to %s\'s polling data" % (', '.join(tags), args[0])
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage
        self.write_to_log()

    def do_del(self, arguments):
        'Delete a Node/Tags.\nUsage: del node/tags ..'
        usage = self.do_del.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if not args:
            print usage
            return
        if 'node' == args[0]:
            self.del_node(args[1:])
        elif 'tags' == args[0]:
            self.del_tags(args[1:])
        else:
            print usage

    def complete_del(self, text, line, begidx, endidx):
        completions = self.common_complete(text, line, begidx, endidx)
        return completions

    def del_node(self, args):
        'Delete a Node.'
        usage = 'Usage: del node <node name>\n\tOr\n'
        usage += 'Usage: del node --node_name <node name>'

        org_args = args[:]
        cargs = [x for x in args if '--' in x]
        args = [x for x in args if '--' not in x]
        missed_args = set(node_name_cargs) - set(cargs)
        if org_args and org_args[-1] in 'help':
            print usage
        elif len(args) >= len(node_name_cargs) and (not missed_args or len(missed_args) == len(node_name_cargs)):
            if args[0] in self.nodes:
                ##### Del Node
                ind = self.nodes.index(args[0])
                try:
                    del self.nodes[ind]
                except:
                    pass
                self.get_progress_char()
                print "Successfully Deleted", args
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage
        self.write_to_log()

    def del_tags(self, args):
        'Remove tags.'
        usage = 'Usage: del tags <node name> [tag list]\n\tOr\n'
        usage += 'Usage: del tags --node_name <node name> --tags [tag list]'

        org_args = args[:]
        cargs = [x for x in args if '--' in x]
        args = [x for x in args if '--' not in x]
        missed_args = set(add_tags_cargs) - set(cargs)
        if org_args and org_args[-1] in 'help':
            print usage
        elif len(args) >= len(add_tags_cargs) and (not missed_args or len(missed_args) == len(add_tags_cargs)):
            tags = args[1:]
            if args[0] in self.nodes:
                #### remove_tag
                if tags:
                    self.get_progress_char()
                    print "Tags '%s' removed from %s\'s polling data" % (', '.join(tags), args[0])
                else:
                    print usage
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage
        self.write_to_log()

    def do_start(self, arguments):
        'Start Poll.\nUsage: start poll ..'
        usage = self.do_start.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if not args:
            print usage
            return 
        if 'poll' == args[0]:
            self.start_poll(args[1:])
        else:
            print usage

    def complete_start(self, text, line, begidx, endidx):
        completions = self.common_complete(text, line, begidx, endidx)
        return completions

    def start_poll(self, args):
        'Start polling a Node.'
        usage = 'Usage: start poll <node name>\n\tOr\n'
        usage = 'Usage: start poll --node_name <node name>'

        org_args = args[:]
        cargs = [x for x in args if '--' in x]
        args = [x for x in args if '--' not in x]
        missed_args = set(node_name_cargs) - set(cargs)
        if org_args and org_args[-1] in 'help':
            print usage
        elif len(args) >= len(node_name_cargs) and (not missed_args or len(missed_args) == len(node_name_cargs)):
            if args[0] in self.nodes:
                self.get_progress_char()
                ##### Start Polling Node
                print "Started Polling node: '%s'" % args[0]
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage
        self.write_to_log()

    def do_stop(self, arguments):
        'Stop Polling.\nUsage: stop poll ..'
        usage = self.do_start.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if not args:
            print usage
            return
        if 'poll' == args[0]:
            self.stop_poll(args[1:])
        else:
            print usage

    def complete_stop(self, text, line, begidx, endidx):
        completions = self.common_complete(text, line, begidx, endidx)
        return completions

    def stop_poll(self, args):
        'Stop Polling a Node.'
        usage = 'Usage: stop poll <node name>\n\tOr\n'
        usage += 'Usage: stop poll <node name>'

        org_args = args[:]
        cargs = [x for x in args if '--' in x]
        args = [x for x in args if '--' not in x]
        missed_args = set(node_name_cargs) - set(cargs)
        if org_args and org_args[-1] in 'help':
            print usage
        elif len(args) >= len(node_name_cargs) and (not missed_args or len(missed_args) == len(node_name_cargs)):
            if args[0] in self.nodes:
                ##### Stop Monitoring Node
                self.get_progress_char()
                print "Stopped Polling node: '%s'" % args[0]
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage
        self.write_to_log()

    def do_set(self, arguments):
        'Set Interval.\nUsage: set interval ...'
        usage = self.do_set.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if not args:
            print usage
            return
        if 'interval' == args[0]:
            self.set_interval(args[1:])
        else:
            print usage

    def complete_set(self, text, line, begidx, endidx):
        completions = self.common_complete(text, line, begidx, endidx)
        return completions

    def set_interval(self, args):
        'Set Polling Interval.'
        usage = 'Usage: set interval <node name> <interval>\n\tOr\n'
        usage += 'Usage: set interval --node_name  <node name> <interval>'

        org_args = args[:]
        cargs = [x for x in args if '--' in x]
        args = [x for x in args if '--' not in x]
        missed_args = set(set_interval_cargs) - set(cargs)
        interval = 0
        if org_args and org_args[-1] in 'help':
            print usage
        elif len(args) >= len(set_interval_cargs) and (not missed_args or len(missed_args) == len(set_interval_cargs)):
            tags = args[1:]
            if args[0] in self.nodes:
                try:
                    interval = int(args[1])
                except:
                    print 'Invalid Interval value'
                if interval:
                    ##### set interval
                    self.get_progress_char()
                    print "%s\'s Interval Changed to %s seconds" % (args[0], args[1])
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage
        self.write_to_log()

    def do_show(self, arguments):
        'Show Details Nodes/Node.\nUsage: show nodes/node'
        usage = self.do_show.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if not args:
            print usage
            return
        if 'nodes' == args[0]:
            self.show_nodes(args[1:])
        elif 'node' == args[0]:
            self.show_node(args[1:])
        else:
            print usage

    def complete_show(self, text, line, begidx, endidx):
        completions = self.common_complete(text, line, begidx, endidx)
        return completions

    def show_node(self, args):
        'Show Node Details.'
        usage = 'Usage: show node <node name>\n\tOr\n'
        usage += 'Usage: show node--node_name  <node name>'

        org_args = args[:]
        cargs = [x for x in args if '--' in x]
        args = [x for x in args if '--' not in x]
        missed_args = set(node_name_cargs) - set(cargs)
        if org_args and org_args[-1] in 'help':
            print usage
        elif len(args) >= len(node_name_cargs) and (not missed_args or len(missed_args) == len(node_name_cargs)):
            if args[0] in self.nodes:
                self.display_node_info(args[0])
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage
        self.write_to_log()

    def show_nodes(self, args):
        'Show Nodes Details.'
        usage = 'Usage: show nodes'
        if args and args[-1] in 'help':
             print usage
        else:
            self.display_node_info()
        self.write_to_log()

    def do_EOF(self, line):
        return True

    def emptyline(self):
        pass

    def get_progress_char(self):
        i = 0
        while i < 2:
           for c in '\-/|':
               sys.stdout.write('\t' + c + '\r')
               sys.stdout.flush()
               sleep(0.2)
           i += 1

if __name__ == '__main__':
    monitor_cli().cmdloop()
