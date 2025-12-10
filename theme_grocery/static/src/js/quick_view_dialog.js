/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import publicWidget from "@web/legacy/js/public/public_widget";
import { WebsiteSale } from "@website_sale/js/website_sale";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.WebsiteSaleQuickView = WebsiteSale.extend({
    selector: ".oe_website_sale",
    events: Object.assign({}, WebsiteSale.prototype.events, {
        "click .p_quick_view, .tp-product-quick-view-small-btn": "_onQuickView",
    }),

    async _onQuickView(ev) {
        ev.preventDefault();
        const productId = parseInt(ev.currentTarget.dataset.productId);

        const $target = $(".quick_view_pop_up_p_detail");

        // Show loading spinner
        $target.html(`
            <div class="d-flex justify-content-center align-items-center" style="height:200px;">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `);

        try {
            const data = await rpc("/add/quick/views/popup", { product_id: productId });
            $target.html(data.data);

            $(".quick_view_pop_up_p_detail .js_main_product [data-attribute_exclusions]")
                .trigger("change");

            $("#product_quick_views_popup").modal("show");
        } catch (err) {
            console.error("Quick view failed:", err);
            $target.html(`<div class="text-danger">Error loading product.</div>`);
        }
    },
});
