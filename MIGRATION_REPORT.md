# Informe de migración (Odoo 14 -> Odoo 18) — farmaoffers

Resumen rápido
- Escaneo inicial del addon completado. El código está mayoritariamente compatible con API moderna de Odoo (uso de `odoo` imports y `api`).
- Se detectaron áreas que requieren atención antes de intentar instalación en Odoo 18: manifests, firmas de métodos/super, y algunas prácticas que conviene simplificar para evitar conflictos.

Hallazgos concretos
- Manifests
  - `farmaoffers_design/__manifest__.py` tiene `'version': '14.0.11'`. Actualizar el manifiesto a formato y versión compatibles con Odoo 18 (por convención usar `18.0.x.y` o `18.0.1.0.0`) y validar que todas las dependencias sigan existiendo en v18.
  - `theme_grocery/__manifest__.py` ya muestra `"version": "18.0.0.1"` — OK.

- Modelos Python
  - Uso extensivo de `browse()` y `search()` (válido). Revisar lugares donde se asume que `browse(id)` siempre devuelve registro existente — usar `.exists()` o comprobar.
  - Algunos modelos definen `_name = 'product.template'` y `_inherit = "product.template"`. Para extender modelos existentes, basta con `_inherit = 'product.template'` (quitar `_name`) para evitar definir un nuevo model con el mismo nombre.
  - No se encontraron decoradores obsoletos `@api.one` o `@api.multi`, ni imports de `openerp`. Buen indicador.
  - Firmas de métodos que llaman `super()` (en controllers y modelos relacionados con website/pos) deben verificarse frente a las firmas actuales de Odoo 18: parámetros añadidos/removidos pueden romper la llamada a `super()`. Revisar especialmente controladores en `controllers.py` y métodos sobrescritos en `sale_report.py`, `pos_order.py`, `delivery_carrier.py`.

- Vistas / QWeb / Assets
  - Los manifests incluyen `assets` que parecen compatibles con Odoo 18. Sin embargo, las templates QWeb pueden requerir ligeras adaptaciones si usaban helpers/variables que cambiaron en v18.
  - Archivos SCSS/JS listos para revisión — validar rutas y que no usen APIs JS obsoletas.

- Posibles riesgos
  - Dependencias: algunos items en `depends` pueden haber cambiado de nombre o modularización en v18 (ej.: `website_sale_delivery` u otros submódulos). Confirmar que todos los módulos dependientes existen en la instancia Odoo 18.
  - Cambios en APIs internas de website/pos: revisar logs al intentar instalar para detectar firmas incompatibles.

Recomendaciones y plan de trabajo (pasos siguientes)
1. Actualizar manifests:
   - Cambiar `version` en `farmaoffers_design/__manifest__.py` a formato Odoo 18 (ej. `18.0.1.0.0`).
   - Revisar y validar la lista `depends`, eliminar/ajustar dependencias inexistentes en v18.
2. Refactor Python mínimo:
   - Remover `_name` cuando se usa solo `_inherit` para extender modelos (ej.: `product.template`, `res.company`).
   - En métodos que usan `browse(id)`, reemplazar por `env['model'].browse(id).exists()` si se depende de existencia.
   - Revisar llamadas a `super()` en controladores y métodos sobrescritos para asegurar compatibilidad de firma.
3. Ejecutar Odoo 18 en modo desarrollador e intentar instalar el addon:
   - Recopilar errores del log y corregir (firmas, imports, campos faltantes).
4. Ajustar vistas/QWeb y assets según errores y pruebas manuales en la UI.
5. Pruebas funcionales: flujo web (tienda), POS, checkout, y procesos donde hay overrides.

Patch sugeridos (ejemplos)
- Manifest: actualizar versión
  - Antes: `'version': '14.0.11',`
  - Sugerido: `"version": "18.0.1.0.0",`

- Extensión de modelo (quitar `_name` duplicado)
  - Antes:
    ```py
    class ProductTemplate(models.Model):
        _name = 'product.template'
        _inherit = "product.template"
        ...
    ```
  - Sugerido:
    ```py
    class ProductTemplate(models.Model):
        _inherit = "product.template"
        ...
    ```

Notas finales
- El código fuente no muestra problemas graves de API obsoleta, por lo que la migración debería centrarse en manifests, signatures de `super()` y pruebas en runtime.
- Siguiente acción recomendada: aplicar los cambios en manifests y en los `_name/_inherit` redundantes, luego iniciar Odoo 18 y proceder con instalación para capturar errores concretos del entorno.

Checklist de trabajo (estado actual)
- [x] Crear lista de tareas e inspeccionar el directorio del módulo
- [x] Identificar APIs y dependencias incompatibles con Odoo 18 (escaneo inicial)
- [x] Leer archivos Python y detectar issues principales (informe)
- [ ] Actualizar manifest (metadata) para Odoo 18
- [ ] Ajustar código Python (models, fields, api decorators, imports)
- [ ] Actualizar vistas XML / QWeb templates a sintaxis de Odoo 18
- [ ] Migrar/ajustar assets estáticos (SCSS/JS)
- [ ] Ejecutar servidor Odoo 18 en modo depuración e intentar instalar el módulo
- [ ] Corregir errores y warnings del log
- [ ] Pruebas funcionales finales en Odoo 18
