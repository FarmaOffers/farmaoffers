/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
// import Splide from "@web/../splide.min.js";

publicWidget.registry.card_client_reviews = publicWidget.Widget.extend({
    selector: ".card_client_reviews",
    start() {
        console.log("card_client_reviews snippet loaded (Splide)");
        const element = this.el.querySelector("#client_reviews_splide");
        if (element) {
            new Splide(element, {
                type: "loop",
                perPage: 3,
                gap: "1.5rem",
                autoplay: true,
                pauseOnHover: true,
                pagination: true,
                arrows: true,
                breakpoints: {
                    992: { perPage: 2 },
                    768: { perPage: 1 },
                },
            }).mount();
        }
        return this._super(...arguments);
    },
});
