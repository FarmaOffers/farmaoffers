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

        std_price = "COALESCE((p.standard_price->>(s.company_id::text))::numeric, 0)"

        res += (
            f", {std_price} AS standard_price"
            f", SUM(l.qty_delivered * {std_price}) AS total_cost"
            f", (SUM(l.price_total) - SUM(l.qty_delivered * {std_price})) AS total_margin"
            ", SUM(l.price_total + ((l.price_unit * l.product_uom_qty * l.discount / 100.0 / "
            "   CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END))) AS total_incl_no_discount"
            ", SUM(l.price_subtotal + ((l.price_unit * l.product_uom_qty * l.discount / 100.0 / "
            "   CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END))) AS total_no_discount"
        )
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        # debe ser la misma expresión del SELECT (sin SUM/AVG)
        res += ", COALESCE((p.standard_price->>(s.company_id::text))::numeric, 0)"
        return res

    def _select_pos(self):
        res = super()._select_pos()

        res += ", NULL::integer as branch_id"

        std_price = "COALESCE((p.standard_price->>(pos.company_id::text))::numeric, 0)"

        res += (
            f", {std_price} AS standard_price"
            f", SUM(l.qty * {std_price}) AS total_cost"
            ", (SUM(l.price_subtotal_incl) / MIN(CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END)"
            f"   - SUM(l.qty * {std_price})) AS total_margin"
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
        res += ", COALESCE((p.standard_price->>(pos.company_id::text))::numeric, 0)"
        return res
