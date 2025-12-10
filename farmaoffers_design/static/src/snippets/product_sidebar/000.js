/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.product_sidebar = publicWidget.Widget.extend({
    selector: ".product_sidebar",
    start() {
        this._super.apply(this, arguments);
        const sidebar = this.$el.find(".fo-side-list ul li a");
        sidebar.on("click", (e) => {
            e.preventDefault();
            const href = $(e.currentTarget).attr("href");
            if (href && $(href).length) {
                $("html, body").animate({ scrollTop: $(href).offset().top }, 800);
            }
        });
        console.log("product_sidebar snippet loaded");
    },
});