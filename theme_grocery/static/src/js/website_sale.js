/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";
import wSaleUtils from "@website_sale/js/website_sale_utils";
import "@website_sale/js/website_sale"; // ensures WebsiteSale is loaded

publicWidget.registry.WebsiteSale.include({
    /**
     * Override: Update quantity in cart
     */
    async _changeCartQuantity($input, value, $dom_optional, line_id, productIDs) {
        $dom_optional.each((i, elem) => {
            const $qty = $(elem).find(".js_quantity");
            if ($qty.is("input")) {
                $qty.val(value);
            } else {
                $qty.text(value);
            }
            productIDs.push($(elem).find("span[data-product-id]").data("product-id"));
        });

        $input.data("update_change", true);

        // ✅ FIX: Correct rpc usage
        const data = await rpc("/shop/cart/update_json", {
            line_id,
            product_id: parseInt($input.data("product-id"), 10),
            set_qty: value,
        });

        $input.data("update_change", false);

        let check_value = parseInt($input.val() || 0, 10);
        if (isNaN(check_value)) {
            check_value = 1;
        }
        if (value !== check_value) {
            $input.trigger("change");
            return;
        }
        if (!data.cart_quantity) {
            window.location = "/shop/cart";
            return;
        }

        wSaleUtils.updateCartNavBar(data);

        // Update main input
        $input.val(data.quantity);

        // Update all quantity fields for this line
        const $qty = $(`.js_quantity[data-line-id=${line_id}]`);
        if ($qty.is("input")) {
            $qty.val(data.quantity);
        } else {
            $qty.text(data.quantity);
        }

        // Update navbar cart
        $("#my_cart").html(data.cart_quantity).hide().fadeIn(600);
        $(".price-minicart .price").html(data.cart_amount).hide().fadeIn(600);

        // Show warnings if any
        if (data.warning) {
            let cart_alert = $(".oe_cart").parent().find("#data_warning");
            if (!cart_alert.length) {
                $(".oe_cart").prepend(
                    `<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                        ${data.warning}
                    </div>`
                );
            } else {
                cart_alert.html(
                    `<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                    ${data.warning}`
                );
            }
            $input.val(data.quantity);
        }
    },
    onClickAddCartJSON: function (ev) {
        ev.preventDefault();
        ev.stopImmediatePropagation(); 
        var $link = $(ev.currentTarget);
        var $input = $link.closest('.input-group').find("input");
        var min = parseFloat($input.data("min") || 0);
        var max = parseFloat($input.data("max") || Infinity);
        var previousQty = parseFloat($input.val() || 0, 10);
        var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
        var newQty = quantity > min ? (quantity < max ? quantity : max) : min;

        if (newQty !== previousQty) {
            $input.val(newQty).trigger('change');
        }
        return false;
    },

    /**
     * Override: Submit optional products modal
     */
    async _onModalSubmit(goToShop) {
        const productAndOptions = JSON.stringify(
            this.optionalProductsModal.getSelectedProducts()
        );

        const data = await rpc("/shop/cart/update_option", {
            product_and_options: productAndOptions,
        });

        if (goToShop) {
            window.location.pathname = "/shop/cart";
        }

        const res = JSON.parse(data);
        $("#my_cart").html(res.cart_quantity).hide().fadeIn(600);
        $(".price-minicart .price").html(res.cart_amount).hide().fadeIn(600);
    },
});
