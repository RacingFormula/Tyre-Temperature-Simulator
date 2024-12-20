import numpy as np
import matplotlib.pyplot as plt

class TyreTemperatureSimulator:
    def __init__(self, config):
        self.compounds = config.get("compounds", [])
        self.track_temperature = config.get("track_temperature", 30)  # degrees Celsius
        self.base_load = config.get("base_load", 1500)  # Load in Newtons
        self.race_distance = config.get("race_distance", 50)  # laps
        self.driving_style_factor = config.get("driving_style_factor", 1.0)  # Aggressiveness multiplier

    def simulate_compound(self, compound):
        heat_capacity = compound["heat_capacity"]
        thermal_conductivity = compound["thermal_conductivity"]
        base_temp = self.track_temperature

        temperatures = []
        performance = []
        current_temp = base_temp

        for lap in range(1, self.race_distance + 1):
            # Heat generation
            heat_generated = self.base_load * self.driving_style_factor * 0.01

            # Heat dissipation
            heat_dissipated = (current_temp - base_temp) * thermal_conductivity

            # Update temperature
            current_temp += (heat_generated - heat_dissipated) / heat_capacity

            # Clamp temperature within a realistic range
            current_temp = max(base_temp, current_temp)

            # Performance metric (inverse of temperature deviation from ideal)
            ideal_temp = compound["ideal_temperature"]
            performance_metric = max(0, 1 - abs(current_temp - ideal_temp) / ideal_temp)

            temperatures.append(current_temp)
            performance.append(performance_metric)

        return {
            "temperatures": temperatures,
            "performance": performance
        }

    def analyse_compounds(self):
        results = {}

        for compound in self.compounds:
            name = compound["name"]
            print(f"Simulating {name} compound...")
            results[name] = self.simulate_compound(compound)

        return results

    def plot_results(self, results):
        laps = range(1, self.race_distance + 1)

        plt.figure(figsize=(14, 8))

        # Plot temperature profiles
        plt.subplot(2, 1, 1)
        for compound, data in results.items():
            plt.plot(laps, data["temperatures"], label=f"{compound} Temperature")
        plt.title("Tyre Temperature Over Race Distance")
        plt.xlabel("Lap")
        plt.ylabel("Temperature (°C)")
        plt.legend()
        plt.grid(True)

        # Plot performance metrics
        plt.subplot(2, 1, 2)
        for compound, data in results.items():
            plt.plot(laps, data["performance"], label=f"{compound} Performance")
        plt.title("Tyre Performance Over Race Distance")
        plt.xlabel("Lap")
        plt.ylabel("Performance Metric")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    compounds = [
        {
            "name": "Soft",
            "heat_capacity": 0.8,
            "thermal_conductivity": 0.03,
            "ideal_temperature": 85
        },
        {
            "name": "Medium",
            "heat_capacity": 1.0,
            "thermal_conductivity": 0.05,
            "ideal_temperature": 90
        },
        {
            "name": "Hard",
            "heat_capacity": 1.2,
            "thermal_conductivity": 0.07,
            "ideal_temperature": 95
        }
    ]

    config = {
        "compounds": compounds,
        "track_temperature": 30,
        "base_load": 1500,
        "race_distance": 50,
        "driving_style_factor": 1.2
    }

    simulator = TyreTemperatureSimulator(config)
    results = simulator.analyse_compounds()
    simulator.plot_results(results)