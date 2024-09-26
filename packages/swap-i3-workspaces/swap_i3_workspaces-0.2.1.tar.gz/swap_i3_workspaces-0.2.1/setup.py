from setuptools import setup, find_packages

setup(
    name='swap_i3_workspaces',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'i3ipc',
    ],
    entry_points={
        'console_scripts': [
            'swap_i3_workspaces=swap_i3_workspaces.main:main',
        ],
    },
    description="Swap i3 workspaces",
    project_urls={
        'Source': 'https://gitlab.com/sandeep-datta/swap_i3_workspaces',
        'Tracker': 'https://gitlab.com/sandeep-datta/swap_i3_workspaces/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
)
