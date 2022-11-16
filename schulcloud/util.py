import os
from typing import List, Optional


class Environment:

    def __init__(self, env_vars: Optional[List[str]] = None, ask_for_missing: bool = False):
        self.vars = {}

        if env_vars is None:
            return

        missing = []
        for env_var in env_vars:
            value = os.getenv(env_var)
            if value is None:
                if ask_for_missing:
                    value = ''
                    while not value:
                        value = input(f'{env_var}=')
                else:
                    missing.append(env_var)
                    continue
            self.vars[env_var] = value
        if missing:
            raise RuntimeError(f'Missing environment variables: {missing}')

    def __getitem__(self, item):
        if not self.vars:
            var = os.getenv(item)
            if not var:
                raise RuntimeError(f'Environment variable not found: {item}')
            return var
        else:
            return self.vars[item]
