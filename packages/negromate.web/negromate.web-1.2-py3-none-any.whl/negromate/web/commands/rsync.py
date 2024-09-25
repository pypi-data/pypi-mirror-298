import subprocess
from pathlib import Path


name = "rsync"
help_text = "Sincronize the static web with the server"
initial_config = {
    "host": "negromate.rocks",
    "user": "root",
    "port": "22",
    "destination": "/var/www/html",
}


def options(parser, config, **kwargs):
    parser.add_argument(
        "-s",
        "--song_folder",
        type=Path,
        default=config["global"]["song_folder"],
        help=f"Folder with the song database, defaults to {config['global']['song_folder']}",
    )
    parser.add_argument(
        "-H", "--host", default=config[name]["host"], help=f"Target server, defaults to {config[name]['host']}."
    )
    parser.add_argument(
        "-u",
        "--user",
        default=config[name]["user"],
        help=f"User in the server, defaults to {config[name]['user']}.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=config[name]["port"],
        type=int,
        help=f"Port of the ssh server, defaults to {config[name]['port']}.",
    )
    parser.add_argument(
        "-d",
        "--destination",
        default=config[name]["destination"],
        help=f"Folder of the server, defaults to {config[name]['destination']}",
    )


def run(args, **kwargs):
    contents = str(args.song_folder.expanduser()) + "/"
    destination = f"{args.user}@{args.host}:{args.destination}"
    command = [
        "rsync",
        "-av",
        f"--rsh=ssh -p {args.port}",
        contents,
        destination,
    ]
    print(" ".join(command))
    subprocess.check_call(command)
