# proc_tool

A little tool to launch sub processes with a command and environmental variables set in a config file.  Gui and command line.

Relies on modules: PyYAML (and tkinter for gui)

## Getting started

```
usage: proc_tool.py [-h] [--config CONFIG] [procid [procid ...]]

positional arguments:
  procid           Proc ids to execute. Use none for gui interface.

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Config file to use, if empty use subprocs.yaml file.
  -l, --list       Lists all proc ids available.
```



Example to execute proc id 'proc_logfile': 
```
./proc_tool.py proc_logfile
```

Leave empty for gui interface:
```
./proc_tool.py
```


All proc ids are defined in a yaml config file.
