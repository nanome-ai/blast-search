# Nanome - Similarity Search

Stage 1: A plugin that takes in a single PDB, MMCIF and converts the file format to FASTA runs a search on BLAST, Returns similarities for top N results w/ % similarity score, return a PDB/PDB Code and show those options in Nanome window

Install the latest version of [Python 3](https://www.python.org/downloads/)

| NOTE for Windows: replace `python3` in the following commands with `python` |
| - |

Install the latest `nanome` lib:
```sh
$ python3 -m pip install nanome --upgrade
```

Run the plugin:
```sh
$ python3 run.py -a <plugin_server_address> [optional args]
```

### License

MIT
