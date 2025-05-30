# Copyright 2023 Trobz Consulting
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import odoo.tests

from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon


@odoo.tests.tagged("post_install", "-at_install")
class TestLotSelection(TestPointOfSaleHttpCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        cls.lot_product_1 = cls.env["product.product"].create(
            {
                "name": "Lot Product 1",
                "type": "product",
                "tracking": "lot",
                "categ_id": cls.env.ref("product.product_category_all").id,
                "available_in_pos": True,
            }
        )
        lots = cls.env["stock.lot"].create(
            [
                {
                    "name": "10120000515",
                    "product_id": cls.lot_product_1.id,
                    "company_id": cls.env.company.id,
                },
                {
                    "name": "10120000516",
                    "product_id": cls.lot_product_1.id,
                    "company_id": cls.env.company.id,
                },
            ]
        )
        location_id = cls.main_pos_config.picking_type_id.default_location_src_id.id
        cls.env["stock.quant"].with_context(inventory_mode=True).create(
            {
                "product_id": cls.lot_product_1.id,
                "inventory_quantity": 100,
                "location_id": location_id,
                "lot_id": lots[0].id,
            }
        ).action_apply_inventory()
        cls.env["stock.quant"].with_context(inventory_mode=True).create(
            {
                "product_id": cls.lot_product_1.id,
                "inventory_quantity": 100,
                "location_id": location_id,
                "lot_id": lots[1].id,
            }
        ).action_apply_inventory()

    def test_lot_selection(self):
        self.main_pos_config.with_user(self.pos_user).open_ui()
        self.start_tour(
            "/pos/ui?config_id=%d" % self.main_pos_config.id,
            "LotSelectionTour",
            login="pos_user",
        )

    def test_click_lot_icon(self):
        self.main_pos_config.with_user(self.pos_user).open_ui()
        self.start_tour(
            "/pos/ui?config_id=%d" % self.main_pos_config.id,
            "ClickLotIconTour",
            login="pos_user",
        )
