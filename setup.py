from distutils.core import setup

setup(name='dndresmanager',
      version='1.0',
      description='Resource manager for dnd 5e',
      packages=['dndresmanager'],
      entry_points={
        'console_scripts': [
            'dndresmanager = dndresmanager:main',
        ]
    }
     )