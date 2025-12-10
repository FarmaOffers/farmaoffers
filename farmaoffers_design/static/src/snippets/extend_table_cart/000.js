/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.extend_table_cart = publicWidget.Widget.extend({
    selector: ".oe_cart",
    start() {
        console.log("extend_table_cart snippet loaded");
        this._bindEvents();
        return this._super(...arguments);
    },
    _bindEvents() {
        this.el.querySelectorAll(".remove-item").forEach(btn => {
            btn.addEventListener("click", ev => this._onRemoveItem(ev));
        });
        this.el.querySelectorAll(".update-qty").forEach(input => {
            input.addEventListener("change", ev => this._onUpdateQty(ev));
        });
    },
    async _onRemoveItem(ev) {
        ev.preventDefault();
        const lineId = ev.currentTarget.dataset.lineId;
        try {
            await rpc("/shop/cart/remove", { line_id: lineId });
            window.location.reload();
        } catch (error) {
            console.error("Error removing cart line:", error);
        }
    },
    async _onUpdateQty(ev) {
        ev.preventDefault();
        const lineId = ev.currentTarget.dataset.lineId;
        const quantity = ev.currentTarget.value;
        try {
            await rpc("/shop/cart/update", { line_id: lineId, quantity });
            window.location.reload();
        } catch (error) {
            console.error("Error updating quantity:", error);
        }
    },
});
