from odoo import fields, models

class SaleReport(models.Model):
    _inherit = "sale.report"

    standard_price = fields.Float(string="Costo Productos Unitario", readonly=True, group_operator="avg")
    total_cost = fields.Float(string="Total costo", readonly=True, group_operator="sum")
    total_margin = fields.Float(string="Margen total", readonly=True, group_operator="sum")
    total_no_discount = fields.Float(string="Total libre de impuesto sin descuento", readonly=True, group_operator="sum")
    total_incl_no_discount = fields.Float(string="Total sin descuento", readonly=True, group_operator="sum")

    def _select_sale(self):
        res = super()._select_sale()
        res += (
            ", (p.standard_price::numeric) AS standard_price"
            ", SUM(l.qty_delivered * (p.standard_price::numeric)) AS total_cost"
            ", (SUM(l.price_total) - SUM(l.qty_delivered * (p.standard_price::numeric))) AS total_margin"
            ", SUM(l.price_total + ((l.price_unit * l.product_uom_qty * l.discount / 100.0 / "
            "   CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END))) AS total_incl_no_discount"
            ", SUM(l.price_subtotal + ((l.price_unit * l.product_uom_qty * l.discount / 100.0 / "
            "   CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END))) AS total_no_discount"
        )
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += ", (p.standard_price::numeric)"
        return res

    def _select_pos(self):
        res = super()._select_pos()
        res += (
            ", (p.standard_price::numeric) AS standard_price"
            ", SUM(l.qty * (p.standard_price::numeric)) AS total_cost"
            ", (SUM(l.price_subtotal_incl) / MIN(CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END)"
            "   - SUM(l.qty * (p.standard_price::numeric))) AS total_margin"
            ", SUM(l.price_subtotal_incl + ((l.price_unit * l.qty * l.discount / 100.0 / "
            "   CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END)))"
            "   / MIN(CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END) AS total_incl_no_discount"
            ", SUM(l.price_subtotal + ((l.price_unit * l.qty * l.discount / 100.0 / "
            "   CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END)))"
            "   / MIN(CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END) AS total_no_discount"
        )
        return res

    def _group_by_pos(self):
        res = super()._group_by_pos()
        res += ", (p.standard_price::numeric)"
        return res
