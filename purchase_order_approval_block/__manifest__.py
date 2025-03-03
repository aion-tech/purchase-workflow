# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Order Approval Block",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "version": "16.0.1.0.0",
    "category": "Purchase Management",
    "website": "https://github.com/OCA/purchase-workflow",
    "depends": ["purchase_exception"],
    "data": [
        "data/purchase_exception_data.xml",
        "security/ir.model.access.csv",
        "security/purchase_order_approval_block_security.xml",
        "views/purchase_approval_block_reason_view.xml",
        "views/purchase_order_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
