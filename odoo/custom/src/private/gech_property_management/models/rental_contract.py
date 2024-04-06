from odoo import api, fields, models


class RentalContract(models.Model):
    _name = "rental.contract"
    _description = "Rental Contract"

    # property_id = fields.Many2one(comodel_name='property.property', string='Property', required=True)
    PAYMENT_FREQUENCY = [
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("biannually", "Biannually"),  # Added biannually option
        ("annually", "Annually"),
    ]

    CONTRACT_TYPES = [
        ("residential", "Residential"),
        ("commercial", "Commercial"),
        ("industrial", "Industrial"),
        # Add more contract types as needed
    ]

    # Optional reference to a main contract
    main_contractid = fields.Char(string="Main Contract ID")

    # Contract code (required)
    contract_code = fields.Char(string="Contract Code", required=True)

    # Contract type
    contract_type = fields.Selection(
        selection=CONTRACT_TYPES,
        string="Contract type",
        required=True,
        help="Select the frequency of rental payments (e.g., monthly, quarterly).",
    )

    # Company code
    company_code = fields.Char(string="Company Code")

    # Contract name
    contract_name = fields.Char(string="Contract Name")

    # Contract group
    contract_group = fields.Char(string="Contract Group")

    # Rent start date (required)
    rent_begin_date = fields.Date(string="Rent Begin Date", required=True)

    # Rent end date (required)
    rent_end_date = fields.Date(string="Rent End Date", required=True)

    # Valid from date (required)
    valid_from = fields.Date(string="Valid From", required=True)

    # Valid until date (required)
    valid_until = fields.Date(string="Valid Until", required=True)

    # Notice period
    period_of_notice = fields.Char(string="Period of Notice")

    # Payment in advance flag
    payment_in_advance = fields.Boolean(string="Payment in Advance")

    # Payment frequency (required)
    payment_frequency = fields.Selection(
        selection=PAYMENT_FREQUENCY,
        string="Payment Frequency",
        required=True,
        help="Select the frequency of rental payments (e.g., monthly, quarterly).",
    )

    # Short term lease flag
    short_term_leaase = fields.Boolean(string="Short Term Lease")

    # Tenant sector
    tenant_sector = fields.Char(string="Tenant Sector")

    # Turnover reporting interval
    turnover_reporting_interval = fields.Char(string="Turnover Reporting Interval")

    # from odoo import models, fields, api

    # class RentalContract(models.Model):
    #     _name = 'rental.contract'
    #     _description = 'Rental Contract Management'

    #     # Many2one referencing the 'property.property' model (required)
    #     # property_id = fields.Many2one(comodel_name='property.property', string='Property', required=True, ondelete='restrict',
    #                                 #  help="The property associated with this rental contract.")

    #     # Optional reference to a main contract
    #     main_contract_id = fields.Char(string='Main Contract ID', help="Optional reference ID for a linked main contract.")

    #     # Contract code (required)
    #     contract_code = fields.Char(string='Contract Code', required=True, help="Unique identifier for this rental contract.")

    #     # Contract type
    #     contract_type = fields.Selection(string='Contract Type', selection=[],
    #                                     help="Select the type of rental contract (e.g., residential, commercial).")  # Replace with relevant options

    #     # Tenant company (foreign key to partner.id)
    #     tenant_id = fields.Many2one(comodel_name='res.partner', string='Tenant Company', required=True, ondelete='restrict',
    #                                help="The company renting the property under this contract.")

    #     # Contract name
    #     contract_name = fields.Char(string='Contract Name', help="Optional name for the rental contract.")

    #     # Contract group
    #     contract_group = fields.Char(string='Contract Group', help="Optional group classification for the rental contract.")

    #     # Rent start date (required)
    #     rent_begin_date = fields.Date(string='Rent Begin Date', required=True, help="Date the rental period starts.")

    #     # Rent end date (required)
    #     rent_end_date = fields.Date(string='Rent End Date', required=True, help="Date the rental period ends.")

    #     # Valid from date (required)
    #     valid_from = fields.Date(string='Valid From', required=True, help="The date from which this contract is considered valid.")

    #     # Valid until date (required)
    #     valid_until = fields.Date(string='Valid Until', required=True, help="The date until which this contract remains valid.")

    #     # Notice period
    #     period_of_notice = fields.Char(string='Period of Notice', help="Required notice period for terminating the contract.")

    #     # Payment in advance flag
    #     payment_in_advance = fields.Boolean(string='Payment in Advance', help="Flag indicating if rent is paid in advance.")

    #     # Payment frequency (required)
    #     payment_frequency = fields.Selection(string='Payment Frequency', selection=[],
    #                                          help="Select the frequency of rental payments (e.g., monthly, quarterly).")  # Replace with relevant options

    #     # Short term lease flag
    #     short_term_lease = fields.Boolean(string='Short Term Lease', help="Flag indicating a short-term lease agreement.")

    #     # Tenant sector
    #     tenant_sector = fields.Char(string='Tenant Sector', help="The tenant's industry sector (e.g., retail, technology).")

    #     # Turnover reporting interval
    #     turnover_reporting_interval = fields.Char(string='Turnover Reporting Interval', help="Frequency for reporting tenant turnover.")

    # Description field
    description = fields.Text(
        string="Description",
        help="Optional field for additional details about the rental contract.",
    )

    invoice_count = fields.Integer(compute="_compute_invoice_count")

    terminate_date = fields.Date(
        string="Termination Date",
        readonly=True,
        copy=False,
        tracking=True,
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        index=True,
        default=lambda self: self.env.user,
    )

    group_id = fields.Many2one(
        string="Group",
        comodel_name="account.analytic.account",
        ondelete="restrict",
    )

    active = fields.Boolean(
        default=True,
    )

    currency_id = fields.Many2one(
        compute="_compute_currency_id",
        inverse="_inverse_currency_id",
        comodel_name="res.currency",
        string="Currency",
    )
    manual_currency_id = fields.Many2one(
        comodel_name="res.currency",
        readonly=True,
    )

    def _get_computed_currency(self):
        """Helper method for returning the theoretical computed currency."""
        self.ensure_one()
        currency = self.env["res.currency"]
        if any(self.contract_line_ids.mapped("automatic_price")):
            # Use pricelist currency
            currency = (
                self.pricelist_id.currency_id
                or self.partner_id.with_company(
                    self.company_id
                ).property_product_pricelist.currency_id
            )
        return currency or self.journal_id.currency_id or self.company_id.currency_id

    @api.depends(
        "manual_currency_id",
        "pricelist_id",
        "partner_id",
        "journal_id",
        "company_id",
    )
    def _compute_currency_id(self):
        for rec in self:
            if rec.manual_currency_id:
                rec.currency_id = rec.manual_currency_id
            else:
                rec.currency_id = rec._get_computed_currency()

    def _inverse_currency_id(self):
        """If the currency is different from the computed one, then save it
        in the manual field.
        """
        for rec in self:
            if rec._get_computed_currency() != rec.currency_id:
                rec.manual_currency_id = rec.currency_id
            else:
                rec.manual_currency_id = False
