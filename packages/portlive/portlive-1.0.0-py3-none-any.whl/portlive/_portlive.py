
from .exceptions import NotConnectedError
from typing import Dict, Union, Iterable
from io import TextIOWrapper
import subprocess
import importlib
import requests
import sys

class PortLive:
    """`PortLive class`
    
    This class contains dynamically generated properties
    that hold the imported modules.
    """
    def __enter__(self):
        """`Enter Context`"""
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """`Exit Context`"""
        pass

    def __init__(
            self,
            modules: Dict[str, Union[str, None]],
            compiler_output: bool = False,
            logger: Union[TextIOWrapper, None] = None,
            loading_message: str = "",
            failed_message: str = "Failed to import library: {}",
    ) -> None:
        """`PortLive class that will generate properties dynamically named after
        the libraries set in the parameter and make it callable.`
        """

        # for each name in the module,
        for name in modules:
            package = None # set placeholder for package
            path = None # set placeholder for path
            name = name.replace('-', '_')

            if '.' in name: # if the name is a path
                parts = name.split('.') # split the parts
                package = parts[0] # first part is the package
                path = '.'.join(parts[1:]) # rest is the path
                name2 = parts[-1] # last part is the name
            
            if package: # if package is not none
                # try to import the library
                try:
                    try:
                        fetched = importlib.import_module('.'+path, package)
                        if modules[name]:
                            setattr(self, modules[name], fetched)
                        else:
                            setattr(self, name2, fetched)
                    except ModuleNotFoundError:
                        raise Exception()
                except Exception: # if fails
                    if loading_message:
                        print(loading_message)
                    
                    try: # try to install the library
                        if compiler_output:
                            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                        elif logger:
                            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], stderr=logger, stdout=logger)
                        else:
                            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    except subprocess.CalledProcessError: # if fails
                        if failed_message:
                            print(failed_message.format(package))
                        sys.exit(1) # exit
                    
                    # import the package now
                    if modules[name]:
                        setattr(self, modules[name], importlib.import_module('.'+path, package))
                    else:
                        setattr(self, name2, importlib.import_module('.'+path, package))
                    
            else: # if package is none
                try: # try importing it
                    try:
                        fetched = importlib.import_module(name)

                        if modules[name]:
                            setattr(self, modules[name], importlib.import_module(name))
                        else:
                            setattr(self, name, importlib.import_module(name))
                    except ModuleNotFoundError:
                        raise Exception()
                except Exception: # if importing fails
                    if loading_message:
                        print(loading_message)
                    
                    try: # try installing
                        if compiler_output:
                            subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])
                        elif logger:
                            subprocess.check_call([sys.executable, '-m', 'pip', 'install', name], stderr=logger, stdout=logger)
                        else:
                            subprocess.check_call([sys.executable, '-m', 'pip', 'install', name], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    except subprocess.CalledProcessError:
                        if failed_message:
                            print(failed_message.format(name))
                        sys.exit(1)
                    
                    # finally import it
                    if modules[name]:
                        setattr(self, modules[name], importlib.import_module(name))
                    else:
                        setattr(self, name, importlib.import_module(name))
    
    def remove(self, property: str):
        """`Delete an imported module.`"""
        delattr(self, property)

def portlive(
        modules: Iterable[str],
        aliases: Union[Iterable[Union[str, None]], None] = None,
        console_output: bool = False,
        logger: Union[TextIOWrapper, None] = None,
        loading_message: str = "",
        error_message: str = "Failed to import library: {}",
) -> PortLive:
    """`Returns a Class that contains all the imported libraries in the form of properties.`
    
    ### Params
    
    - `modules`: An iterable containing the module names or paths. A single module
    name could be of the type `requests` or `requests.get` where the entire module or
    the `get` method will be imported respectively

    - `aliases`: If you want to implement the `import requests as r` type importing,
    where `requests` is the module and `r` is the alias, then suppose you have a list
    of 4 modules you want to import -> `['1', '2', '3', '4']` and you want to import `3` as `three`
    then you can set aliases as `[None, None, 'three', None]`. If no alias needed, set it to None.

    - `console_output`: whether to print the console output (verbose).

    - `logger`: if console_output is set to `False` and a logger file is provided, all outputs and
    errors will be logged to the file.

    `NOTE`: if `console_output` is `False` and no `logger` is provided, all stdout and stderr will be
    suppressed.

    - `loading_message`: The message to print before installing if installation is necessary.
    Set it to `""` if dont want to print.

    - `error_message`: The message to print if install error occurs while installation. Set it to `""`
    if dont want to print.

    ### Usage

    Usage is pretty simple and with the `with` keyword is recommended.

    ```python
    >>> from portlive import portlive
    
    >>> with portlive(
    ...     modules=['mr_menu', 'looger', 'wrapper_bar.wrapper'],
    ...     aliases=[None, 'logger', 'wrapper_bar']
    ... ) as imported:
    ...     # imported.mr_menu will act as mr_menu
    ...     # imported.logger will act as looger
    ...     # imported.wrapper_bar will act as wrapper_bar.wrapper
    ```
    """
    packages = {}
    for i in range(len(modules)):
        packages[modules[i]] = aliases[i] if aliases else None
    
    if requests.get("https://google.com").status_code == 200:
    
        return PortLive(
            packages,
            console_output,
            logger,
            loading_message,
            error_message,
        )
    else:
        raise NotConnectedError("Connetion is either not found or interrupted! Please check your internet connection and try again.")