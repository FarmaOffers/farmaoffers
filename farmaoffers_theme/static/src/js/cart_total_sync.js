/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.FarmaoffersCartTotalSync = publicWidget.Widget.extend({
    selector: '.minicart-header',

    start() {
        if (window.__farmaoffersCartSyncInitialized) {
            return this._super(...arguments);
        }
        window.__farmaoffersCartSyncInitialized = true;

        this._boundClickHandler = this._onBodyClick.bind(this);
        document.body.addEventListener("click", this._boundClickHandler);

        return this._super(...arguments);
    },

    destroy() {
        if (this._boundClickHandler) {
            document.body.removeEventListener("click", this._boundClickHandler);
        }
        return this._super(...arguments);
    },

    async _onBodyClick(ev) {
        const addToCartBtn = ev.target.closest(
            'a[href*="/shop/cart/update"], form[action*="/shop/cart/update"] button, .a-submit, #add_to_cart, .o_we_buy_now, .js_check_product, .js_add_cart_json'
        );

        if (!addToCartBtn) {
            return;
        }

        let previousQty = null;

        try {
            previousQty = await rpc("/shop/cart/header_info", {});
        } catch (error) {
            console.error("[CartSync] Error reading previous header info:", error);
        }

        setTimeout(async () => {
            let newInfo = null;

            try {
                newInfo = await rpc("/shop/cart/header_info", {});
            } catch (error) {
                console.error("[CartSync] Error reading new header info:", error);
            }

            if (!previousQty || !newInfo) {
                return;
            }

            if (previousQty.quantity === newInfo.quantity) {
                return;
            }

            this._updateMiniCart(newInfo);
        }, 1000);
    },

    _updateMiniCart(info) {
        if (!info) {
            return;
        }

        document.querySelectorAll(".my_cart_quantity").forEach((el) => {
            el.textContent = info.quantity ?? 0;
        });

        document.querySelectorAll(".my_cart_total").forEach((el) => {
            el.textContent = info.amount_total_formatted ?? "0.00";
        });

    },
});