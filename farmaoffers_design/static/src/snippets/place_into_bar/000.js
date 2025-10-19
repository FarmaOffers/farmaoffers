/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.place_into_bar = publicWidget.Widget.extend({
    selector: ".place_into_bar",
    start() {
        console.log("place_into_bar snippet loaded");
    },
});
