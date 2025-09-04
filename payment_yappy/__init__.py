# -*- coding: utf-8 -*-
from . import models
from . import controllers


def _post_init_hook(cr, registry):
    import shutil
    import os
    from pynpm import NPMPackage
    from os.path import dirname

    source_dir = dirname(__file__) + '/node_sdk'
    destination_dir = os.path.expanduser('~') + '/node_sdk'

    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)

    pkg = NPMPackage(destination_dir + '/package.json')
    pkg.install()
    pkg.run_script('build')


def uninstall_hook(cr, registry):
    """En Odoo 18 no existe reset_payment_provider, así que
    en desinstalación podemos simplemente eliminar el registro del provider si hace falta."""
    from odoo.api import Environment

    env = Environment(cr, 1, {})  # usuario admin
    provider = env['payment.provider'].search([('code', '=', 'yappy')])
    if provider:
        provider.unlink()