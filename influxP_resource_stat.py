#!/usr/bin/python
#! -*- coding:utf-8 -*-

import sched, time
import subprocess
import re
from influxdb import InfluxDBClient
from threading import Timer
import argparse

global DB_NAME
global DEST_HOST
global PORT

DB_NAME = 'map_stat_db'
DEST_HOST = 'localhost'
PORT = 8086

def get_stat():
    sproc_obj = subprocess.Popen(['top', '-n1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    outp, aerr = sproc_obj.communicate()
    if outp:
        res_ar = []
        prc_res = outp.split('\n') 
        for i, prc_info in enumerate(prc_res[7:]):
            ar = prc_info.split(None) 
            ar = map(lambda x:re.sub(r'(\x1b[^m]*m*\x1b.*[A-Z])|(\x1b[^m]*m)', '', x), ar)
            ar = [x for x in ar if x.strip()]
            if not ar :continue
            if len(ar) < 10:continue
            if i == 0:
               continue
            try:
               cpu = float(ar[8])
               memory = float(ar[9])
            except:
                continue
            if (not cpu) and (not memory):
                continue
            #['PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND']
            point = {
                "measurement": "system_resource_stats",
                "tags": {
                    "user_name": ar[1],
                    "command_name": ar[11],
                        },
                "fields": {
                     "cpu_usage": cpu,
                     "memory_usage": memory,
                        }
                }
            print point
            res_ar.append(point)
        if res_ar:
            print '=' * 100 + '\n'
            client = InfluxDBClient(DEST_HOST, PORT, '', '', DB_NAME)
            client.create_database(DB_NAME)
            client.write_points(res_ar)

def get_counter_value(cv=0):
    c = 0
    if cv.lower() == 'inf':
        c = float('inf')
    elif str(cv).isdigit():
        c = int(cv)
    return c

def run_stat_update(cv=0, fr=2):
    c = get_counter_value(cv)
    while c > 0:
        Timer(1, get_stat, ()).start()
        time.sleep(fr)
        c -= 1

def start_monitor(username, cv=0, fr=0, fixed_time='', range_time='', qv='', mn=''):
    client = InfluxDBClient(DEST_HOST, PORT, '', '', DB_NAME)
    cond_str_ar = []
    if username:
        if username[0] == '~':
            username = ' !~ /' + username[1:] + '/ ' 
        else:
            username = ' =~ /' + username + '/ ' 
        cond_str_ar.append("user_name%s" % (username))
    if fixed_time or range_time:
        if fixed_time:
            cond_str_ar.append("time > now() - %s" % (fixed_time))
        else: 
            stt, ent = range_time.split('|')
            if stt.strip():
                cond_str_ar.append("time >= '%s' - 5h - 30m" % (stt))
            if ent.strip():
                cond_str_ar.append("time <= '%s' - 5h - 30m" % (ent))
    cond_str = ' and '.join(cond_str_ar)

    if qv:
        func_var_ar = qv.split('#')
        select_query_ar = [] 
        for func_var in func_var_ar:
            function_name, variable_name = func_var.split('|')
            func_var_as_name = function_name + '_' + variable_name
            select_query_ar.append(function_name + '(' + variable_name + ') as ' + func_var_as_name) 
        q_str = 'select ' + ', '.join(select_query_ar) + ' from ' + mn + ' where %s group by user_name fill(0)' % (cond_str)
    else:
        q_str = 'select max(cpu_usage) as max_cpu, min(cpu_usage) as min_cpu, max(memory_usage) as max_memory, min(memory_usage) as min_memory, mean(cpu_usage)as avg_cpu, mean(memory_usage) as avg_memory  from system_resource_stats where cpu_usage>0 and memory_usage>0 and %s group by user_name fill(0)'  % (cond_str) 
    print '\n' + '+' * 100
    print q_str
    print '\n' + '+' * 100 + '\n\n'
    c = get_counter_value(cv)
    while c > 0:
        res_set = client.query(q_str, expected_response_code=200, raise_errors=True)
        for k, v in res_set.items():
            row_res_ar = []
            #row_res_ar.append(('Measurement', k[0]))
            row_res_ar.append(('User Name', k[1]['user_name']))
            for res_elm in list(v):
                for tagname, value in res_elm.items():
                    if tagname == 'time':continue
                    row_res_ar.append((tagname, str(value)))
            row_res_ar.sort()
            print '\n'.join(map(lambda x:'{:<20}'.format(x[0])+ ':\t' + x[1], row_res_ar))
            print '-' * 50
        print '=' * 100   
        c -= 1
        time.sleep(fr)

def parse_args():
    parser = argparse.ArgumentParser(description='INFLUX DB DEMO')
    parser.add_argument('--db', type=str, required=False, default=DB_NAME, help='Data Base Name')
    parser.add_argument('--host', type=str, required=False, default=DEST_HOST, help='Host Name')
    parser.add_argument('--port', type=int, required=False, default=PORT, help='Port Number')
    parser.add_argument('--cmd', type=str, required=True, default=0, help='"Run" to start stat monitoring tool | "Q" to Query')
    parser.add_argument('--un', type=str, required=False, default='', help='User Name')
    parser.add_argument('--cv', type=str, required=False, default=0, help='Counter Value')
    parser.add_argument('--fr', type=int, required=False, default=0, help='Frequency')
    parser.add_argument('--ft', type=str, required=False, default='', help='From Current Time given time value (N + Precisions [ns, s, m, h, d, w])')
    parser.add_argument('--rt', type=str, required=False, default='', help='Start Time | End Time (Format YYYY-MM-DD HH:MM:SS:ns')
    parser.add_argument('--qv', type=str, required=False, default='', help='Query Function|Variable#QF2|V...')
    parser.add_argument('--mn', type=str, required=False, default='', help='Measurement Name')
    return parser.parse_args()

def main(args):
    global DB_NAME
    global DEST_HOST
    global PORT

    DB_NAME = args.db
    DEST_HOST = args.host
    PORT = args.port
    cmd = args.cmd

    if cmd.lower() == 'run':
        cv = args.cv
        fr = args.fr
        run_stat_update(cv, fr)
    elif cmd =='Q':
        username = args.un
        cv = args.cv
        fr = args.fr
        fixed_time = args.ft
        range_time = args.rt
        qv = args.qv
        mn = args.mn
        start_monitor(username, cv, fr, fixed_time, range_time, qv, mn)

if __name__=='__main__':
    args = parse_args()
    main(args)
