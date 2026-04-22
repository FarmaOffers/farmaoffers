/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.mobileCategoryMenu = publicWidget.Widget.extend({
    selector: '.category-main-option-menu',

    events: {
        'click .category-main-trigger': '_toggleMain',
        'click .toggle-child-btn': '_toggleChild',
    },

    start() {
        return this._super(...arguments);
    },

    _toggleMain(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        this.el.classList.toggle('open');
    },

    _toggleChild(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        const item = ev.currentTarget.closest('.category-header-mobile');
        if (!item) {
            return;
        }

        item.classList.toggle('open');
    },
});