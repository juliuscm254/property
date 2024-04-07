import datetime

from odoo import fields, models


class Building(models.Model):
    _name = "building.building"
    _description = "A building represents a structure that provides shelter for its occupants or contents and stands in one place. The building is also used to provide a basic element within the spatial structure hierarchy for the components of a building project (together with site, storey, and space)"

    PRIMARY_TYPE_OF_BUILDING = [
        ("office", "Office"),
        ("residential", "Residential"),
        ("commercial", "Commercial"),
        ("other", "Other"),
    ]
    SECONDARY_TYPE_OF_BUILDING = [
        ("warehouse", "Warehouse"),
        ("manufacturing", "Manufacturing"),
        ("other", "Other"),
        # Add more options as needed
    ]

    # # Unique identifier (consider using a sequence)
    # building_id = fields.Char(string='Building ID', required=True, index=True, help="Unique identifier for the building. This can be generated automatically using a sequence or defined manually.")

    # Many2one field referencing a potential 'site.site' model (if applicable)
    site_id = fields.Many2one(
        comodel_name="site.site",
        string="Site",
        help="Reference to the Site which the building belongs to (if applicable).",
    )

    name = fields.Char(
        string="Name",
        required=True,
        help="User-specific building name. This can be a descriptive name for the building, e.g., EMEA Headquarters or Office Berlin.",
    )

    building_code = fields.Char(
        string="Building Code",
        help="Optional user-specific Building Code for internal reference.",
    )

    # Selection field for primary building type (if there are predefined options)
    primary_type_of_building = fields.Selection(
        string="Primary Type",
        required=True,
        selection=PRIMARY_TYPE_OF_BUILDING,
        help="The primary type of building use. This can be categorised based on its function.",
    )
    # Selection field for secondary building type (if there are predefined options)
    secondary_type_of_building = fields.Selection(
        string="Secondary Type",
        selection=SECONDARY_TYPE_OF_BUILDING,
        help="The secondary type of building use, if applicable. This can be used to further classify the building's function.",
    )

    energy_efficiency_class = fields.Char(
        string="Energy Efficiency Class",
        help="The Energy Efficiency Class of the building, if known. This can indicate the building's energy performance.",
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

    construction_year = fields.Date(
        string="Construction Year",
        help="The year the building was constructed. If only the year is known, use yyyy-01-01.",
    )  # Use Date for years

    year_of_last_refurbishment = fields.Date(
        string="Year of Last Refurbishment",
        help="The year the building underwent its last refurbishment. If only the year is known, use yyyy-01-01.",
    )  # Use Date for years

    monument_protection = fields.Boolean(
        string="Monument Protection",
        help="Indicates whether the building is declared as a monument with national importance by the government.",
    )

    # Selection field for type of ownership (if there are predefined options)
    type_of_ownership = fields.Selection(
        string="Ownership Type",
        required=True,
        selection=[("owned", "Own"), ("leased", "Lease"), ("other", "Other")],
        default="owned",
        help="Indicates whether the building is owned or leased.",
    )

    self_use = fields.Boolean(
        string="Self Use",
        help="Indicates whether the building is used by the company itself (Y/N).",
    )

    tenant_structure = fields.Char(
        string="Tenant Structure",
        help="Describes the tenant structure of the building. This could be single-tenant, multi-tenant, etc.",
    )

    parking_spaces = fields.Integer(
        string="Parking Spaces",
        help="The total number of parking spaces available in the building.",
    )

    electric_vehicle_charging_stations = fields.Integer(
        string="EV Charging Stations",
        help="The number of electric vehicle charging stations available in the building.",
    )

    primary_energy_type = fields.Char(
        string="Primary Energy Type",
        help="The primary type of energy used for the building's operation, e.g., electricity, natural gas, etc.",
    )

    primary_water_type = fields.Char(
        string="Primary Water Type",
        help="The primary type of water used in the building, e.g., municipal water, well water, etc.",
    )

    primary_heating_type = fields.Char(
        string="Primary Heating Type",
        help="The primary type of heating system used in the building.",
    )

    secondary_heating_type = fields.Char(
        string="Secondary Heating Type",
        help="The secondary type of heating system used in the building, if applicable.",
    )

    air_conditioning = fields.Boolean(
        string="Air Conditioning",
        help="Does the building have air conditioning (Y/N) (Needed for precise future emissions projection of CHP Systems)",
    )

    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one(
        "res.country.state",
        string="State",
        ondelete="restrict",
        domain="[('country_id', '=?', country_id)]",
    )
    country_id = fields.Many2one("res.country", string="Country", ondelete="restrict")

    state = fields.Selection(
        [("new", "New"), ("ok", "OK"), ("archived", "Archived")],
        string="State",
        default="new",
    )

    def approved_building(self):
        self.write({"state": "ok"})
