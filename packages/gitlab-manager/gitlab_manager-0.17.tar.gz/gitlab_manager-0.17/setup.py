from setuptools import setup, find_packages
from pathlib import Path
import os
import sys

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Fix macOS path issues by checking if it's installed in user directories
if sys.platform == 'darwin':
    user_base = os.path.expanduser('~')
    bin_path = os.path.join(user_base, 'Library/Python', f"{sys.version_info.major}.{sys.version_info.minor}", 'bin')
    if bin_path not in os.environ.get('PATH', ''):
        print(f"WARNING: The script is installed in '{bin_path}' which is not on PATH.")
        print(f"Consider adding this directory to PATH:\n  export PATH=\"$PATH:{bin_path}\"")

setup(
    name='gitlab-manager',
    version='0.17',
    readme="README.md",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'requests',
        'python-gitlab'
    ],
    entry_points={
        'console_scripts': [
            'gitlab-manager = gitlab_manager.main:main',
        ],
    },
)
