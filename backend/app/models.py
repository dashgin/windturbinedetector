from dataclasses import dataclass

# efficency = 0.35  # % (https://www.emo.org.tr/ekler/4986d86a17424ee_ek.pdf)


@dataclass
class Vertical:
    min_speed: int = 10  # m/s
    power: int = 500  # kW
    unit_price: float = 10_000  # AZN
    transportation_cost: float = unit_price * 5 / 100  # AZN


@dataclass
class Horizontal:
    min_speed: int = 20  # m/s
    power: int = 3_000  # kW
    unit_price: float = 10_000  # AZN
    transportation_cost: float = unit_price * 20 / 100  # AZN


@dataclass
class CO2Emission:
    coal: float = 227 * 0.001  # kg/MJ
    gas: float = 129 * 0.001  # kg/MJ
    biomass: float = 66 * 0.001  # kg/MJ
    hydro: float = 30 * 0.001  # kg/MJ
    solar: float = 18 * 0.001  # kg/MJ
    geothermal: float = 12.5 * 0.001  # kg/MJ
    nuclear: float = 5 * 0.001  # kg/MJ
    wind_vertical: float = 4.2 * 0.001  # kg/MJ
    wind_horizontal: float = 4.7 * 0.001  # kg/MJ


ELECTRIC_USAGE_PER_YEAR = 10_000
