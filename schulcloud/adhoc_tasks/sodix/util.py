
import os
from typing import List


class Environment:

    def __init__(self, env_vars: List[str], ask_for_missing: bool = False):
        self.vars = {}
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
        return self.vars[item]
