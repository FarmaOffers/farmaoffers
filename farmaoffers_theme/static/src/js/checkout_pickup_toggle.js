odoo.define('farmaoffers_theme.checkout_pickup_toggle', function () {
  "use strict";

  document.addEventListener('DOMContentLoaded', () => {
    const rAddress = document.getElementById('fo_mode_address');
    const rPickup  = document.getElementById('fo_mode_pickup');

    if (!rAddress || !rPickup) return;

    const updateUrlAndReload = (pickup) => {
      const url = new URL(window.location.href);
      if (pickup) url.searchParams.set('pickup', '1');
      else url.searchParams.delete('pickup');
      window.location.href = url.toString();
    };

    rAddress.addEventListener('change', () => updateUrlAndReload(false));
    rPickup.addEventListener('change', () => updateUrlAndReload(true));
  });
});
