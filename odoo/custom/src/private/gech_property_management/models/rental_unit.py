import datetime

from odoo import api, fields, models


class RentalUnit(models.Model):
    _name = "rental.unit"
    _description = "Rental Unit"

    building_id = fields.Many2one(
        comodel_name="building.building", string="Building", required=True
    )
    name = fields.Char(string="Name", required=True, help="Name of the rental unit")
    rental_unit_code = fields.Char(
        string="Rental Unit Code", help="User-specific Rental Unit Code"
    )
    occupancy_state = fields.Selection(
        string="Occupancy Status",
        selection=[("rented", "Rented"), ("vacant", "Vacant"), ("other", "Other")],
        default="vacant",
    )
    rented_out = fields.Boolean(
        # readonly=True,
        string="Is Rented Out?",
        help="Is the rental unit rented out (Y/N)",
        default=False,
    )
    usage_type = fields.Char(string="Usage Type", help="Usage type of the rental unit")
    vacancy = fields.Boolean(
        string="Is Vacant?", help="Is the rental unit vacant (Y/N)"
    )
    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        default=fields.Datetime.now,
        help="The date from which the building record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )
    valid_until = fields.Datetime(
        string="Valid Until",
        required=True,
        default=lambda self: datetime.datetime(year=9999, month=12, day=31),
        help="The date until which the building record is considered valid. This should be in the format yyyy-mm-ddThh:mm:ssZ (conforms to ISO 8061).",
    )

    monthly_rent = fields.Monetary(
        string="Monthly Rent",
        currency_field="currency_id",
        required=True,
        help="The monthly rent amount for this rental unit.",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id.id,
        help="The currency in which the monthly rent is expressed.",
    )

    @api.constrains("monthly_rent")
    def _check_monthly_rent_positive(self):
        for record in self:
            if record.monthly_rent < 0:
                raise ValidationError("Monthly rent cannot be negative.")

    def act_show_rental_unit(self):
        """
        If there are multiple units, it opens the list view first.
        If a rental_unit_id is provided, it opens the form view for that rental unit.
        @return: the rental unit view
        """
        self.ensure_one()
        rental_unit_id = self.env.context.get(
            "active_id"
        )  # Get clicked unit ID from context
        print("CONTEXT!!!!", self.env.context)
        if rental_unit_id:
            # Open the form view for the clicked unit
            return {
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "rental.unit",
                "views": [
                    [
                        self.env.ref(
                            "gech_property_management.building_rental_unit_form_view"
                        ).id,
                        "form",
                    ]
                ],
                "res_id": rental_unit_id,
                "target": "current",  # Open in the current window
            }

    def action_create_rental_unit(self):
        action = self.env.ref(
            "gech_property_management.building_rental_unit_form_view"
        ).read()[0]
        action["context"] = {"default_building_id": self.env.context.get("active_id")}
        return action

    # Other model methods and logic can be added here
