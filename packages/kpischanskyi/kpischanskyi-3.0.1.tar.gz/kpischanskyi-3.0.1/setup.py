#!/usr/bin/env python
import os
import shutil
import sys
from distutils.core import setup

package_version = "3.0.1"
package_name = 'grdpcli'
target_execute_path = '/usr/local/bin/grdp'

data_files=[
        ('grdpcli/__init__.py'),
        ('grdpcli/variables.py'),
        ('grdpcli/cmd_exec.py'),
        ('grdpcli/help_content.py'),
    ]


# Fix macOS path issues by checking if it's installed in user directories
if sys.platform == 'darwin':
    user_base = os.path.expanduser('~')
    bin_path = os.path.join(user_base, 'Library/Python', f"{sys.version_info.major}.{sys.version_info.minor}", 'bin')
    if bin_path not in os.environ.get('PATH', ''):
        print(f"WARNING: The script is installed in '{bin_path}' which is not on PATH.")
        print(f"Consider adding this directory to PATH:\n  export PATH=\"$PATH:{bin_path}\"")

#MacOS
if not os.path.exists(target_execute_path):
    shutil.copy('grdp', target_execute_path)

def package_files(data_files, directory_list):
    paths_dict = {}
    for directory in directory_list:
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(path, filename)
                install_path = os.path.join('share', package_name, path)
                if install_path in paths_dict.keys():
                    paths_dict[install_path].append(file_path)
                else:
                    paths_dict[install_path] = [file_path]
    for key in paths_dict.keys():
        data_files.append((key, paths_dict[key]))
    return data_files

setup(name='kpischanskyi',
      version=package_version,
      description='Gitlab Rapid Development Platform CLI client',
      author='test',
      author_email='kostiantyn.pischanskyi@onix-systems.com',
      url='https://test.com',
      data_files=package_files(data_files, ['grdpcli/']),
      install_requires=[
          'GitPython==3.1.24',
          'requests==2.27.1',
          'tabulate==0.9.0',
          'grdp-cli-kubernetes==1.0.2',
          'rich==10.16.2',
          'questionary==2.0.1'
      ],
      scripts=["grdp"],
      python_requires='>=3'
     )
