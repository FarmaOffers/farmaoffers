# -*- coding: utf-8 -*-
from . import controllers
from . import models

from odoo.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(env):
    import os
    import json
    from pynpm import NPMPackage
    from os.path import dirname, join

    destination_dir = join(dirname(__file__), 'node_sdk')
    package_json_path = join(destination_dir, 'package.json')

    if os.path.exists(package_json_path):
        with open(package_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data.get("type") == "module":
            data.pop("type")
            with open(package_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

        pkg = NPMPackage(package_json_path)
        pkg.install()
        pkg.run_script('build')

    setup_provider(env, 'yappy')


def uninstall_hook(env):
    reset_payment_provider(env, 'yappy')
