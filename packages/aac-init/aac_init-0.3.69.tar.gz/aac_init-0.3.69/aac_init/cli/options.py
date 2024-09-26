# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>

import click


yaml_dir_path = click.option(
    '--data',
    '-d',
    type=click.Path(),
    required=True,
    help='Path to aac-init YAML data files.'
)

# log_help = "Specify the logging level. Choose from: debug, info, warning, error, critical."
log_help = """
    Specify the logging level. Default setting is 'info'.
    Available levels: debug, info, warning, error, critical.
"""

log_level = click.option(
    '--log-level',
    '-l',
    type=click.Choice(['debug', 'info', 'warning', 'error', 'critical'], case_sensitive=False),
    default='info',
    show_default=True,
    help=log_help
)
