'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 12:47:58
 # Thanks to https://mike.depalatis.net/blog/simplifying-argparse.html
'''
import argparse
import os
import sys as _sys
import webbrowser

from dashtools.cli import update
from dashtools.deploy import deployHeroku
from dashtools.docker import dockerUtils
from dashtools.runtime import runtimeUtils
from dashtools.templating import buildApp, buildAppUtils, createTemplate
from dashtools.version import __version__


class MyArgumentParser(argparse.ArgumentParser):
    """Override default help message"""

    def print_help(self, file=None):
        if file is None:
            file = _sys.stdout
        message = f"""The dashtools v{__version__} CLI for Plotly Dash. See https://github.com/andrew-hossack/dash-tools for more details.
\nUsage:
    {'dashtools <command> [options]':<29}
\nCommands and Options:
    {'docker':<29}Handle Docker creation. Choose option:
        {'--init <image name>':<25}Creates a docker image in current directory

    {'heroku':<29}Handle Heroku deployment. Choose option:
        {'--deploy':<25}Deploys the current project to Heroku
        {'--update [remote name]':<25}Push changes to existing Heroku remote

    {'init <app name> [template]':<29}Create a new app
        {'--dir, -d':<25}Specify alternative create location

    {'run':<29}Run the app (experimental)
        {'--set-py-cmd <command>':<25}Set the python shell command

    {'templates':<29}List and create templates
        {'--init <directory>':<25}Creates a template from specified directory
        {'--list':<25}List available templates
\nOther Options:
    {'--help, -h':<29}Display help message
    {'--report-issue':<29}Report a bug or issue
    {'--version, -v':<29}Display version
"""
        file.write(message+"\n")


parser = MyArgumentParser()

parser._positionals.title = 'Positional Arguments'
parser._optionals.title = 'Optional Arguments'

subparsers = parser.add_subparsers(dest="subcommand")


def argument(*name_or_flags, **kwargs):
    """Convenience function to properly format arguments to pass to the
    subcommand decorator.
    """
    return (list(name_or_flags), kwargs)


def subcommand(args=[], parent=subparsers):
    """Decorator to define a new subcommand in a sanity-preserving way.
    The function will be stored in the ``func`` variable when the parser
    parses arguments so that it can be called directly like so::
        args = cli.parse_args()
        args.func(args)
    Usage example::
        @subcommand([argument("-d", help="Enable debug mode", action="store_true")])
        def subcommand(args):
            print(args)
    Then on the command line::
        $ python cli.py subcommand -d
    """
    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)
    return decorator


parser.add_argument(
    '-v',
    '--version',
    action='version',
    version=f'dashtools {__version__}')

parser.add_argument(
    '--report-issue',
    action='store_true',
    help='Report a bug or issue')


@subcommand(
    [
        argument(
            '--init',
            help='Create a new docker image for the current project',
            metavar='<image name>',
            nargs=1
        ),
    ])
def docker(args):
    """Initialize a new docker image for the current project."""
    if args.init:
        dockerUtils.create_image(
            image_name=args.init[0],
            cwd=os.getcwd()
        )
    else:
        print('dashtools: docker: error: Too few arguments')
        exit('dashtools: Available docker options: --init [--dir, -d]')


@ subcommand(
    [
        argument(
            "init",
            help='Create a new Dash app. Args: REQUIRED: <app name> OPTIONAL: <template> (Default: "default").',
            metavar='<app name> [<template>]',
            nargs='+'),
        argument(
            '--dir',
            '-d',
            help='Specify the directory to create the app in. Args: REQUIRED: <directory>',
            default=os.getcwd(),
            metavar='<directory>',
            nargs='?')
    ])
def init(args):
    """Initialize a new app."""
    if args.dir is None:
        print('dashtools: init: No directory specified. Usage Example: dashtools init MyDashApp -d ~/Desktop')
        exit('dashtools: init: Failed')
    buildApp.create_app(
        target_dir=args.dir,
        app_name=args.init[0],
        template=buildAppUtils.get_template_from_args(args))
    print(
        f'dashtools: Run your app using the "python {os.path.join(args.init[0], "src", "app.py")}" command')
    print(f'dashtools: For an in-depth guide on configuring your app, see https://dash.plotly.com/layout')


@ subcommand(
    [
        argument(
            "--list",
            help="List available templates",
            default=False,
            action="store_true"),
        argument(
            "--init",
            help="Convert directory to a template. Args: REQUIRED: <directory to convert>",
            nargs=1),
    ])
def templates(args):
    if args.list:
        print('dashtools: Templates usage example, type: dashtools init MyApp csv')
        print('dashtools: templates: List of available templates:')
        buildAppUtils.print_templates()
    elif args.init:
        createTemplate.create_template(src=args.init[0], dest=os.getcwd())
    else:
        print('dashtools: templates error: too few arguments')
        print('dashtools: For more information on templates, see https://github.com/andrew-hossack/dash-tools#templates')
        exit('dashtools: Available templates options: --list, --init')


@ subcommand(
    [
        argument(
            "--deploy",
            help="Deploys the current project to Heroku. Run command from the root of the project",
            default=False,
            action="store_true",
        ),
        argument(
            "--update",
            help="Updates the current project to Heroku. Run command from the root of the project. Args: OPTIONAL: <git remote>",
            nargs="?",
            const="heroku",
            type=str
        ),
    ])
def heroku(args):
    if args.deploy:
        deployHeroku.deploy_app_to_heroku(os.getcwd())
    elif args.update:
        deployHeroku.update_heroku_app(os.getcwd(), remote=args.update)
    else:
        print('dashtools: heroku error: too few arguments')
        exit('dashtools: Available heroku options: --deploy, --update')


@ subcommand(
    [
        argument(
            "run",
            help="Run the app locally. Uses Procfile if available, else recursive search for app.py",
            default=False,
            action="store_true"),
        argument(
            '--set-py-cmd',
            help='Set the python shell command. Args: REQUIRED: <python shell command>',
            metavar='<python shell command>',
            nargs=1)
    ])
def run(args):
    if args.set_py_cmd:
        runtimeUtils.set_python_shell_cmd(args.set_py_cmd[0])
    elif args.run:
        try:
            runtimeUtils.run_app(os.getcwd())
        except RuntimeError as e:
            print(e)
            exit('dashtools: run: Failed')


def main():
    """
    dashtools CLI entry point.
    """
    args = parser.parse_args()
    if args.subcommand:
        args.func(args)
    elif args.report_issue:
        print('dashtools: Report an issue at: https://github.com/andrew-hossack/dash-tools/issues/new/choose')
        if input('dashtools: Open in browser? (y/n) > ') == 'y':
            webbrowser.open(
                'https://github.com/andrew-hossack/dash-tools/issues/new/choose')
    else:
        parser.print_help()
    update.check_for_updates()
