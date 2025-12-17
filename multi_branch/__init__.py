# See LICENSE file for full copyright and licensing details.
"""Imports all The python files."""

from . import models
from . import wizard
from odoo import api, SUPERUSER_ID


def _disable_security_rules(env):
    """Hook method, used to disable security rules."""
    # env = api.Environment(cr, SUPERUSER_ID, {})
    sale_own_rule_id = env.ref("sale.sale_order_personal_rule")
    sale_rule_id = env.ref("sale.sale_order_see_all")
    sale_order_line_rule_id = env.ref("sale.sale_order_line_see_all")
    crm_rule_id = env.ref("crm.crm_rule_all_lead")
    crm_activity_report_id = env.ref("crm.crm_activity_report_rule_all_activities")
    account_move_see_all_id = env.ref("account.account_move_see_all")
    account_move_rule_id = env.ref("account.account_move_rule_group_invoice")

    po_user_moves = env.ref("purchase.purchase_user_account_move_rule")
    readonly_moves = env.ref("account.account_move_rule_group_readonly")
    all_invs_rule = env.ref("sale.account_invoice_rule_see_all")
    personal_invs_rule = env.ref("sale.account_invoice_rule_see_personal")

    if sale_own_rule_id:
        sale_own_rule_id.update(
            {
                "domain_force": """['|', ('branch_id', '=', False),
                         ('branch_id', 'in', [branch.id for branch in user.branch_ids]),
                         ('user_id', 'in', [user.id, False])
                         ]"""
            }
        )
    if sale_rule_id:
        sale_rule_id.write({"active": False})

    if sale_order_line_rule_id:
        sale_order_line_rule_id.write({"active": False})

    if crm_rule_id:
        crm_rule_id.write({"active": False})

    if crm_activity_report_id:
        crm_activity_report_id.write({"active": False})

    if account_move_rule_id:
        account_move_rule_id.write({"active": False})

    if account_move_see_all_id:
        account_move_see_all_id.write({"active": False})

    if all_invs_rule:
        all_invs_rule.write({"active": False})

    if personal_invs_rule:
        personal_invs_rule.write({"active": False})

    if readonly_moves:
        readonly_moves.write({"active": False})

    if po_user_moves:
        po_user_moves.write({"active": False})


def _enable_security_rules(env):
    """Hook method, used to enable security rules."""
    # env = api.Environment(cr, SUPERUSER_ID, {})
    sale_rule_id = env.ref("sale.sale_order_see_all")
    crm_rule_id = env.ref("crm.crm_rule_all_lead")
    crm_activity_report_id = env.ref("crm.crm_activity_report_rule_all_activities")
    sale_order_line_rule_id = env.ref("sale.sale_order_line_see_all")
    account_move_see_all_id = env.ref("account.account_move_see_all")
    account_move_rule_id = env.ref("account.account_move_rule_group_invoice")
    sale_own_rule_id = env.ref("sale.sale_order_personal_rule")

    po_user_moves = env.ref("purchase.purchase_user_account_move_rule")
    readonly_moves = env.ref("account.account_move_rule_group_readonly")
    all_invs_rule = env.ref("sale.account_invoice_rule_see_all")
    personal_invs_rule = env.ref("sale.account_invoice_rule_see_personal")

    if sale_own_rule_id:
        sale_own_rule_id.update(
            {
                "domain_force": """['|',('user_id','=',user.id),
            ('user_id','=',False)]"""
            }
        )

    if sale_rule_id:
        sale_rule_id.write({"active": True})

    if sale_order_line_rule_id:
        sale_order_line_rule_id.write({"active": True})

    if crm_rule_id:
        crm_rule_id.write({"active": True})

    if crm_activity_report_id:
        crm_activity_report_id.write({"active": True})

    if account_move_rule_id:
        account_move_rule_id.write({"active": True})

    if account_move_see_all_id:
        account_move_see_all_id.write({"active": True})

    if all_invs_rule:
        all_invs_rule.write({"active": True})

    if personal_invs_rule:
        personal_invs_rule.write({"active": True})

    if readonly_moves:
        readonly_moves.write({"active": True})

    if po_user_moves:
        po_user_moves.write({"active": True})
