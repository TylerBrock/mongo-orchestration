#!/usr/bin/python
# coding=utf-8
import argparse
import atexit
import json
import os
import sys

from bson import SON

from mongo_orchestration.daemon import Daemon

work_dir = os.environ.get('MONGO_ORCHESTRATION_HOME', os.getcwd())

pid_file = os.path.join(work_dir, 'server.pid')
log_file = os.path.join(work_dir, 'server.log')

DEFAULT_BIND = 'localhost'
DEFAULT_PORT = 8889
DEFAULT_SERVER = 'cherrypy'

import logging
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w')


def read_env():
    """return command-line arguments"""
    parser = argparse.ArgumentParser(description='mongo-orchestration server')
    parser.add_argument('-f', '--config',
                        action='store', default=None, type=str, dest='config')
    parser.add_argument('-e', '--env',
                        action='store', type=str, dest='env', default=None)
    parser.add_argument(action='store', type=str, dest='command',
                        default='start', choices=('start', 'stop', 'restart'))
    parser.add_argument('--no-fork',
                        action='store_true', dest='no_fork', default=False)
    parser.add_argument('-b', '--bind',
                        action='store', dest='bind', type=str,
                        default=DEFAULT_BIND)
    parser.add_argument('-p', '--port',
                        action='store', dest='port', type=int,
                        default=DEFAULT_PORT)
    parser.add_argument('-s', '--server',
                        action='store', dest='server', type=str,
                        default=DEFAULT_SERVER)

    cli_args = parser.parse_args()

    if cli_args.env and not cli_args.config:
        print("Specified release '%s' without a config file" % cli_args.env)
        sys.exit(1)
    if cli_args.command == 'stop' or not cli_args.config:
        return cli_args
    try:
        # read config
        with open(cli_args.config, 'r') as fd:
            config = json.loads(fd.read(), object_hook=SON)
        if not 'releases' in config:
            print("No releases defined in %s" % cli_args.config)
            sys.exit(1)
        releases = config['releases']
        if cli_args.env is not None and cli_args.env not in releases:
            print("Release '%s' is not defined in %s"
                  % (cli_args.env, cli_args.config))
            sys.exit(1)
        cli_args.releases = releases
        return cli_args
    except (IOError):
        print("config file not found")
        sys.exit(1)
    except (ValueError):
        print("config file is corrupted")
        sys.exit(1)


def setup(releases, default_release):
    """setup storages"""
    from mongo_orchestration import set_releases, cleanup_storage
    set_releases(releases, default_release)
    atexit.register(cleanup_storage)


def get_app():
    """return bottle app that includes all sub-apps"""
    from bottle import default_app
    default_app.push()
    for module in ("mongo_orchestration.apps.servers",
                   "mongo_orchestration.apps.replica_sets",
                   "mongo_orchestration.apps.sharded_clusters"):
        __import__(module)
    app = default_app.pop()
    return app


class MyDaemon(Daemon):
    """class uses to run server as daemon"""

    def __init__(self, *args, **kwd):
        super(MyDaemon, self).__init__(*args, **kwd)

    def run(self):
        from bottle import run
        setup(getattr(self.args, 'releases', {}), self.args.env)
        if self.args.command in ('start', 'restart'):
            print("Starting Mongo Orchestration on port %d..." % self.args.port)
            run(get_app(), host=self.args.bind, port=self.args.port, debug=False,
                reloader=False, quiet=not self.args.no_fork, server=self.args.server)

    def set_args(self, args):
        self.args = args


def main():
    daemon = MyDaemon(pid_file, timeout=5, stdout=sys.stdout)
    args = read_env()
    daemon.set_args(args)
    if args.command == 'stop':
        daemon.stop()
    if args.command == 'start' and not args.no_fork:
        daemon.start()
    if args.command == 'start' and args.no_fork:
        daemon.run()
    if args.command == 'restart':
        daemon.restart()


if __name__ == "__main__":
    main()
