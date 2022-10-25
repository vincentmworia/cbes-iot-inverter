import json
from time import sleep
import paho.mqtt.client as paho
from paho import mqtt
import threading

global input_voltage
global output_voltage
global input_frequency
global pv_voltage
global pv_current
global pv_power
global ac_and_pv_charging_current
global ac_charging_current
global pv_charging_current

global fault_reference_code
global warning_indicator

global standby_charging_by_utility_and_pv_energy
global standby_charging_by_utility
global standby_charging_by_pv_energy
global standby_no_charging

global fault_mode_charging_by_utility_and_pv_energy
global fault_mode_charging_by_utility
global fault_mode_charging_by_pv_energy
global fault_mode_no_charging

global line_mode_charging_by_utility_and_pv_energy
global line_mode_charging_by_utility
global line_mode_solar_energy_not_sufficient
global line_mode_battery_not_connected
global line_mode_power_from_utility

global battery_mode_power_from_battery_and_pv_energy
global battery_mode_pv_energy_to_loads_and_charge_battery_no_utility
global battery_mode_power_from_battery
global battery_mode_power_from_pv_energy


def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def mqtt_subscription_thread():
    client.subscribe([("inverter_status", 1), ("inverter_data", 1)], qos=1)
    client.loop_forever()


def read_inverter():
    # TODO READ SERIALLY AND RETURN THE INVERTER DATA AS PER THE inverter_data_dummy.txt FILE
    inverter_dummy_data = {}
    with open("inverter_data_dummy.txt", "r") as file:
        for line in file.readlines():
            a, b = line.split(":")
            inverter_dummy_data[a.strip()] = b.strip()
    return inverter_dummy_data


def mqtt_publish_thread():
    input_voltage = 0
    output_voltage = 0
    input_frequency = 0
    pv_voltage = 0
    pv_current = 0
    pv_power = 0
    ac_and_pv_charging_current = 0
    ac_charging_current = 0
    pv_charging_current = 0

    fault_reference_code = "f02"
    warning_indicator = "06"

    standby_charging_by_utility_and_pv_energy = "false"
    standby_charging_by_utility = "false"
    standby_charging_by_pv_energy = "false"
    standby_no_charging = "false"

    fault_mode_charging_by_utility_and_pv_energy = "false"
    fault_mode_charging_by_utility = "false"
    fault_mode_charging_by_pv_energy = "false"
    fault_mode_no_charging = "false"

    line_mode_charging_by_utility_and_pv_energy = "false"
    line_mode_charging_by_utility = "false"
    line_mode_solar_energy_not_sufficient = "false"
    line_mode_battery_not_connected = "false"
    line_mode_power_from_utility = "false"

    battery_mode_power_from_battery_and_pv_energy = "false"
    battery_mode_pv_energy_to_loads_and_charge_battery_no_utility = "false"
    battery_mode_power_from_battery = "false"
    battery_mode_power_from_pv_energy = "false"
    while True:
        # client.publish("inverter_data", payload="dummy", qos=1)
        client.publish("inverter_data", payload=json.dumps({
            "main_data": {
                "input_voltage": read_inverter()["input_voltage"] + "V",
                "output_voltage": read_inverter()["output_voltage"] + "V",
                "input_frequency": read_inverter()["input_frequency"] + "Hz",
                "pv_voltage": read_inverter()["pv_voltage"] + "V",
                "pv_current": read_inverter()["pv_current"] + "A",
                "pv_power": read_inverter()["pv_power"] + "W",
                "ac_and_pv_charging_current": read_inverter()["ac_and_pv_charging_current"] + "A",
                "ac_charging_current": read_inverter()["ac_charging_current"] + "A",
                "pv_charging_current": read_inverter()["pv_charging_current"] + "A",
            },
            "fault_reference_code": read_inverter()["fault_reference_code"],
            "warning_indicator": read_inverter()["warning_indicator"],
            "operation_modes": {
                "standby_mode": {
                    "charging_by_utility_and_pv_energy": read_inverter()["standby_charging_by_utility_and_pv_energy"],
                    "charging_by_utility": read_inverter()["standby_charging_by_utility"],
                    "charging_by_pv_energy": read_inverter()["standby_charging_by_pv_energy"],
                    "no_charging": read_inverter()["standby_no_charging"],
                },
                "fault_mode": {
                    "charging_by_utility_and_pv_energy": read_inverter()[
                        "fault_mode_charging_by_utility_and_pv_energy"],
                    "charging_by_utility": read_inverter()["fault_mode_charging_by_utility"],
                    "charging_by_pv_energy": read_inverter()["fault_mode_charging_by_pv_energy"],
                    "no_charging": read_inverter()["fault_mode_no_charging"],
                },
                "line_mode": {
                    "charging_by_utility_and_pv_energy": read_inverter()["line_mode_charging_by_utility_and_pv_energy"],
                    "charging_by_utility": read_inverter()["line_mode_charging_by_utility"],
                    "solar_energy_not_sufficient": read_inverter()["line_mode_solar_energy_not_sufficient"],
                    "battery_not_connected": read_inverter()["line_mode_battery_not_connected"],
                    "power_from_utility": read_inverter()["line_mode_power_from_utility"]
                },

                "battery_mode": {
                    "power_from_battery_and_pv_energy": read_inverter()[
                        "battery_mode_power_from_battery_and_pv_energy"],
                    "pv_energy_to_loads_and_charge_battery_no_utility": read_inverter()[
                        "battery_mode_pv_energy_to_loads_and_charge_battery_no_utility"],
                    "power_from_battery": read_inverter()["battery_mode_power_from_battery"],
                    "power_from_pv_energy": read_inverter()["battery_mode_power_from_pv_energy"],
                },
            }
        }), qos=1)
        sleep(2)


if __name__ == '__main__':
    client = paho.Client(client_id="python_user", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("Vincent", "mycluster")
    client.connect("ceb1d69ea6904c50836dc3ce8214c321.s1.eu.hivemq.cloud", 8883)

    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish

    # threading.Thread(target=inverter_read_data_thread).start()
    threading.Thread(target=mqtt_subscription_thread).start()
    threading.Thread(target=mqtt_publish_thread).start()
