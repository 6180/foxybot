""" import the commands _dynamically_ """

import os

__path__ = ['commands']
__all__ = [filename.rsplit('.')[0] for filename in os.listdir(__path__[0])
           if not filename.startswith('_')
           and (filename.endswith('.py') or os.path.isdir(f'{__path__[0]}/{filename}'))]

print(f'[commands]: {__all__}')
