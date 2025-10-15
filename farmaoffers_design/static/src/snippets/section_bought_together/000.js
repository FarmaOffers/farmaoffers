/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { loadJS } from "@web/core/assets";

publicWidget.registry.section_bought_together = publicWidget.Widget.extend({
    selector: ".section_bought_together",
    async start() {
        await this._initCarousel();
        console.log("section_bought_together snippet loaded");
    },

    async _initCarousel() {
        try {
            // Ensure Owl Carousel is available globally
            if (typeof $.fn.owlCarousel === "undefined") {
                await loadJS("/farmaoffers_design/static/lib/owl.carousel.min.js");
            }

            const carousel = this.el.querySelector(".owl-carousel");
            if (carousel) {
                $(carousel).owlCarousel({
                    loop: false,
                    nav: true,
                    dots: false,
                    autoplay: false,
                    autoplayHoverPause: true,
                    margin: 30,
                    navText: [
                        "<i class='fa fa-angle-double-left h3 text-primary mr-2'></i>",
                        "<i class='fa fa-angle-double-right h3 text-secondary'></i>"
                    ],
                    responsive: {
                        0: { items: 1 },
                        480: { items: 2 },
                        768: { items: 3 },
                        991: { items: 3 },
                        1200: { items: 3 }
                    },
                });
            }
        } catch (error) {
            console.error("Error initializing bought-together carousel:", error);
        }
    },
});