/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.fo_cart_lines = publicWidget.Widget.extend({
    selector: ".fo_cart_lines",
    start() {
        console.log("fo_cart_lines snippet loaded");
    },
});
