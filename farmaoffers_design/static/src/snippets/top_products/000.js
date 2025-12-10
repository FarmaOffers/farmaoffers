/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TopProductsSnippet = publicWidget.Widget.extend({
    selector: '.top_products',
    start() {
        $(".top_products .owl-carousel").owlCarousel({
            loop: false,
            nav: true,
            dots: false,
            autoplay: false,
            autoplayHoverPause: true,
            margin: 0,
            navText: [
                "<i class='fa fa-angle-double-left h3 text-primary mr-2'></i>",
                "<i class='fa fa-angle-double-right h3 text-secondary'></i>"
            ],
            responsive: {
                0: { items: 2 },
                480: { items: 2 },
                768: { items: 4 },
                991: { items: 5 },
                1200: { items: 5 }
            }
        });
        return this._super.apply(this, arguments);
    },
})