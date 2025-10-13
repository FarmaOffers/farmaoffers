/** @odoo-module **/

import { registry } from "@web/core/registry";

console.log("✅ Stripe Info snippet JS loaded!");  // 👈 Prueba de carga

registry.category("website_snippets").add("farmaoffers_design.stripe_info_snippet", {
    name: "Stripe Info",
    template: "farmaoffers_design.stripe_info_snippet",
    category: "Structure", // más visible que "Custom"
});