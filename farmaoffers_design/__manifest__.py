{
    "name": "Farmaoffers Design",
    "version": "1.0.0",
    "author": "Farmaoffers",
    "category": "Website",
    "summary": "Base module for Farmaoffers custom design and snippets",
    "license": "LGPL-3",
    "depends": [
        "website",
        "web_editor",
        "website_sale",
        "sale_management",
        "sale_stock",
        "stock",
        "product",
    ],
    "data": [
        # === Base Templates ===
        "views/homepage_templates.xml",

        # === Snippets ===
        "views/snippets/stripe_info_snippet.xml",
        "views/snippets/stripe_info_snippet_registry.xml",
        "views/snippets/top_products_snippet.xml",
        "views/snippets/top_products_snippet_registry.xml",
        "views/snippets/section_banner_snippet.xml",
        "views/snippets/section_banner_snippet_registry.xml",
        "views/snippets/section_desc_disc_snippet.xml",
        "views/snippets/section_desc_disc_snippet_registry.xml",
        "views/snippets/section_aditional_info_snippet.xml",
        "views/snippets/section_aditional_info_snippet_registry.xml",
        "views/snippets/section_same_compound_snippet.xml",
        "views/snippets/section_same_compound_snippet_registry.xml",
        "views/snippets/section_bought_together_snippet.xml",
        "views/snippets/section_bought_together_snippet_registry.xml",
        "views/snippets/section_general_info_snippet.xml",
        "views/snippets/section_general_info_snippet_registry.xml",
"views/snippets/section_faqs_snippet.xml",
"views/snippets/section_faqs_snippet_registry.xml",
"views/snippets/section_product_resume_snippet.xml",
"views/snippets/section_product_resume_snippet_registry.xml",
"views/snippets/product_sidebar_snippet.xml",
"views/snippets/product_sidebar_snippet_registry.xml",



        # === Header & Footer Templates ===
        #"views/h_f_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            # === Farmaoffers Core Styles ===
            "/farmaoffers_design/static/src/css/website_sale.css",
            # "/farmaoffers_design/static/src/css/splide/splide.min.css",
            "/farmaoffers_design/static/src/scss/farmaoffers_variables.scss",
           # "/farmaoffers_design/static/src/scss/farmaoffers_styles.scss",
           # "/farmaoffers_design/static/src/scss/farmaoffers_top_header.scss",

            # === Farmaoffers JS ===
            "/farmaoffers_design/static/src/js/script.js",
            "/farmaoffers_design/static/src/js/splide/splide.min.js",

            # === Google Fonts ===
            "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined",

            # === Snippet: Stripe Info ===
            "/farmaoffers_design/static/src/snippets/stripe_info/style.scss",
            "/farmaoffers_design/static/src/snippets/stripe_info/000.js",

            # === Snippet: Top Products ===
            "/farmaoffers_design/static/src/snippets/top_products/top_products.scss",
            "/farmaoffers_design/static/src/snippets/top_products/000.js",

            # === Snippet: Section Banner ===
            "/farmaoffers_design/static/src/snippets/s_section_banner/style.scss",

            # === Snippet: Section Description & Disclaimer ===
            "/farmaoffers_design/static/src/snippets/section_desc_disc/style.scss",
            "/farmaoffers_design/static/src/snippets/section_desc_disc/style.scss",
            "/farmaoffers_design/static/src/snippets/section_aditional_info/style.scss",

            # === Snippet: Productos con el mismo compuesto activo ===
            "/farmaoffers_design/static/src/snippets/section_same_compound/style.scss",
            "/farmaoffers_design/static/src/snippets/section_same_compound/000.js",

            # === Snippet: Productos comprados juntos ===
            "/farmaoffers_design/static/src/snippets/section_bought_together/style.scss",
            "/farmaoffers_design/static/src/snippets/section_bought_together/000.js",
            "/farmaoffers_design/static/src/snippets/section_general_info/style.scss",
            "/farmaoffers_design/static/src/snippets/section_faqs/style.scss",

"/farmaoffers_design/static/src/snippets/section_product_resume/style.scss",

"/farmaoffers_design/static/src/snippets/product_sidebar/style.scss",
"/farmaoffers_design/static/src/snippets/product_sidebar/000.js",


        ],
        "web_editor.assets_wysiwyg": [
            # === JS enabled in editor mode ===
            "/farmaoffers_design/static/src/snippets/stripe_info/000.js",
            "/farmaoffers_design/static/src/snippets/top_products/000.js",
        ],
    },
    "installable": True,
    "application": False,
}