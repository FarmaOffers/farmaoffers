odoo.define("farmaoffers_theme.checkout_pickup_toggle", [], function () {
  "use strict";

  const saveToOrder = async ({ pickup, branch_id }) => {
    try {
      await fetch("/fo/checkout/set_shipping", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pickup: !!pickup, branch_id: branch_id || null }),
      });
      return true;
    } catch (e) {
      console.error("Failed saving shipping selection", e);
      return false;
    }
  };

  const loadBranches = async (selectedId) => {
    const select = document.getElementById("fo_branch_select");
    if (!select) return;

    const res = await fetch("/fo/branches", { method: "GET" });
    const branches = await res.json();

    select.innerHTML = '<option value="">-SUCURSAL-</option>';

    for (const b of branches) {
      const opt = document.createElement("option");
      opt.value = b.id;
      opt.textContent = b.name;
      if (selectedId && String(b.id) === String(selectedId)) opt.selected = true;
      select.appendChild(opt);
    }
  };

  const setPickupUI = (pickup) => {
    const wrap = document.getElementById("fo_pickup_branch_wrap");
    if (wrap) wrap.classList.toggle("d-none", !pickup);

    const deliveryRow = document.getElementById("delivery_address_row");
    if (deliveryRow) deliveryRow.classList.toggle("d-none", pickup);
  };

  const run = async () => {
    const container = document.getElementById("fo_pickup_toggle");
    const rAddress = document.getElementById("fo_mode_address");
    const rPickup  = document.getElementById("fo_mode_pickup");
    const branchSel = document.getElementById("fo_branch_select");
    if (!container || !rAddress || !rPickup) return;

    const shippingMode = (container.dataset.shippingMode || "").trim();
    const branchId = (container.dataset.branchId || "").trim();

    const pickupInit = shippingMode === "branch";
    let isInitializing = true;

    // Establecer UI inicial basado en el estado del servidor
    rPickup.checked = pickupInit;
    rAddress.checked = !pickupInit;
    setPickupUI(pickupInit);

    // Cargar sucursales si está en modo pickup
    if (pickupInit) {
      try { 
        await loadBranches(branchId || null); 
      } catch (e) { 
        console.error(e); 
      }
    }

    // Marcar que la inicialización terminó
    setTimeout(() => {
      isInitializing = false;
    }, 100);

    // Event listeners
    rAddress.addEventListener("change", async () => {
      if (isInitializing) return;
      
      const ok = await saveToOrder({ pickup: false, branch_id: null });
      if (ok) {
        window.location.reload();
      }
    });

    rPickup.addEventListener("change", async () => {
      if (isInitializing) return;
      
      const branch_id = branchSel ? (branchSel.value || branchId || null) : (branchId || null);
      const ok = await saveToOrder({ pickup: true, branch_id });
      if (ok) {
        window.location.reload();
      }
    });

    if (branchSel) {
      branchSel.addEventListener("change", async () => {
        if (isInitializing) return;
        
        const branch_id = branchSel.value || null;
        const ok = await saveToOrder({ pickup: true, branch_id });
        if (ok) {
          window.location.reload();
        }
      });
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
});