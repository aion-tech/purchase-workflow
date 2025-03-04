# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _name = "purchase.order"

    transport_mode_id = fields.Many2one(
        "purchase.transport.mode",
        compute="_compute_transport_mode_id",
        store=True,
        readonly=False,
    )
    transport_mode_status = fields.Json(
        compute="_compute_transport_mode_validation_status",
        help="Collect and validate order details to satisfy transport mode requirements",
        default={},
    )
    transport_mode_status_display = fields.Html(
        compute="_compute_transport_mode_validation_status",
        help="Render transport_mode_status in the UI",
    )
    transport_mode_status_ok = fields.Boolean(
        compute="_compute_transport_mode_validation_status",
        help="All transport mode requirements are satisfied",
    )

    @api.depends("partner_id")
    def _compute_transport_mode_id(self):
        for rec in self:
            rec.transport_mode_id = (
                rec.partner_id.commercial_partner_id.purchase_transport_mode_id
            )

    @api.depends("transport_mode_id")
    def _compute_transport_mode_validation_status(self):
        for rec in self:
            rec.transport_mode_status = rec._get_transport_mode_validation_status()
            rec.transport_mode_status_display = (
                rec._get_transport_mode_validation_status_display()
            )
            rec.transport_mode_status_ok = False if rec.transport_mode_status else True

    def _get_transport_mode_validation_status(self):
        self.ensure_one()
        errors = []
        if (
            not self.company_id.purchase_transport_mode_contraint_enabled
            or not isinstance(self.id, int)  # Record is not saved yet
        ):
            return {}
        for constraint in self.transport_mode_id.constraint_ids:
            if not constraint.filter_valid_purchase(self):
                error_message = "{}: {}".format(
                    constraint.name, constraint.description or ""
                )
                errors.append(error_message)
        if errors:
            return {"errors": errors}
        return {}

    def _get_transport_mode_validation_status_display(self):
        if not self.transport_mode_status:
            return ""
        errors = self.transport_mode_status.get("errors", [])
        if errors:
            return self.env["ir.qweb"]._render(
                "purchase_transport_mode.purchase_order_transport_mode_status_display",
                {"order": self, "errors": errors},
            )
        return ""
