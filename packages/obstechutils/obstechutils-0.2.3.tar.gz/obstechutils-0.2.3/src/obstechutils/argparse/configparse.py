try:
    import tomllib
except:
    try:
        from pip._vendor import toml as tomllib
    except:
        from pip._vendor import tomli as tomllib

import yaml
import argparse 
import re
import sys
import textwrap
from typing import Callable, Union

from pathlib import Path
from importlib import resources
from pathlib import Path

import inspect
from importlib import resources
from pathlib import Path


def get_parent_resource(path):

    stack = inspect.stack()

    for frm in stack[-2::-1]:
        modname = inspect.getmodule(frm[0]).__name__
        if modname != "__main__":
            break

    if modname != __name__:
        root = resources.files(modname.split('.')[0])
        return Path(root) / path

    msg = "Could not determine system-wide configuration location"    
    raise RuntimeError(msg)


class CustomHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):

    def _format_args(self, action, default_metavar):

        get_metavar = self._metavar_formatter(action, default_metavar)
        x = get_metavar(1)[0]
        if isinstance(x, list):
            return ' '.join(x)
        return super()._format_args(action, default_metavar)

def type_from_str(
        name: str, 
        user_types: dict[str, Callable[[object], object]]
    ) -> Callable[[object], object]:

    name = name.strip()

    builtins = __builtins__
    if not isinstance(builtins, dict):
        builtins = dict(builtins)

    type_ = builtins.get(name, user_types.get(name, None))

    if not callable(type_):
        raise TypeError(f'invalid type {name}')

    return type_

def paragraph(text: str, width: int = 79, indent: str = '# ') -> str:

    text = textwrap.fill(
        text, width=width, 
        initial_indent=indent, subsequent_indent=indent
    ) + "\n"

    return text

class PrintConfig(argparse.Action):

    def __init__(self, option_strings, options, name, *args, **kwargs) -> None:

        self.options = options
        self.name = name
        super().__init__(option_strings=option_strings, *args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        config_file = Path(f"~/config/{self.name}.yaml").expanduser()

        config = paragraph(f"configuration for {self.name}") 
        config += paragraph(f"user configuration: {config_file}")
        config += "\n"

        for opt, kwargs in self.options.items():

            if help_ := kwargs.get('help'):
                config += paragraph(help_)
                
            if type_ := kwargs.get('type'):
                config += paragraph(f"({type_})")

            if (default := kwargs.get('default')) is not None:
                if isinstance(default, list):
                    yval = yaml.dump(default, default_flow_style=True)
                    config += f"{opt}: {yval}\n"
                else:
                    config += yaml.dump({opt: default}) + "\n"
            else:
                config += "# No system-wide default\n"
                config += f"# {opt} = NODEFAULT\n\n"

        print(config)
        sys.exit(0)

class ConfigParser:

    def __init__(
        self, 
        name: str, 
        sys_config_dir: Union[Path, None] = None, 
        **kwargs
    ) -> None:

        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = CustomHelpFormatter
       
        self.name = name
 
        if sys_config_dir is None:
            sys_config_dir = get_parent_resource('config')
        self.sys_config_file = sys_config_dir / f"{name}.toml"
       
        self.parser = argparse.ArgumentParser(**kwargs)

    def add_options_from_config(
            self, 
            *,  
            user_config: bool = True, 
            environ: bool = False,
            user_types: dict = { }
    ) -> None:

        # system-wide configuration
   
        with open(self.sys_config_file, 'r') as in_:
            sys_options = tomllib.loads(in_.read())
        
        options = {opt: kwargs for opt, kwargs in sys_options.items()}
        if user_config_dir := options.pop('user_config_dir', None):
            usr_config_dir = Path(user_config_dir)
        else:
            usr_config_dir = Path("~/.config/{self.name}").expanduser()
        self.usr_config_file = usr_config_dir / f"{self.name}.yaml"

        cfg_help = f"User configuration file: {self.usr_config_file}\n"
        
        epilog = self.parser.epilog if self.parser.epilog else ''
        self.parser.epilog = f"{epilog}\n{cfg_help}"

        for opt in ['print_config']:
            if opt in sys_options:
                raise RuntimeError(f'option --{opt} is reserved')

        # read user configuration

        usr_options = {}
        if user_config and self.usr_config_file.is_file():
            with open(self.usr_config_file) as in_:
                usr_options = yaml.safe_load(in_)

        # read environment variables

        env_options = {}
        if environ:
            for opt in sys_options:
                if value := os.environ.get(f"{self.name}_{opt}".upper()):
                    env_options[opt] = value

        # override system defaults with user config and environment variables

        for opt, default in usr_options.items():
            if opt not in sys_options:
                raise RuntimeError(f"unkwnown options: {opt}")
            options[opt]['default'] = default
        
        for opt, default in env_options.items():
            options[opt]['default'] = default
        
        # build parser

        for opt, kwargs in options.items(): 

            kwargs = {a: b for a, b in kwargs.items()}
            alternate_names = kwargs.get('alternate_names', [])

            for name in alternate_names:
                if name[0] not in '-':
                    msg = f"alternate name {name} for --{opt} must start with -"
                    raise argparse.ArgumentError(msg)

            action = kwargs.pop('action', None)
            dest = kwargs.pop('dest', opt) 
            default = kwargs.pop('default', None)
            type_ = kwargs.pop('type', None)
            if type_:
                msg = f"Invalid type {type_} for {opt}"
                type_ = type_from_str(type_, user_types)
                if type_ is None:
                    raise RuntimeError(msg)

            if type_:
                kwargs['type'] = type_

            if action == 'flag':
                action = argparse.BooleanOptionalAction
            
            self.parser.add_argument(
                f"--{opt}", *alternate_names, 
                default=default,
                dest=dest, action=action, **kwargs
            )

        self.parser.add_argument(
            '--print_config', action=PrintConfig,
            options=options, name=self.name, nargs=0,
            help="print default configuration and exit"
        )
        
    def add_argument(self, arg: str, **kwargs: dict) -> None:

        if arg in '-+':
            return argparse.ArgumentError('can only add non option arguments')
        
        self.parser.add_argument(arg, **kwargs)

    def parse_args(
        self, 
        args: tuple[str] = [], 
        namespace: object = None
    ) -> object:

        return self.parser.parse_args(args=args, namespace=namespace) 

