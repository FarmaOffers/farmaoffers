/** @odoo-module **/

import { registry } from "@web/core/registry";

registry.category("website_snippets").add("farmaoffers_design.stripe_info_snippet", {
    name: "Stripe Info",
    template: "farmaoffers_design.stripe_info_snippet",
    category: "Structure", // más visible que "Custom"
});

