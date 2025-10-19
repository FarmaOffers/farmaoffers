/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import Splide from "@web/../splide.min.js";

publicWidget.registry.t_owl_carousel = publicWidget.Widget.extend({
    selector: ".t_owl_carousel",
    start() {
        console.log("t_owl_carousel snippet loaded (Splide)");

        const element = this.el.querySelector("#t_owl_carousel_splide");
        if (element) {
            new Splide(element, {
                type: "loop",
                perPage: 3,
                gap: "1rem",
                autoplay: true,
                pauseOnHover: true,
                breakpoints: {
                    992: { perPage: 2 },
                    768: { perPage: 1 },
                },
            }).mount();
        }

        return this._super(...arguments);
    },
});
