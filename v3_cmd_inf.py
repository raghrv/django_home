import cmd
import sys
import time
import shlex
import ipaddr

class monitor_cli(cmd.Cmd):
    def __init__(self, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)
        self.intro = ' Maple Labs Cluster Management\n'
        self.prompt = '$ '
        self.nodes = ['compute001', 'compute002']
        self.add_node_cargs = ['--id', '--ip', '--un', '--pw']
        self.refresh_node_info()

    def refresh_node_info(self):
        self.nodes_dict = {d:{} for d in self.nodes}
        self.all_cmd_dict = {
                              'add':{
                                'node': {self.add_node_cargs[0]:{self.add_node_cargs[1]:{self.add_node_cargs[2]:{self.add_node_cargs[2]:{}}}}},
                                'tag': self.nodes_dict,
                                    },
                              'del':{
                                'node': self.nodes_dict,
                                'tag': self.nodes_dict,
                                    },
                              'start':{
                                'monitor': self.nodes_dict,
                                      },
                              'stop':{
                                'monitor': self.nodes_dict,
                                      },
                              'change':{
                                'interval': self.nodes_dict,
                                      },
                              'show':{
                                'node': self.nodes_dict,
                                    },
                            }

    def common_complete(self, ccmd, text, line, begidx, endidx):
        self.refresh_node_info()
        c_dict = self.all_cmd_dict.get(ccmd, {})
        prev_dict = c_dict
        line_cmds = shlex.split(line)
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
        #print [line, text], line_cmds, prev_cmds, c_dict.keys(), '\n'
        if not text:
            if (line_cmds[-1] in prev_cmds) and c_dict:
                completions = [f for f in c_dict.keys() if f.startswith(text)]
            else:
                if line_cmds[-1] in prev_cmds:
                    completions = []
                else:
                    completions = prev_cmds
        elif line_cmds[-2] in prev_cmds:
            completions = [f for f in c_dict.keys() if f.startswith(text)]
        else:
            completions = [f for f in prev_cmds if f.startswith(text)]
        return completions

    def precmd(self, line):
        newline=line.strip()
        is_cmt=newline.startswith('#')
        if is_cmt:
            return ('')
        return (line)

    def is_valid_ip(self, ip_add):
        try: 
            val_ip = ipaddr.IPAddress(ip_add)
        except ValueError:
            val_ip = 0
        return val_ip

    def do_add(self, arguments):
        'Add a Node/Tag.\nUsage: add node/tag ..'
        usage = self.do_add.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if 'node' in arguments:
            if 'node' == args[0]:
                args = args[1:]
            self.add_node(args)
        elif 'tag' in arguments:
            if 'tag' == args[0]:
                args = args[1:]
            self.add_tag(args)
        else:
            print usage

    def complete_add(self, text, line, begidx, endidx):
        completions = self.common_complete('add', text, line, begidx, endidx)
        return completions

    def add_node(self, args):
        'Add a Node.\n'
        usage = 'Usage: add node <node_id> <node_ip> <username> <password> \n         Or\nadd node --id <node_id> --ip <node_ip> --un <username> --pw <password>'
        cargs = [x for x in args if '--' in x]
        args = [x for x in args if '--' not in x]
        missed_args = set(self.add_node_cargs) - set(cargs)
        if len(args) == 4 and not missed_args:
            node_name, node_ip, username, password = args
            if self.is_valid_ip(node_ip):
                ##### Add Node
                if node_name in self.nodes:
                    print "Node ID '%s' Already Exists" % args[0]
                else:
                    self.get_progress_char()
                    self.nodes.append(node_name)
                    print "Successfully added", args
            else:
                print "Invalid Ip Address\n" + usage
        else:
            print 'Missed arguments: ', list(missed_args), '\n'
            print usage

    def add_tag(self, args):
        'Add tag.'
        usage = 'Usage: add tag <node_name> <tag>'
        if len(args) == 2:
            if args[0] in self.nodes:
                #### add_tag
                self.get_progress_char()
                print "Tag '%s' added to %s\'s monitoring data" % (args[1], args[0])
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage

    def do_del(self, arguments):
        'Delete a Node/Tag.\nUsage: del node/tag ..'
        usage = self.do_del.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if 'node' in arguments:
            if 'node' == args[0]:
                args = args[1:]
            self.del_node(args)
        elif 'tag' in arguments:
            if 'tag' == args[0]:
                args = args[1:]
            self.del_tag(args)
        else:
            print usage

    def complete_del(self, text, line, begidx, endidx):
        completions = self.common_complete('del', text, line, begidx, endidx)
        return completions

    def del_node(self, args):
        'Delete a Node.'
        usage = 'Usage: del node <node_name>'
        if len(args) == 1:
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

    def del_tag(self, args):
        'Remove tag.'
        usage = 'Usage: del tag <node_name>'
        if len(args) == 1:
            if args[0] in self.nodes:
                #### remove_tag
                self.get_progress_char()
                print "Tags removed from %s\'s monitoring data" % (args[0])
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage

    def do_start(self, arguments):
        'Start Monitoring.\nUsage: start monitor ..'
        usage = self.do_start.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if 'monitor' in arguments:
            if 'monitor' == args[0]:
                args = args[1:]
            self.start_monitor(args)
        else:
            print usage

    def complete_start(self, text, line, begidx, endidx):
        completions = self.common_complete('start', text, line, begidx, endidx)
        return completions

    def start_monitor(self, args):
        'Start Monitoring a Node.'
        usage = 'Usage: start monitor <node_name>'
        if len(args) == 1:
            if args[0] in self.nodes:
                self.get_progress_char()
                ##### Start Monitoring Node
                print "Started Monitoring node: '%s'" % args[0]
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage

    def do_stop(self, arguments):
        'Stop Monitoring.\nUsage: stop monitor ..'
        usage = self.do_start.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if 'monitor' in arguments:
            if 'monitor' == args[0]:
                args = args[1:]
            self.stop_monitor(args)
        else:
            print usage

    def complete_stop(self, text, line, begidx, endidx):
        completions = self.common_complete('stop', text, line, begidx, endidx)
        return completions

    def stop_monitor(self, args):
        'Stop Monitoring a Node.'
        usage = 'Usage: stop monitor <node_name>'
        if len(args) == 1:
            if args[0] in self.nodes:
                ##### Stop Monitoring Node
                self.get_progress_char()
                print "Stopped Monitoring node: '%s'" % args[0]
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage

    def do_change(self, arguments):
        'Change Interval.\nUsage: change interval ...'
        usage = self.do_change.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if 'interval' in arguments:
            if 'interval' == args[0]:
                args = args[1:]
            self.change_interval(args)
        else:
            print usage

    def complete_change(self, text, line, begidx, endidx):
        completions = self.common_complete('change', text, line, begidx, endidx)
        return completions

    def change_interval(self, args):
        'Change Monitoring Interval.'
        usage = 'Usage: change interval <node_name> <interval>'
        interval = 0
        if len(args) == 2:
            if args[0] in self.nodes:
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

    def do_show(self, arguments):
        'Show Details Node.\nUsage: show node'
        usage = self.do_show.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if 'node' in arguments:
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
            if args[0] in self.nodes:
                #### Node Details
                self.get_progress_char()
                print "Node: '%s'\'s details" % args[0]
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage

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
               time.sleep(0.2)
           i += 1

if __name__ == '__main__':
    monitor_cli().cmdloop()
