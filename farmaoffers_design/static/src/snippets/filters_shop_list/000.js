/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.filters_shop_list = publicWidget.Widget.extend({
    selector: ".filters_shop_list",
    start() {
        console.log("filters_shop_list snippet loaded");

        this.el.querySelectorAll(".fo-side-list ul li a").forEach((link) => {
            link.addEventListener("click", (e) => {
                e.preventDefault();
                const targetId = link.getAttribute("href");
                const target = document.querySelector(targetId);
                if (target) {
                    window.scrollTo({
                        top: target.offsetTop - 80,
                        behavior: "smooth",
                    });
                }
            });
        });

        return this._super(...arguments);
    },
});
