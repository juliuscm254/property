from odoo import fields, models


class RentalUnitSite(models.Model):
    _name = "rental.unit.site"  # Descriptive name
    _description = "Rental Unit - Site Link"

    # Unique identifier (consider using a sequence)
    # rental_unit_site_id = fields.Char(string='ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('rental.unit.site'))

    # Many2one field referencing the RentalUnit model
    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="cascade",
    )

    # Many2one field referencing the Site model
    site_id = fields.Many2one(
        comodel_name="site.site", string="Site", required=True, ondelete="cascade"
    )

    # Additional fields (consider if needed)
    # Example: primary_usage = fields.Char(string='Primary Usage')  # If a unit has different uses on different sites
