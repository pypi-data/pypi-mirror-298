import re
import os
import yaml
import difflib
import fnmatch
import itertools
from argparse import ArgumentParser
from pathlib import Path

from .printing import print
from .remote import Remote


class UConf:

    def __init__(self,
                 preset: Path = None,
                 host: str = None,
                 user: str = None,
                 password: str = None,
                 public_key: str = None,
                 sudo: bool = False,
                 debug: bool = False,
                 directory: str = None):

        self.preset_data = {}
        if preset:
            with print('🟪[Loading preset]', close='\n'):
                self.load_preset(preset)

        self.debug = debug
        self.directory = directory

        if self.preset_data.get('remote', None):
            remote_preset = self.preset_data['remote']
            host = host or remote_preset.get('host', None)
            user = user or remote_preset.get('user', None)
            public_key = public_key or remote_preset.get('public_key', None)
            sudo = sudo or remote_preset.get('sudo', None)

        host = host or 'localhost'
        user = user or 'root'

        self.remote = Remote(host, user, password, public_key, sudo=sudo, debug=debug)

    def list_options(self, config: str = None, directory: str = None, comp: bool = False):
        '''
        List the available configuration options.
        '''
        path = self.get_config_path(config, directory, comp)
        with print(f'🟪{path}'):
            content = self.remote.get(path)

            # Find all options and defaults
            options = re.findall(r'#\s+Option:\s+(.*)', content, re.MULTILINE)
            defaults = re.findall(r'#\s+[Dd]efault:\s+(.*)', content, re.MULTILINE)

            longest = max([len(option.strip()) for option in options])
            lines = []
            for option, default in zip(options, defaults):
                lines.append(f'{option.strip()} {"." * (longest - len(option) + 4)} {default.strip()}')

            lines = sorted(lines)
            # split each option by _ and group them into separate lists by the first part
            groups = [list(g) for k, g in itertools.groupby(lines, lambda x: x.split('_')[0])]
            # sort groups by number of options in each group, then alphabetically
            groups.sort(key=lambda x: (len(x), x[0][0]))

            option = "[Option Name]"
            print(f'🟩{option} {" " * (longest - len(option) + 4)} [Default Value]')
            for i, group in enumerate(groups):
                for option in group:
                    option = option.strip()
                    option = f'🟦{option}' if i % 2 == 0 else f'⏹{option}'
                    print(option)

    def get_option_info(self, config: str, option: str, directory: str = None, comp: bool = False):
        '''
        Get the description of a specific configuration option.
        '''
        config_path = self.get_config_path(config, directory, comp)
        content = self.remote.get(config_path)
        lines = content.splitlines()

        found = False
        for line in lines:
            if found and line.startswith('# Option') or line.startswith('#####'):
                break
            if re.match(r'#\s+Option:\s+{}'.format(option), line):
                found = True
            if found:
                print(f'⏹{line[1:].rstrip()}')
        else:
            print(f'🟨Option {option} not found in {config_path}')

    def update(self, config: str, directory: str = None, comp: bool = False, **options: str):
        '''
        Set configuration options in a configuration file.
        '''
        config_path = self.get_config_path(config, directory, comp)

        with print(f'🟪{config_path}'):
            content = self.remote.get(config_path)
            current_options = self.parse(content)
            new_content = content.splitlines()

            for option, value in options.items():
                if value is not None:
                    value = '{0}    {1}'.format(" " * max(24 - len(option), 0), value)
                matches = fnmatch.filter(current_options.keys(), option)
                if matches:
                    for match in matches:
                        spanned_lines = current_options[match]['lines']
                        for i in spanned_lines:
                            new_content[i] = None
                        if value is not None:
                            new_content[spanned_lines[0]] = '{0}{1}\n'.format(match, value)
                elif value is not None:
                    new_content.append('{0}{1}\n'.format(option, value))
            new_content = '\n'.join([i for i in new_content if i is not None])
            self.remote.put(config_path, new_content)
            self.diff(content, new_content)

    def diff(self, original, updated):
        # remove comments
        orig = [line for line in original.splitlines() if not line.startswith('#')]
        new = [line for line in updated.splitlines() if not line.startswith('#')]

        # get the diff

        result = difflib.Differ().compare(orig, new)

        changed = False
        for line in result:
            if line.startswith('?'):
                line = line.replace('?', '🟨?', 1)
                changed = True
            if line.startswith('-'):
                line = line.replace('-', '🟥-', 1)
                changed = True
            if line.startswith('+'):
                line = line.replace('+', '🟩+', 1)
                changed = True
            print(line)

        if not changed:
            print('⏹No changes were made')

    def parse(self, content: str) -> dict:
        compacted = []
        multiline = False
        buffer = " "
        line = ""
        for line_num, line in enumerate(content.splitlines()):
            if line.startswith('#'):
                continue

            line = line.strip()
            if len(line) == 0:
                continue
            last_char = line[-1]
            if last_char == '-' or last_char == '+':
                line = line[0:-1]

            if multiline:
                compacted[-1]['entry'] = (compacted[-1]['entry'] + buffer + line)
                compacted[-1]['lines'].append(line_num)
            else:
                compacted.append({'entry': line, 'lines': [line_num]})

            if last_char == '+':
                multiline = True
                buffer = ""
            elif last_char == '-':
                multiline = True
                buffer = " "
            else:
                multiline = False

        result = {}
        for item in compacted:
            pair = item['entry'].split(maxsplit=1)
            if len(pair) != 2:
                result[pair[0]] = {'value': None, 'lines': item['lines']}
            else:
                result[pair[0]] = {'value': pair[1], 'lines': item['lines']}
        return result

    def get_config_path(self, name: str, directory: str = None, comp: bool = False):
        directory = directory or self.directory or '/etc/universal/'
        comp = comp or self.preset_data.get('comp', False)

        if not comp and not name.endswith('.conf'):
            name += '.conf'

        return directory.rstrip('/') + '/' + name

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

    parser.add_argument('config_or_preset', type=str)
    parser.add_argument('options', nargs='*', )

    # Remote
    parser.add_argument('-i', '--host', type=str, default=os.environ.get('SBUTILS_HOST'))
    parser.add_argument('-u', '--user', type=str, default=os.environ.get('SBUTILS_USER'))
    parser.add_argument('-p', '--password', type=str, default=os.environ.get('SBUTILS_PASSWORD'))
    parser.add_argument('-P', '--public-key', type=str, default=os.environ.get('SBUTILS_PUBLIC_KEY'))
    parser.add_argument('-s', '--no-sudo', action='store_false', dest='sudo')
    parser.add_argument('--debug', action='store_true')
    # Function
    parser.add_argument('-d', '--directory', type=str)
    parser.add_argument('-m', '--more', type=str)
    parser.add_argument('-c', '--comp', action='store_true')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-B', '--backup', action='store_true')
    parser.add_argument('-R', '--restore', action='store_true')

    args = parser.parse_args()

    if args.config_or_preset.endswith('.yml'):
        preset = args.config_or_preset
        config = None
    else:
        config = args.config_or_preset
        preset = None

    uconf = UConf(preset=preset,
                  host=args.host,
                  user=args.user,
                  password=args.password,
                  public_key=args.public_key,
                  sudo=args.sudo,
                  debug=args.debug,
                  directory=args.directory)
    if preset:
        # uconf.load_preset(preset)
        pass
    elif args.list:
        uconf.list_options(config=config, directory=args.directory, comp=args.comp)
    elif args.more:
        uconf.get_option_info(config=config, option=args.more, directory=args.directory, comp=args.comp)
    elif args.backup:
        pass
    elif args.restore:
        pass
    else:
        options = {}
        for option in args.options:
            if '=' not in option:
                options[option] = None
                continue
            key, value = option.split('=', 1)
            options[key] = value
        uconf.update(config=config, directory=args.directory, comp=args.comp, **options)


if __name__ == '__main__':
    main()
