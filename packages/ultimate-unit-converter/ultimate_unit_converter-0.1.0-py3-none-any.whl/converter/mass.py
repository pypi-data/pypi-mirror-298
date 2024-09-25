class MassConverter:
    conversion_factors = {
        'kg_to_lb': 2.20462,
        'lb_to_kg': 0.453592
    }

    @staticmethod
    def kg_to_lb(kg):
        return kg * MassConverter.conversion_factors['kg_to_lb']

    @staticmethod
    def lb_to_kg(lb):
        return lb * MassConverter.conversion_factors['lb_to_kg']