from odoo import fields, models


class RentalOption(models.Model):
    _name = "rental.option"
    _description = "Information about rental option of rental contract"

    # Fields
    # rental_option_id = fields.Char(string='Rental Option ID', required=True, help='Unique identifier either coming from the previous system or needs to be defined')
    rental_contract_id = fields.Char(
        string="Rental Contract ID",
        required=True,
        help="Reference to the corresponding rental contract",
    )
    option_type = fields.Char(string="Type", required=True, help="Type of option")
    option_subtype = fields.Char(
        string="Subtype", required=True, help="Subtype of the option"
    )
    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        help="Date option is valid from (in yyyy-mm-dd'Thh:mm:ssZ' format)",
    )
    valid_until = fields.Datetime(
        string="Valid Until",
        required=True,
        help="Date option is valid until (in yyyy-mm-dd'Thh:mm:ssZ' format)",
    )
    document_id = fields.Char(
        string="Document ID", help="Reference to the document (if it exists)"
    )
