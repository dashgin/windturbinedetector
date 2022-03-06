from typing import Union
from django.conf import settings

import pandas as pd

from .models import (
    ELECTRIC_USAGE_PER_YEAR,
    Horizontal,
    Vertical,
    CO2Emission,
)


def get_horizontal_available_data(df_: pd.DataFrame) -> pd.DataFrame:
    """
    We consider that horizontal turbines can work only with winddirection with 90 degree difference.
    Filtering data with winddirection with 90 degree difference by average winddirection
    """

    # average the wind direction of the data
    wind_direction = df_["winddir"].mean()

    difference_list = [abs(i - wind_direction) for i in df_["winddir"]]

    less_that_90 = [i for i in difference_list if i <= 90]

    # index of the data that is less than 90 degree in data
    idxs = [difference_list.index(i) for i in less_that_90]

    return df_[df_.index.isin(idxs)]


def filter_by_speed(df_: pd.DataFrame, min_speed: int) -> pd.DataFrame:

    return df_[df_["windspeed"] >= min_speed]


def get_intensity(data: pd.DataFrame, type_: Union[Horizontal, Vertical]) -> float:
    filtered_by_speed = filter_by_speed(data, type_.min_speed)
    if type_ == Horizontal:
        horizontal_available_data = get_horizontal_available_data(filtered_by_speed)

        return horizontal_available_data["windspeed"].count() / len(data)
    return filtered_by_speed["windspeed"].count() / len(data)


def get_direction(data_: pd.DataFrame, type_: Union[Horizontal, Vertical]) -> float:
    if type_ == Vertical:
        return "-"
    return str(round(data_["winddir"].mean(), 2))


def get_efficency(intensity: float, power: int) -> float:
    """
    return kW/day or KJ (joul)
    """
    return intensity * power


def get_type(data: pd.DataFrame) -> Union[Horizontal, Vertical]:
    """
    We select the type of the turbine that has the highest efficiency with the given location.
    """
    _horizontal_intensity = get_intensity(data, Horizontal)

    _horizontal_efficiency = get_efficency(
        _horizontal_intensity, Horizontal.power
    )  # how many kW at one day

    _vertical_intensity = get_intensity(data, Vertical)

    _vertical_efficiency = get_efficency(
        _vertical_intensity, Vertical.power
    )  # how many kW at one day
    print(_horizontal_efficiency, _vertical_efficiency)
    if _horizontal_efficiency > _vertical_efficiency:
        return Horizontal
    return Vertical


def get_kwatt_per_year(efficency) -> float:

    return efficency * 365


def get_co2_emission(kwatt: float) -> float:
    for_coal = CO2Emission.coal * kwatt
    for_gas = CO2Emission.gas * kwatt
    for_biomass = CO2Emission.biomass * kwatt
    for_hydro = CO2Emission.hydro * kwatt
    for_solar = CO2Emission.solar * kwatt
    for_geothermal = CO2Emission.geothermal * kwatt
    for_nuclear = CO2Emission.nuclear * kwatt
    for_wind = CO2Emission.wind_horizontal * kwatt
    return {
        "coal": for_coal,
        "gas": for_gas,
        "biomass": for_biomass,
        "hydro": for_hydro,
        "solar": for_solar,
        "geothermal": for_geothermal,
        "nuclear": for_nuclear,
        "wind": for_wind,
    }


def get_home_count_by_kwatt(kwatt: float) -> int:
    return round((kwatt / ELECTRIC_USAGE_PER_YEAR), 2)


def get_result_for_one_location(location_data: pd.DataFrame) -> dict:
    _type_class = get_type(location_data)
    _intensity = get_intensity(location_data, _type_class)
    _direction = get_direction(location_data, _type_class)
    _efficency = get_efficency(_intensity, _type_class.power)
    _kwatt_per_year = get_kwatt_per_year(_efficency)
    _co2_emission = get_co2_emission(_kwatt_per_year)
    _home_count_by_kwatt = get_home_count_by_kwatt(_kwatt_per_year)
    _turbine_cost = _type_class.unit_price
    _turbine_transport_cost = _type_class.transportation_cost
    data = {
        "turbine_type": _type_class.__name__,
        "turbine_direction": _direction,
        "intensity": _intensity,
        "efficiency": round(_efficency, 2),
        "co2_emission": _co2_emission,
        "home_count_by_kwatt": _home_count_by_kwatt,
        "turbine_cost": _turbine_cost,
        "turbine_transport_cost": _turbine_transport_cost,
    }
    return data


def get_result(locations):
    data_path = settings.BASE_DIR / "static/data.csv"
    _full_df = pd.read_csv(data_path)
    _result = []

    for location in locations:
        _location_df = _full_df[_full_df["location"] == location]
        _result.append(
            {
                "data": get_result_for_one_location(_location_df)|{"lat":location.split(",")[0],"long":location.split(",")[1]},
                "location": location.split(","),
            }
        )

    return _result
