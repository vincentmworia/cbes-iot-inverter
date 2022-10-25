inverter_api = {
    "main_data": {
        "input_voltage": "230V",
        "output_voltage": "230V",
        "input_frequency": "50Hz",
        "pv_voltage": "260V",
        "pv_current": "2.5A",
        "pv_power": "500W",
        "ac_and_pv_charging_current": "50A",
        "ac_charging_current": "50A",
        "pv_charging_current": "50A",
    },
    "fault_reference_code": "f02",
    "warning_indicator": "06",
    "operation_modes": {
        "standby_mode": {
            "charging_by_utility_and_pv_energy": "true",
            "charging_by_utility": "false",
            "charging_by_pv_energy": "false",
            "no_charging": "false",
        },
        "fault_mode": {
            "charging_by_utility_and_pv_energy": "true",
            "charging_by_utility": "false",
            "charging_by_pv_energy": "false",
            "no_charging": "false",
        },
        "line_mode": {
            "charging_by_utility_and_pv_energy": "true",
            "charging_by_utility": "false",
            "solar_energy_not_sufficient": "false",
            "battery_not_connected": "false",
            "power_from_utility": "false",
        },

        "battery_mode": {
            "power_from_battery_and_pv_energy": "true",
            "pv_energy_to_loads_and_charge_battery_no_utility": "false",
            "power_from_battery": "false",
            "power_from_pv_energy": "false",
        },
    }
}
