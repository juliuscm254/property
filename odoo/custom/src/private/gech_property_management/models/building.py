from odoo import _, api, fields, models


class Building(models.Model):
    _inherit = "building.building"

    rental_unit_count = fields.Integer(
        string="Rental Units",
        compute="_compute_rental_unit_count",
    )

    def _get_rental_unit_domain(self):
        return [("building_id", "=", self.id)]

    def _compute_rental_unit_count(self):
        rental_unit_model = self.env["rental.unit"]
        rental_unit_count = rental_unit_model.search_count(
            self._get_rental_unit_domain()
        )
        print(rental_unit_count)
        self.rental_unit_count = rental_unit_count

    @api.model  # Decorator to mark this as a model method
    def create_rental_unit(self):
        """
        Opens the rental unit form view with the building_id pre-filled.
        @return: dictionary containing information to open the form view
        """

        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "rental.unit",
            # "context": self.env.context,
            "context": dict(self._context, default_building_id=self.id),
        }

    def act_show_rental_unit(self):
        """
        If there are multiple units, it opens the list view first.
        If a rental_unit_id is provided, it opens the form view for that rental unit.
        @return: the rental unit view
        """
        self.ensure_one()
        if self.rental_unit_count == 0:
            # No units, directly open the create form
            return self.create_rental_unit()

        return {
            "type": "ir.actions.act_window",
            "view_mode": "list",
            "res_model": "rental.unit",
            "domain": self._get_rental_unit_domain(),
            "context": self.env.context,
            "views": [
                (
                    self.env.ref(
                        "gech_property_management.building_rental_unit_tree_view2"
                    ).id,
                    "list",
                )
            ],
            "name": _("Rental Units"),
        }
