/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.FarmaoffersCarousel = publicWidget.Widget.extend({
  selector: ".t_owl_carousel",

  start() {
    const mode = this.el.dataset.carouselType || "default";

    let target = this.el.querySelector(".splide");

    if (!target) {
      console.warn("No se encontró Splide en este bloque:", this.el);
      return this._super(...arguments);
    }

    const baseOptions = {
      type: "loop",
      autoplay: true,
      interval: 2500,
      pauseOnHover: true,
      arrows: true,
      pagination: true,
      gap: "1rem",
    };

    const config = {
      default: {
        perPage: 3,
      },
      homepage: {
        perPage: 1,
      },
      offers: {
        perPage: 4,
        arrows: false,
      },
      products: {
        perPage: 4,
        arrows: false,
      },
      our_tips: {
        perPage: 4,
        arrows: false,
      },
      client_reviews: {
        perPage: 3,
        arrows: false,
      },
    };

    const options = Object.assign(
      {},
      baseOptions,
      config[mode] || config.default
    );

    if (window.Splide) {
      new Splide(target, options).mount();
    } else {
      console.error("Splide no está disponible en window.Splide");
    }

    return this._super(...arguments);
  },
});
