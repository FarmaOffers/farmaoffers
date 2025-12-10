/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.section_same_compound = publicWidget.Widget.extend({
    selector: ".section_same_compound",
    start() {
        this._bindEvents();
        console.log("section_same_compound snippet loaded");
    },

    _bindEvents() {
        this.el.querySelector("#show-more-with-same-compound")?.addEventListener("click", (e) => {
            e.preventDefault();
            this._toggleProducts();
        });
    },

    _toggleProducts() {
        const compound = this.el.querySelector("#current_product_compound")?.textContent.trim();
        const productId = this.el.querySelector(".product_template_id")?.value;
        const button = this.el.querySelector("#show-more-with-same-compound");
        const ul = this.el.querySelector("#ul-same-compound");

        if (!compound || !productId) return;

        let limit = undefined;
        let text = "Desplegar menos";
        if (button.innerText !== "Desplegar más") {
            limit = 3;
            text = "Desplegar más";
        }

        rpc("/products/same-compounds",{
            params: {
                exception: productId,
                compound: compound,
                limit: limit,
            },
        }).then((products) => {
            ul.innerHTML = "";
            products.forEach((element) => {
                const li = document.createElement("li");
                li.classList.add("font-montserrat", "font-size-cards", "mb-2");
                li.innerHTML = `<a itemprop="name" href="${element.website_url}" content="${element.name}">${element.name}</a>`;
                ul.appendChild(li);
            });
            button.innerText = text;
        });
    },
});