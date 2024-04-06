from odoo import fields, models


def generate_uuid():
    import uuid

    return str(uuid.uuid4())


class OperationalMeasurement(models.Model):
    _name = "operational.measurement"  # Descriptive name
    _description = "Operational Measurement"

    """
    Represents individual data on energy consumption, water consumption/withdrawal, waste output or
    fugitive emissions including various further information (procured by, subtypes, purpose, covered time period)
    """

    # Unique identifier as GUID
    operational_measurement_id = fields.Char(
        string="ID",
        required=True,
        default=generate_uuid,
        readonly=True,
        help="Unique identifier for this operational measurement (GUID).",
    )

    parent_id = fields.Char(
        string="Parent ID", help="Unique identifier (guid or id) of the parent entity."
    )

    purpose = fields.Char(
        string="Purpose",
        required=True,
        help="Specific purpose of resource consumption (e.g., 'space heating').",
    )

    accuracy = fields.Selection(
        string="Accuracy",
        selection=[("metered", "Metered"), ("extrapolated", "Extrapolated")],
        required=True,
        help="Information on the accuracy of the value (e.g., 'metered' or 'extrapolated').",
    )

    type = fields.Selection(
        string="Type",
        selection=[],
        required=True,
        help="General type of operational measurement (e.g., energy, water, waste).",
    )  # Replace with relevant options

    sub_type = fields.Selection(
        string="Sub-Type",
        selection=[],
        help="Specific type of operational measurement (e.g., district heating, water discharge).",
    )  # Replace with relevant options

    name = fields.Char(
        string="Name",
        help="User-provided name of the individual operational measurement.",
    )

    value = fields.Float(
        string="Value",
        help="Value of the individual operational measurement.",
        digits=(19, 6),
    )

    unit = fields.Char(
        string="Unit",
        help="Unit of the operational measurement (e.g., 'kWh' or 'cubm').",
    )

    procured_by = fields.Selection(
        string="Procured By",
        selection=[],
        help="Information on operational control of resource consumption ('who bought it?') according to Greenhouse Gas Protocol.",
    )  # Replace with relevant options

    space_type_id = fields.Many2one(
        comodel_name="space.type",
        string="Space Type",
        help="Reference to a specific space type (or 'whole building').",
    )

    life_cycle_assessment = fields.Char(
        string="Life Cycle Assessment",
        help="Related life cycle assessment stage according to ISO 14040.",
    )

    posting_date = fields.Datetime(
        string="Posting Date", help="Date of measurement posting (yyyy-mm-dd hh:mm:ss)."
    )

    measurement_date = fields.Datetime(
        string="Measurement Date",
        help="Date the measurement was taken (yyyy-mm-dd hh:mm:ss).",
    )

    valid_from = fields.Datetime(
        string="Valid From",
        required=True,
        default=lambda self: fields.Datetime.now(),
        help="Date the measurement validity starts (yyyy-mm-dd hh:mm:ss).",
    )

    valid_until = fields.Datetime(
        string="Valid Until",
        required=True,
        help="Date the measurement validity ends (yyyy-mm-dd hh:mm:ss).",
    )

    sensor_id = fields.Char(
        string="Sensor ID", help="Unique identifier of the sensor (if applicable)."
    )

    _sql_constraints = [
        (
            "unique_operational_measurement_id",
            "unique(operational_measurement_id)",
            "Operational Measurement ID must be unique.",
        )
    ]
