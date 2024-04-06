class PropertyAgency(models.Model):
    _name = "property.agency"

    def calculate_commission(self, property):
        total_rent = sum(
            unit.tenant_contract_id.rent_price for unit in property.rental_unit_ids
        )
        commission_rate = property.owner_contract_id.commission_rate
        return total_rent * commission_rate

    def calculate_owner_payment(self, property):
        total_rent = sum(
            unit.tenant_contract_id.rent_price for unit in property.rental_unit_ids
        )
        commission = self.calculate_commission(property)
        return total_rent - commission
