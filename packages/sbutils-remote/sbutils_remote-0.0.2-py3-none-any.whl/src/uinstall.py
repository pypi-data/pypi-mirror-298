import os
import re
import yaml
import builds
from pathlib import Path
from argparse import ArgumentParser

from .remote import Remote
from .printing import print


class UInstall:

    def __init__(self,
                 preset: Path = None,
                 host: str = None,
                 user: str = None,
                 password: str = None,
                 public_key: str = None,
                 sudo: bool = False,
                 debug: bool = False):

        self.preset_data = {}
        if preset:
            with print('🟪[Loading preset]', close='\n'):
                self.load_preset(preset)

        self.debug = debug

        if self.preset_data.get('remote', None):
            remote_preset = self.preset_data['remote']
            host = host or remote_preset.get('host', None)
            user = user or remote_preset.get('user', None)
            public_key = public_key or remote_preset.get('public_key', None)
            sudo = sudo or remote_preset.get('sudo', None)

        host = host or 'localhost'
        user = user or 'root'

        self.remote = Remote(host, user, password, public_key, sudo=sudo, debug=debug)

    def uninstall(self,
                  rpm: str = None,
                  ubrokerd_path: str = '/opt/universal/ubroker/ubrokerd',
                  paths: list = []):
        '''
        Uninstalls UBroker.

        If an RPM is provided, it will be uninstalled with `rpm -e`.
        Otherwise, the Universal Broker will be stopped and the paths
        provided will be removed.
        '''
        print('🟪[Uninstalling UBroker]')
        print.indent(close='\n')

        # Preset precedence
        conf = self.preset_data.get('uninstall', {})
        rpm = rpm or conf.get('rpm', None)
        ubrokerd_path = ubrokerd_path or conf.get('ubrokerd_path', None)
        paths = paths or conf.get('paths', None)

        if rpm:
            with print(f'⏹Uninstalling with RPM - {rpm}'):
                try:
                    self.remote.run(f'rpm -e {rpm}')
                except RuntimeError as e:
                    if 'is not installed' in str(e):
                        print('🟩Package not installed')
        elif ubrokerd_path:
            self.remote.run(f'{ubrokerd_path} stop')

        if paths:
            with print('⏹Cleaning up paths'):
                for path in paths:
                    with print(f'- {path}'):
                        self.remote.run(f'rm -r {path}')
        print.dedent()

    def install(self,
                link: str = None,
                release: str = None,
                match: str = None,
                options: dict = {}):
        '''Downloads and installs UBroker using the provided options'''
        print('🟪[Installing UBroker]')
        print.indent()

        working_dir = self.download_and_extract(link=link, release=release, match=match)

        options = options or self.preset_data.get('install', {}).get('options', {})
        with print('⏹Running installer script', indent='  | '):
            binary_options = ' '.join(options)
            sudo = 'sudo' if self.remote.sudo else ''
            out, err = self.remote.run(f'cd {working_dir} && {sudo} ./unvinst {binary_options}', sudo=False)
            print(out)
            if 'error' in err:
                raise RuntimeError(err)
        print.dedent()

    def download_and_extract(self, link: str = None, release: str = None, match: str = None):
        '''Downloads and extracts the Universal Broker installer tar to a temporary directory'''

        # Preset precedence
        preset = self.preset_data.get('install', {})
        link = link or preset.get('link', None)
        release = release or preset.get('release', None)
        match = match or preset.get('match', None)

        if not link and not release:
            raise ValueError('No link or release provided')

        # Get the link to download
        if not link:
            link = builds.get_build_link(release, match)

        # Setup working directory
        package = link.split('/')[-1]
        working_dir = '/tmp/uinstall'
        with print('⏹Setting up working directory', working_dir):
            self.remote.run(f'rm -r {working_dir}')
            self.remote.run_safe(f'mkdir -p {working_dir}')

        # Download and extract
        output_file = f'{working_dir}/uinstall-{package}'
        with print('⏹Downloading', link):
            _, err = self.remote.run(f'curl -o {output_file} {link}')
            if 'error' in err:
                raise RuntimeError(err)

        with print('⏹Extracting', output_file):
            self.remote.run_safe(f'tar -xzf {output_file} -C {working_dir}')

        return working_dir

    def load_preset(self, path: Path):
        if not path.exists() or not path.is_file():
            print("🟥Preset file not found")
            exit(2)

        try:
            self.preset_data = yaml.safe_load(path.read_text())
        except Exception as e:
            print(f"🟥Error loading preset: {e}")
            exit(3)

        print(f'🟩Loaded preset: "{path.resolve()}"')


def main():
    parser = ArgumentParser()
    parser.add_argument('preset', type=Path)
    parser.add_argument('-i', '--host', type=str, default=os.environ.get('SBUTILS_HOST'))
    parser.add_argument('-u', '--user', type=str, default=os.environ.get('SBUTILS_USER'))
    parser.add_argument('-p', '--password', type=str, default=os.environ.get('SBUTILS_PASSWORD'))
    parser.add_argument('-P', '--public-key', type=str, default=os.environ.get('SBUTILS_PUBLIC_KEY'))
    parser.add_argument('-s', '--no-sudo', action='store_false', dest='sudo')
    parser.add_argument('--release', type=str)
    parser.add_argument('--link', type=str)
    parser.add_argument('--match', type=str)
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()
    if args.release and not re.match(r'^\d+\.\d+\.\d+\.\d+$', args.release):
        parser.error(f'Invalid release format: {args.release}, expected X.X.X.X')

    uinstall = UInstall(preset=args.preset,
                        host=args.host,
                        user=args.user,
                        password=args.password,
                        public_key=args.public_key,
                        sudo=args.sudo,
                        debug=args.debug)
    uinstall.uninstall()
    uinstall.install(link=args.link, release=args.release, match=args.match)


if __name__ == '__main__':
    main()
