import cmd
import sys
import time
import shlex
import ipaddr

class monitor_cli(cmd.Cmd):

    def __init__(self, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)
        self.intro = ' Cluster Management\n'
        self.prompt = '> '
        self.nodes = ['compute001', 'compute002']

    def is_valid_ip(self, ip_add):
        try: 
            val_ip = ipaddr.IPAddress(ip_add)
        except ValueError:
            val_ip = 0
        return val_ip

    def do_add_node(self, arguments):
        'Add a Node.\nUsage: add_node <node_name> <node_ip> <username> <password>'
        usage = self.do_add_node.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if len(args) == 4:
            node_name, node_ip, username, password = args
            if self.is_valid_ip(node_ip):
                ##### Add Node
                if node_name in self.nodes:
                    print "Node Name '%s' Already Exists" % args[0]
                else:
                    self.get_progress_char()
                    self.nodes.append(node_name)
                    print "Successfully added", args
            else:
                print "Invalid Ip Address\n" + usage
        else:
            print usage
  
    def do_del_node(self, arguments):
        'Delete a Node.\nUsage: del_node <node_name>'
        usage = self.do_del_node.__doc__.split('\n')[1]
        args = shlex.split(arguments)
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

    def complete_del_node(self, text, line, begidx, endidx):
        if not text:
            completions = self.nodes[:]
        else:
            completions = [f for f in self.nodes if f.startswith(text)]
        return completions

    def do_start_monitor(self, arguments):
        'Start Monitoring a Node.\nUsage: start_monitor <node_name>'
        usage = self.do_start_monitor.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if len(args) == 1:
            if args[0] in self.nodes:
                self.get_progress_char()
                ##### Start Monitoring Node
                print "Monitoring node: %s" % args[0]
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage

    def complete_start_monitor(self, text, line, begidx, endidx):
        if not text:
            completions = self.nodes[:]
        else:
            completions = [f for f in self.nodes if f.startswith(text)]
        return completions

    def do_stop_monitor(self, arguments):
        'Stop Monitoring a Node.\nUsage: stop_monitor <node_name>'
        usage = self.do_stop_monitor.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if len(args) == 1:
            if args[0] in self.nodes:
                ##### Stop Monitoring Node
                self.get_progress_char()
                print "Stopped Monitoring node: %s" % args[0]
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage

    def complete_stop_monitor(self, text, line, begidx, endidx):
        if not text:
            completions = self.nodes[:]
        else:
            completions = [f for f in self.nodes if f.startswith(text)]
        return completions

    def do_change_interval(self, arguments):
        'Set Monitoring Interval.\nUsage: change_interval <node_name> <interval>'
        usage = self.do_change_interval.__doc__.split('\n')[1]
        args = shlex.split(arguments)
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

    def complete_change_interval(self, text, line, begidx, endidx):
        if not text:
            completions = self.nodes[:]
        else:
            completions = [f for f in self.nodes if f.startswith(text)]
        return completions

    def do_add_tag(self, arguments):
        'Add tag.\nUsage: add_tag <node_name> <tag>'
        usage = self.do_add_tag.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if len(args) == 2:
            if args[0] in self.nodes:
                #### add_tag
                self.get_progress_char()
                print "Tag '%s' added to %s\'s monitoring data" % (args[1], args[0])
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage

    def complete_add_tag(self, text, line, begidx, endidx):
        if not text:
            completions = self.nodes[:]
        else:
            completions = [f for f in self.nodes if f.startswith(text)]
        return completions

    def do_remove_tag(self, arguments):
        'Remove tag.\nUsage: remove_tag <node_name>'
        usage = self.do_remove_tag.__doc__.split('\n')[1]
        args = shlex.split(arguments)
        if len(args) == 1:
            if args[0] in self.nodes:
                #### remove_tag
                self.get_progress_char()
                print "Tags removed from %s\'s monitoring data" % (args[0])
            else:
                print "Node '%s' does not exists in Cluster" % args[0]
        else:
            print usage

    def complete_remove_tag(self, text, line, begidx, endidx):
        if not text:
            completions = self.nodes[:]
        else:
            completions = [f for f in self.nodes if f.startswith(text)]
        return completions

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
