#!/usr/bin/env python3
# pylint: disable=line-too-long
"""Proc_tool runs commands in a subprocess with environ variables based on config files."""
import subprocess
import os
from pathlib import Path
from datetime import datetime
import argparse
import yaml


def load_config(filename):
    """Returns yaml config file as dictionary."""
    return yaml.safe_load(filename.read_text())


def run_proc(config, proc):
    """Runs a process that as defined in config file."""
    pconf = config.get(proc)
    if pconf:
        print("Running process: " + proc)
        command = pconf.get('command')
        if command:
            shell = pconf.get('shell') or False
            logfile = pconf.get('logfile')
            proc_env = pconf.get('environ', [])

            if isinstance(command, str):
                shell = True

            print('    Command: '+str(command))
            print('    Shell: '+str(shell))
            if proc_env:
                print('    Env: '+str(proc_env))

            env = {}
            env.update(os.environ)
            env.update([k.partition('=')[0:3:2] for k in pconf.get('environ', [])])

            if logfile and isinstance(logfile, str):
                logfile = logfile.format(datetime=datetime.now())
                print('    Logfile: '+logfile)
                with open(logfile, 'w') as logfile:
                    subprocess.Popen(command, shell=shell, stdout=logfile, stderr=logfile, env=env)
            else:
                subprocess.Popen(command, shell=shell, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)


def open_gui(config):
    """Opens a gui window."""
    import tkinter as tk
    from tkinter import ttk
    root = tk.Tk()
    root.geometry('600x400')
    root.resizable(True, True)
    root.title('Combobox Widget')

    label = ttk.Label(text="Select a process:")
    label.pack(fill=tk.X, padx=5, pady=5)

    selected_proc = tk.StringVar()
    cbx_proc = ttk.Combobox(root, textvariable=selected_proc)
    cbx_proc['values'] = list(config.keys())
    cbx_proc['state'] = 'readonly'
    cbx_proc.pack(fill=tk.X, padx=5)

    def btn_run_callback():
        proc = selected_proc.get()
        run_proc(config, proc)

    btn_run = ttk.Button(root, text="run", command=btn_run_callback)
    btn_run.pack(fill=tk.X, padx=5, pady=1)

    text = tk.Text(root)
    text.pack(fill=tk.BOTH, padx=5, pady=5)

    def cbx_proc_on_select(event):
        data = config.get(selected_proc.get())
        text.delete(0.0, tk.END)
        tmpstr = 'command: '+str(data['command'])+'\n'
        if data.get('logfile'):
            tmpstr = tmpstr + 'logfile: ' + data['logfile'] + '\n'
        if data.get('environ'):
            tmpstr = tmpstr + 'environ:\n' + yaml.dump(data['environ'], default_flow_style=False) + '\n'
        text.insert(0.0, str(tmpstr))

    cbx_proc.bind('<<ComboboxSelected>>', cbx_proc_on_select)

    root.mainloop()


def parse_args():
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser()
    script_dir = Path(__file__).resolve().parent

    parser.add_argument('--config', default=(script_dir / 'subprocs.yaml').resolve(), help='Config file to use, if empty use subprocs.yaml file.')
    parser.add_argument('procid', type=str, nargs='*', help='Proc ids to execute. Use none for gui interface.')

    opts = parser.parse_args()
    params = vars(opts)
    return params


def main():
    """Parse arguments, load config and execute the correct command."""
    args = parse_args()
    config = load_config(args['config'])
    if not args.get('procid'):
        open_gui(config)
    for proc in args['procid']:
        run_proc(config, proc)


if __name__ == "__main__":
    main()
