# See LICENSE file for full copyright and licensing details.

{
    "name": "Multi Branch",
    "version": "18.0.1.0.1",  # bump para forzar actualización
    "license": "LGPL-3",
    "category": "Extra Tools",
    "sequence": 1,
    "summary": "Multiple Branch Management for single company, Assign One Or Multiple Branch to user, Branch Management.",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",

    # Dependencies (incluye payment por cambios de acquirer->provider en v18)
    "depends": [
        "base",
        "payment",
        "account",
        "account_accountant",
        "sale_management",
        "crm",
        "sale_stock",
        "purchase_stock",
        "stock",
    ],

    # Data load order dentro del módulo
    "data": [
        "security/multi_branch_security.xml",
        "security/ir.model.access.csv",
        "wizard/wiz_branch_warehouse_view.xml",
        "report/sale_report_templates.xml",
        "report/purchase_order_templates.xml",
        "report/report_invoice.xml",
        "report/report_stockpicking_operations.xml",
        "report/report_payment_receipt_templates.xml",
        "views/multi_branch_view.xml",
        "views/res_users_view.xml",
        "views/sale_order_view.xml",
        "views/stock_warehouse_view.xml",
        "views/account_invoice_view.xml",
        "views/stock_picking_view.xml",
        "views/account_payment.xml",
        "views/purchase_order_view.xml",
        "views/stock_location_view.xml",
        "views/account_bank_statement_view.xml",
        "views/crm_lead_view.xml",
    ],

    "images": ["static/description/odoo-app-banner-multi-branch.jpg"],
    "live_test_url": "https://www.youtube.com/watch?v=mnbG1Lo0NGA",

    "installable": True,
    "application": True,
    "auto_install": False,

    "post_init_hook": "_disable_security_rules",
    "uninstall_hook": "_enable_security_rules",

    "price": 79,
    "currency": "EUR",
}
