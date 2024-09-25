class DistanceConverter:
    conversion_factors = {
        'km_to_miles': 0.621371,
        'miles_to_km': 1.60934
    }
    
    @staticmethod
    def km_to_miles(km):
        return km * DistanceConverter.conversion_factors['km_to_miles']
    
    @staticmethod
    def miles_to_km(miles):
        return miles * DistanceConverter.conversion_factors['miles_to_km']
    
    
    
