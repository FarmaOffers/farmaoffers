/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CarouselFix = publicWidget.Widget.extend({
    selector: '#homepageCarousel',

    start: function () {
        const carousel = this.el;
        const indicatorsContainer = carousel.querySelector('.carousel-indicators');
        const items = carousel.querySelectorAll('.carousel-item');

        // Ensure indicators exist and match slides
        indicatorsContainer.innerHTML = '';
        items.forEach((item, i) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.setAttribute('data-bs-target', '#homepageCarousel');
            btn.setAttribute('data-bs-slide-to', i);
            btn.setAttribute('aria-label', `Slide ${i + 1}`);
            if (i === 0) {
                btn.classList.add('active');
                btn.setAttribute('aria-current', 'true');
            }
            indicatorsContainer.appendChild(btn);
        });

        // Listen to slide changes to update indicators
        carousel.addEventListener('slid.bs.carousel', function (e) {
            const activeIndex = e.to;
            const allIndicators = indicatorsContainer.querySelectorAll('button');
            allIndicators.forEach((btn, idx) => {
                btn.classList.toggle('active', idx === activeIndex);
                btn.setAttribute('aria-current', idx === activeIndex ? 'true' : 'false');
            });
        });

        return this._super.apply(this, arguments);
    },
});
