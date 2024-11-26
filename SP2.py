class PowerPlant:
    def __init__(self, name, max_power):
        self.name = name
        self.max_power = max_power
        self.output_powre = 0.0
        self.payment = 0.0


class SolarPlant(PowerPlant):
    def __init__(self, name, max_power, irradiance, temperature):
        super().__init__(name, max_power)
        self.irradiance = irradiance
        self.temperature = temperature
        self.max_power = max_power * (irradiance/1000) * (1+(-0.0035*(0.0256-temperature)))


class WindPlant(PowerPlant):
    def __init__(self, name, max_power, actual_wind_speed, rated_speed, cutin_speed, cutoff_speed):
        super().__init__(name, max_power)

        if actual_wind_speed > cutoff_speed or actual_wind_speed < cutoff_speed:
            self.max_power = 0
        elif cutin_speed <= actual_wind_speed and actual_wind_speed <= rated_speed:
            self.max_power = max_power * ((actual_wind_speed**2 - cutin_speed**2)/(rated_speed**2 - cutin_speed**2))
        elif rated_speed <= actual_wind_speed and actual_wind_speed <= cutoff_speed:
            self.max_power = max_power


class CoalPlant(PowerPlant):
    def __init__(self, name, max_power, offer_price):
        super().__init__(name, max_power)
        self.offer_price = offer_price


class DieselPlant(PowerPlant):
    def __init__(self, name, max_power, offer_price):
        super().__init__(name, max_power)
        self.offer_price = offer_price


class Market:
    def __init__(self, total_demand):
        self.total_demand = total_demand
        self.must_dispatch_plants = []
        self.dispatchable_plants = []
        self.market_price = 0.0
    
    def add_must_dispatch(self, plant):
        self.must_dispatch_plants.append(plant)
    
    def add_dispatchable_plant(self, plant):
        self.dispatchable_plants.append(plant)
    
    def calculate_dispatch(self):
        #Fulfill demand with must-dispatch plants
        remaining_demand = self.total_demand
        for plant in self.must_dispatch_plants:
            if remaining_demand <= 0:
                break
            plant.output_power = min(plant.max_power, remaining_demand)
            remaining_demand -= plant.output_power
        
        #Sort plants in ascending order of offer prices
        for i in range(len(self.dispatchable_plants)):
            for j in range(i + 1, len(self.dispatchable_plants)):
                if self.dispatchable_plants[i].offer_price > self.dispatchable_plants[j].offer_price:
                    self.dispatchable_plants[i], self.dispatchable_plants[j] = self.dispatchable_plants[j], self.dispatchable_plants[i]
        
        #Fulfill remaining demand with dispatchable plants
        for plant in self.dispatchable_plants:
            if remaining_demand <= 0:
                break
            plant.output_power = min(plant.max_power, remaining_demand)
            remaining_demand -= plant.output_power
            # Update market price to the plant's offer price
            self.market_price = plant.offer_price

    def print_results(self, market_clearing_price, total_payment):
        print(f"Total System Demand: {self.total_demand} MW")
        print(f"Market Clearing Price: PHP/kWh {market_clearing_price:.2f}")
        print(f"Total Demand Payment: PHP {total_payment:,.2f}")
        print()
        print("Power Plant Name".ljust(24) + "Power Output (MW)".ljust(24) + "Payment (PHP)")
        for plant in self.must_dispatch_plants + self.dispatchable_plants:
            print(
                f"{plant.name}".ljust(24) +
                f"{plant.output_power}".ljust(24) +
                f"{plant.payment:,.2f}".rjust(16)
            )

def main():
    total_demand = int(input("Total demand in MW: "))
    market = Market(total_demand)

    num_solar_plants = int(input("Number of solar PV plants: "))
    for i in range(num_solar_plants):
        solar_name = str(input(f"Solar PV plant {i+1} name: "))
        solar_p_max = int(input("Maximum power output of the plant in MW: "))
        irradiance = float(input("Solar irradiance in W/m2: "))
        temperature = float(input("Ambient temperature in degree C: "))
        market.add_must_dispatch(SolarPlant(solar_name, solar_p_max, irradiance, temperature))


    num_wind_plants = int(input("Number of wind plants: "))
    for i in range(num_wind_plants):
        wind_name = str(input(f"Wind plant {i+1} name: "))
        wind_p_max = int(input("Maximum power output of the plant in MW: "))
        actual_wind_speed = float(input("Actual wind speed in m/s: "))
        rated_speed = float(input("Rated wind speed in m/s: "))
        cutin_speed = float(input("Cut-in wind speed in m/s: "))
        cutoff_speed = float(input("Cut-off wind speed in m/s: "))
        market.add_must_dispatch(WindPlant(wind_name, wind_p_max, actual_wind_speed, rated_speed, cutin_speed, cutoff_speed))

    num_coal_plants = int(input("Number of coal plants: "))
    for i in range(num_coal_plants):
        coal_name = str(input(f"Coal plant {i+1} name: "))
        coal_max_output = int(input("Maximum power output (offer) of the plant in MW: "))
        coal_offer_price = float(input("Offer price in PHP/kWh: "))
        market.add_dispatchable_plant(CoalPlant(coal_name, coal_max_output, coal_offer_price))

    num_diesel_plants = int(input("Number of diesel plants: "))
    for i in range(num_diesel_plants):
        diesel_name = str(input(f"Diesel plant {i+1} name: "))
        diesel_max_output = int(input("Maximum power output (offer) of the plant in MW: "))
        diesel_offer_price = float(input("Offer price in PHP/kWh: "))
        market.add_dispatchable_plant(DieselPlant(diesel_name, diesel_max_output, diesel_offer_price))

    market.calculate_dispatch()
    total_payment = 0
    for plant in market.must_dispatch_plants + market.dispatchable_plants:
        plant.payment = plant.output_power * market.market_price * 1000
        total_payment += plant.payment

    market.print_results(market_clearing_price=market.market_price, total_payment=total_payment)


if __name__ == "__main__":
    main()

##THE OUTPUTS ARE WRONG##
##ALSO CHANGE THE CODE A BIT##