# Copyright 2015 0k.io
# Copyright 2016 ACSONE SA/NV
# Copyright 2017 Tecnativa
# Copyright 2020 initOS GmbH.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "web_m2x_options",
    "version": "17.0.1.0.0",
    "category": "Web",
    "author": "initOS GmbH,"
    "ACSONE SA/NV, "
    "0k.io, "
    "Tecnativa, "
    "Sygel, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/web",
    "license": "AGPL-3",
    "depends": ["web"],
    "assets": {
        "web.assets_backend": [
            (
                "before",
                "web/static/src/views/fields/*",
                "web_m2x_options/static/src/components/form.esm.js",
            ),
            "web_m2x_options/static/src/components/base.xml",
        ]
    },
    "installable": True,
}
