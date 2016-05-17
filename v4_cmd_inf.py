import cmd
import sys
import shlex
import ipaddr
import readline

from time import sleep
from datetime import datetime

log_file_name = 'cli_cluster_mgmt.log'

class monitor_cli(cmd.Cmd):

    def __init__(self, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)
        self.intro = ' Maple Labs Cluster Management\n'
        self.prompt = '$ '
        self.nodes = ['compute001', 'compute002']
        self.add_node_cargs = ['--name', '--ntype', '--ip', '--username', '--password', '--interval', '--tags']
        self.ntype_ar = ['linux', 'windows', 'vcenter', 'my-sql']
        self.refresh_node_info()

    def refresh_node_info(self):
        self.nodes_dict = {d:{} for d in self.nodes}
        self.all_cmd_dict = {
                              'add':{
                                'node': {
                                        self.add_node_cargs[0]:{
                                        self.add_node_cargs[1]:{
                                        self.add_node_cargs[2]:{
                                        self.add_node_cargs[3]:{
                                        self.add_node_cargs[4]:{
                                        self.add_node_cargs[5]:{
                                        self.add_node_cargs[6]:{
                                        }}}}}}}
                                        },
                                'tags': self.nodes_dict,
                                    },
                              'del':{
                                'node': self.nodes_dict,
                                'tags': self.nodes_dict,
                                    },
                              'start':{
                                'poll': self.nodes_dict,
                                      },
                              'stop':{
                                'poll': self.nodes_dict,
                                      },
                              'set':{
                                'interval': self.nodes_dict,
                                      },
                              'show':{
                                'node': self.nodes_dict,
                                'nodes': {},
                                    },
                            }

    def write_to_log(self):
        with open(log_file_name, 'a') as fp:
            if readline.get_current_history_length():
                fp.write(str(datetime.now()) + '\t' + readline.get_history_item(readline.get_current_history_length()) + '\n')
        
    def common_complete(self, ccmd, text, line, begidx, endidx):
        self.refresh_node_info()
        c_dict = self.all_cmd_dict.get(ccmd, {})
        prev_dict = c_dict
        line_cmds = shlex.split(line)
        org_line_cmds = line_cmds[:]
        #print '\n', ccmd, line_cmds
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
        #print '\n', line_cmds, '\n'
           
        for cmd in line_cmds[:]:
            if ccmd == cmd:continue
            prev_dict = c_dict
            #print '\n', cmd, c_dict, '\n'
            c_dict = c_dict.get(cmd, {})
            #print cmd, c_dict, '\n'
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
        if 'node' in arguments:
            if 'node' == args[0]:
                args = args[1:]
            self.add_node(args)
        elif 'tags' in arguments:
            if 'tags' == args[0]:
                args = args[1:]
            self.add_tags(args)
        else:
            print usage

    def complete_add(self, text, line, begidx, endidx):
        completions = self.common_complete('add', text, line, begidx, endidx)
        if (not text and (line.split()[-1] == '--ntype')):
            completions = [f+' ' for f in self.ntype_ar]
        elif (text and (line.split()[-2] == '--ntype')):
            completions = [f+' ' for f in self.ntype_ar if f.startswith(text)]
        return completions

    def add_node(self, args):
        'Add a Node.\n'
        usage = 'add node <node name> <node type> <ip addr> <username> <password> <interval time> [tag list]\n         Or\n'
        usage += 'add node --name <node name> --ntype <node type> --ip <ip addr> --username <username> --password <password> --interval <interval time> --tags [tag list]'
        #usage = 'Usage: add node ' + ' '.join(map(lambda x:'<'+x.strip('--')+'>', self.add_node_cargs)) + '\n         Or\nadd node ' + ' '.join(map(lambda x:x + ' <'+x.strip('--')+'>', self.add_node_cargs))
        org_args = args[:]
        cargs = [x for x in args if '--' in x]
        args = [x for x in args if '--' not in x]
        missed_args = set(self.add_node_cargs) - set(cargs)
        if org_args and org_args[-1] in 'help':
            print usage
        elif len(args) >= len(self.add_node_cargs) and (not missed_args or len(missed_args) == len(self.add_node_cargs)):
            name, ntype, ip, username, password, interval = args[:6]
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
                ##### Add Node
                if name in self.nodes:
                    print "Node name '%s' Already Exists" % args[0]
                else:
                    self.get_progress_char()
                    self.nodes.append(name)
                    print "Successfully added", args
        else:
            #if len(missed_args) != len(self.add_node_cargs):
            #    print 'Missed arguments: ', list(missed_args), '\n'
            print usage
        self.write_to_log()

    def add_tags(self, args):
        'Add tags.'
        usage = 'Usage: add tags <node_name> [tag list]'
        if args[-1] in 'help':
            print usage
        elif len(args) > 2:
            if args[0] in self.nodes:
                #### addtags
                self.get_progress_char()
                print "Tags '%s' added to %s\'s polling data" % (', '.join(args[1:]), args[0])
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage
        self.write_to_log()

    def do_del(self, arguments):
        'Delete a Node/Tags.\nUsage: del node/tags ..'
        usage = self.do_del.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if 'node' in arguments:
            if 'node' == args[0]:
                args = args[1:]
            self.del_node(args)
        elif 'tags' in arguments:
            if 'tags' == args[0]:
                args = args[1:]
            self.del_tags(args)
        else:
            print usage

    def complete_del(self, text, line, begidx, endidx):
        completions = self.common_complete('del', text, line, begidx, endidx)
        return completions

    def del_node(self, args):
        'Delete a Node.'
        usage = 'Usage: del node <node name>'
        if len(args) == 1:
            if args[-1] in 'help':
                print usage
            elif args[0] in self.nodes:
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
        usage = 'Usage: del tags <node name> [tag list]'
        if len(args) >= 1:
            if args[-1] in 'help':
                print usage
            elif args[0] in self.nodes:
                #### remove_tag
                if args[1:]:
                    self.get_progress_char()
                    print "%s tags removed from %s\'s polling data" % (', '.join(args[1:]), args[0])
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
        if 'monitor' in arguments:
            if 'monitor' == args[0]:
                args = args[1:]
            self.start_monitor(args)
        elif 'poll' in arguments:
            if 'poll' == args[0]:
                args = args[1:]
            self.start_poll(args)
        else:
            print usage

    def complete_start(self, text, line, begidx, endidx):
        completions = self.common_complete('start', text, line, begidx, endidx)
        return completions

    def start_monitor(self, args):
        'Start Monitoring a Node.'
        usage = 'Usage: start monitor <node name>'
        if len(args) == 1:
            if args[-1] in 'help':
                print usage
            elif args[0] in self.nodes:
                self.get_progress_char()
                ##### Start Monitoring Node
                print "Started Monitoring node: '%s'" % args[0]
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage
        self.write_to_log()

    def start_poll(self, args):
        'Start polling a Node.'
        usage = 'Usage: start poll <node name>'
        if len(args) == 1:
            if args[-1] in 'help':
                print usage
            elif args[0] in self.nodes:
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
        if 'monitor' in arguments:
            if 'monitor' == args[0]:
                args = args[1:]
            self.stop_monitor(args)
        elif 'poll' in arguments:
            if 'poll' == args[0]:
                args = args[1:]
            self.stop_poll(args)
        else:
            print usage

    def complete_stop(self, text, line, begidx, endidx):
        completions = self.common_complete('stop', text, line, begidx, endidx)
        return completions

    def stop_monitor(self, args):
        'Stop Monitoring a Node.'
        usage = 'Usage: stop monitor <node_name>'
        if len(args) == 1:
            if args[-1] in 'help':
                print usage
            elif args[0] in self.nodes:
                ##### Stop Monitoring Node
                self.get_progress_char()
                print "Stopped Monitoring node: '%s'" % args[0]
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage
        self.write_to_log()

    def stop_poll(self, args):
        'Stop Polling a Node.'
        usage = 'Usage: stop poll <node_name>'
        if len(args) == 1:
            if args[-1] in 'help':
                print usage
            elif args[0] in self.nodes:
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
        if 'interval' in arguments:
            if 'interval' == args[0]:
                args = args[1:]
            self.change_interval(args)
        else:
            print usage

    def complete_set(self, text, line, begidx, endidx):
        completions = self.common_complete('set', text, line, begidx, endidx)
        return completions

    def change_interval(self, args):
        'Set Polling Interval.'
        usage = 'Usage: set interval <node_name> <interval>'
        interval = 0
        if len(args) == 2:
            if args[-1] in 'help':
                print usage
            elif args[0] in self.nodes:
                try:
                    interval = int(args[1])
                except:
                    print 'Invalid Interval value'
                if interval:
                    ##### change_interval
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
        if 'nodes' in arguments:
            if 'nodes' == args[0]:
                args = args[1:]
            self.show_nodes(args)
        elif 'node' in arguments:
            if 'node' == args[0]:
                args = args[1:]
            self.show_node(args)
        else:
            print usage

    def complete_show(self, text, line, begidx, endidx):
        completions = self.common_complete('show', text, line, begidx, endidx)
        return completions

    def show_node(self, args):
        'Show Node Details.'
        usage = 'Usage: show node <node_name>'
        if len(args) == 1:
            if args[-1] in 'help':
                print usage
            elif args[0] in self.nodes:
                #### Node Details
                self.get_progress_char()
                print "Node: %s\'s details" % args[0]
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
            #### Node Details
            self.get_progress_char()
            print "All Nodes: %s" % self.nodes
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
