# TODO  Doest not work 3.9
#  from pydantic import ValidationError
import datetime

from odoo import api, fields, models


class OwnerContract(models.Model):
    _name = "owner.contract"
    _description = "Property Owner Contract Management"
    _inherits = {"contract.contract": "contract_id"}
    PAYMENT_FREQUENCY = [
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("biannually", "Biannually"),  # Added biannually option
        ("annually", "Annually"),
    ]

    # TODO find a way to limit and default commission product_id

    commission_product_id = fields.Many2one(
        "product.product",
        string="Commission Product",
        # domain=[('type', '=', 'commission')]
    )

    # Optional reference to a main contract
    main_contract_id = fields.Char(
        string="Main Contract ID",
        help="Optional reference ID for a linked main contract.",
    )

    # Contract name
    contract_name = fields.Char(
        string="Contract Name", help="Optional name for the rental contract."
    )
    # Payment frequency (required)
    payment_frequency = fields.Selection(
        selection=PAYMENT_FREQUENCY,
        string="Payment Frequency",
        required=True,
        help="Select the frequency of rental payments (e.g., monthly, quarterly).",
    )

    description = fields.Text(
        string="Description",
        help="Optional field for additional details about the rental contract.",
    )

    payment_type = fields.Char(string="Commission Type", help="Type of commission.")

    # Contract group
    contract_group = fields.Char(
        string="Contract Group",
        help="Optional group classification for the rental contract.",
    )

    # TODO current payment period of the contract

    # Rent start date (required)
    payment_begin_date = fields.Date(
        string="Payment Period From Date",
        # required=True,
        help="Date the CURRENT payment period starts.",
    )

    # Rent end date (required)
    payment_end_date = fields.Date(
        string="Payment Period End Date",
        # required=True,
        help="Date the CURRENT payment period ends.",
    )

    # Notice period
    period_of_notice = fields.Char(
        string="Period of Notice",
        help="Required notice period for terminating the contract.",
    )

    # Payment in advance flag
    payment_in_advance = fields.Boolean(
        string="Payment in Advance", help="Flag indicating if rent is paid in advance."
    )

    # Short term lease flag
    short_term_lease = fields.Boolean(
        string="Short Term Lease", help="Flag indicating a short-term lease agreement."
    )

    # Tenant sector
    owner_sector = fields.Char(
        string="Tenant Sector",
        help="The tenant's industry sector (e.g., retail, technology).",
    )

    # Turnover reporting interval
    turnover_reporting_interval = fields.Char(
        string="Turnover Reporting Interval",
        help="Frequency for reporting tenant turnover.",
    )

    # Valid from date (required)
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

    total_monthly_rent = fields.Monetary(
        string="Total Monthly Rent Value for Contract",
        compute="_compute_total_monthly_rent",
    )

    total_monthly_rent_occupied = fields.Monetary(
        string="Total Monthly Rent Occupied Units",
        compute="_compute_total_monthly_rent_occupied",
        store=True,
    )

    commission_percentage = fields.Float(
        string="Commission Percentage", digits="Product Price"
    )

    rental_unit_ids = fields.One2many(
        comodel_name="rental.unit",
        string="Rental Units",
        compute="_compute_rental_unit_ids",
        ondelete="restrict",
    )
    owner_contract_building_ids = fields.One2many(
        comodel_name="owner.contract.building",
        inverse_name="owner_contract_id",
        string="Owner Contract Buildings",
        ondelete="restrict",
    )

    owner_period_payment = fields.Monetary(
        string="Owner Payment", compute="_compute_owner_payment", store=True
    )

    expense_line_ids = fields.One2many(
        "owner.contract.expense", "contract_id", string="Expense Lines"
    )

    total_monthly_expense = fields.Monetary(
        string="Expenses", compute="_compute_total_expenses", store=True
    )

    @api.depends(
        "owner_contract_building_ids", "owner_contract_building_ids.building_id"
    )
    def _compute_rental_unit_ids(self):
        for record in self:
            building_ids = record.owner_contract_building_ids.mapped("building_id").ids
            record.rental_unit_ids = self.env["rental.unit"].search(
                [("building_id", "in", building_ids)]
            )

    @api.depends("rental_unit_ids", "rental_unit_ids.monthly_rent")
    def _compute_total_monthly_rent(self):
        for record in self:
            record.total_monthly_rent = sum(
                record.rental_unit_ids.mapped("monthly_rent")
            )

    @api.depends("rental_unit_ids", "rental_unit_ids.monthly_rent")
    def _compute_total_monthly_rent_occupied(self):
        for record in self:
            record.total_monthly_rent_occupied = sum(
                rental_unit.monthly_rent
                for rental_unit in record.rental_unit_ids
                if rental_unit.rented_out
            )
            record._update_contract_line()

    # @api.depends('expense_line_ids')
    # def _compute_total_expenses(self):
    #     total_expenses = 0.0
    #     for record in self:
    #         # total_expenses = 0.0
    #         for expense in record.expense_line_ids:
    #             if expense.expense_type == 'percentage':
    #                 total_expenses += record.total_monthly_rent_occupied * (expense.expense_value / 100)
    #             else:
    #                 total_expenses += expense.expense_value
    #         record.total_monthly_expense = total_expenses

    @api.depends(
        "total_monthly_rent_occupied", "commission_percentage", "total_monthly_expense"
    )
    def _compute_owner_payment(self):
        for record in self:
            # Existing logic to handle cases where commission_percentage might be zero
            if not record.commission_percentage:
                record.owner_period_payment = (
                    record.total_monthly_rent_occupied - record.total_monthly_expense
                )
                continue

            commission_amount = record.total_monthly_rent_occupied * (
                record.commission_percentage / 100
            )
            record.owner_period_payment = (
                record.total_monthly_rent_occupied
                - commission_amount
                - record.total_monthly_expense
            )

    @api.depends("expense_line_ids")
    def _compute_total_expenses(self):
        for record in self:
            total_expenses = 0.0
            for expense in record.expense_line_ids:
                if expense.expense_type == "percentage":
                    total_expenses += record.total_monthly_rent_occupied * (
                        expense.expense_value / 100
                    )
                else:
                    total_expenses += expense.expense_value
            record.total_monthly_expense = total_expenses

    @api.constrains("rent_begin_date", "rent_end_date")
    def _check_rent_dates(self):
        for record in self:
            if (
                record.rent_begin_date
                and record.rent_end_date
                and record.rent_begin_date > record.rent_end_date
            ):
                raise ValidationError(
                    "Rent end date must be greater than rent begin date."
                )

    @api.model
    def create(self, vals):
        res = super(OwnerContract, self).create(vals)
        res._create_contract_line()
        return res

    def write(self, vals):
        res = super(OwnerContract, self).write(vals)
        self._update_contract_line()
        return res

    @api.onchange("contract_id", "valid_from", "owner_period_payment", "name")
    def _onchange_update_contract_line(self):
        self._update_contract_line()

    def _create_contract_line(self):
        for record in self:
            if record.commission_product_id:  # No existing line, create a new one
                self.env["contract.line"].create(
                    {
                        "contract_id": record.contract_id.id,
                        "date_start": record.valid_from,
                        "product_id": record.commission_product_id.id,
                        "price_unit": record.owner_period_payment,
                        "name": record.name,
                    }
                )

    def _update_contract_line(self):
        for record in self:
            contract_lines = self.env["contract.line"].search(
                [
                    ("contract_id", "=", record.contract_id.id),
                    ("product_id", "=", record.commission_product_id.id),
                ]
            )
            if record.commission_product_id:  # Commission product is selected
                # Existing line, update it
                contract_lines.write(
                    {
                        "date_start": record.valid_from,
                        "price_unit": record.owner_period_payment,
                        "name": record.name,
                    }
                )
            else:  # No commission product selected, delete any existing line
                if contract_lines:
                    contract_lines.unlink()
        else:
            # Handle the case where contract_id does not exist
            # You can add your logic here
            pass
