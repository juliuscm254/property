from odoo import fields, models


class TenantCommunication(models.Model):
    _name = "tenant.communication"  # Descriptive name
    _description = "Tenant Communication Management"

    # Unique identifier (consider using a sequence)
    tenant_communication_id = fields.Char(
        string="ID",
        required=True,
        default=lambda self: self.env["ir.sequence"].next_by_code(
            "tenant.communication"
        ),
    )

    # Many2one field referencing the RentalUnit model
    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="cascade",
    )

    # Selection field for communication types
    type = fields.Selection(
        string="Type",
        required=True,
        selection=[
            ("notice", "Notice"),
            ("reminder", "Reminder"),
            ("maintenance_request", "Maintenance Request"),
            ("other", "Other"),  # Add more options as needed
        ],
    )

    # Selection field for communication medium (optional)
    medium = fields.Selection(
        string="Medium",
        selection=[
            ("email", "Email"),
            ("phone_call", "Phone Call"),
            ("letter", "Letter"),
            ("in_person", "In Person"),
            ("other", "Other"),  # Add more options as needed
        ],
    )

    # Description of the communication
    description = fields.Text(string="Description", required=True)

    # Date and time the communication occurred
    valid_from = fields.Datetime(
        string="Date", required=True, default=lambda self: fields.Datetime.now()
    )

    # Optional date and time until which the communication is valid
    valid_until = fields.Datetime(string="Valid Until")

    # Selection field for communication status
    status = fields.Selection(
        string="Status",
        required=True,
        selection=[
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("received", "Received"),
            ("closed", "Closed"),  # Add more options as needed
        ],
    )


from odoo import fields, models


class TenantCommunication(models.Model):
    _name = "tenant.communication"  # Descriptive name
    _description = "Tenant Communication Management"

    # Unique identifier (consider using a sequence)
    # tenant_communication_id = fields.Char(string='ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('tenant.communication'))
    # _help = "Unique identifier for this tenant communication."

    # Many2one field referencing the RentalUnit model
    rental_unit_id = fields.Many2one(
        comodel_name="rental.unit",
        string="Rental Unit",
        required=True,
        ondelete="cascade",
    )
    _help = "The rental unit this communication is associated with."

    # Selection field for communication types
    type = fields.Selection(
        string="Type",
        required=True,
        selection=[
            ("notice", "Notice"),
            ("reminder", "Reminder"),
            ("maintenance_request", "Maintenance Request"),
            ("other", "Other"),  # Add more options as needed
        ],
        help="Select the type of communication.",
    )

    # Selection field for communication medium (optional)
    medium = fields.Selection(
        string="Medium",
        selection=[
            ("email", "Email"),
            ("phone_call", "Phone Call"),
            ("letter", "Letter"),
            ("in_person", "In Person"),
            ("other", "Other"),  # Add more options as needed
        ],
        help="Optional field to specify the communication medium (e.g., email, phone call).",
    )

    # Description of the communication
    description = fields.Text(
        string="Description",
        required=True,
        help="Detailed information about the communication.",
    )

    # Date and time the communication occurred
    valid_from = fields.Datetime(
        string="Date", required=True, default=lambda self: fields.Datetime.now()
    )
    _help = "Date and time the communication occurred."

    # Optional date and time until which the communication is valid
    valid_until = fields.Datetime(
        string="Valid Until",
        help="Optional field to specify the date and time until which the communication is considered valid.",
    )

    # Selection field for communication status
    status = fields.Selection(
        string="Status",
        required=True,
        selection=[
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("received", "Received"),
            ("closed", "Closed"),  # Add more options as needed
        ],
        help="Current status of the communication (e.g., draft, sent, received, closed).",
    )
