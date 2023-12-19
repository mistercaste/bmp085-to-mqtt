import os
import logging
import paho.mqtt.client as mqtt
import time
import json
import Adafruit_BMP.BMP085 as BMP085

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
SENSOR_CHECK_INTERVAL = int(os.getenv('SENSOR_CHECK_INTERVAL', 900)) # 15 minutes
DECIMAL_POINTS = int(os.getenv("SENSOR_DECIMAL_POINTS", 2))

MQTT_HOSTNAME = os.getenv("MQTT_HOSTNAME", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TIMEOUT = int(os.getenv("MQTT_TIMEOUT", 10))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", 'home/raspberrypi/bmp085')
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "raspberrypi-bmp085-to-mqtt")
MQTT_CLEAN_SESSION = os.getenv("CLIENT_CLEAN_SESSION", False)
MQTT_TLS_INSECURE = os.getenv("CLIENT_TLS_INSECURE", False)
MQTT_CLIENT_QOS = int(os.getenv("CLIENT_QOS", 4))
MQTT_USERNAME = os.getenv('MQTT_USERNAME', None)
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', None)


def configure_logging():

    level_map={
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'WARN': logging.WARNING,
        'ERROR': logging.ERROR
    }

    log_level=level_map.get(LOG_LEVEL, "Unsupported log level provided!")
    logging.basicConfig(level=log_level)


def on_connect(client, userdata, flags, rc):
    logging.info("Connected to the MQTT broker!")


def on_disconnect(client, userdata, flags, rc):
    logging.warn(f"Disconnected from the MQTT broker. End state - '{rc}'")


if __name__ == '__main__':

    configure_logging()
    bmp_sensor = BMP085.BMP085()

    if MQTT_HOSTNAME is None or MQTT_PORT is None:
        logging.error("Could not acquire MQTT broker connection parameters...")
        exit(1)

    client = mqtt.Client(MQTT_CLIENT_ID, MQTT_CLEAN_SESSION)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(MQTT_HOSTNAME, MQTT_PORT, MQTT_TIMEOUT)

    client.loop_start()
    logging.info("Successfully initialized application! Let's try to read the BMP085 sensor...")

    while True:
        try:

            pressure = bmp_sensor.read_pressure()
            temperature = bmp_sensor.read_temperature()
            altitude = bmp_sensor.read_altitude()

            if pressure is not None and temperature is not None and altitude is not None:

                logging.debug(f"BMP085 sensor values measured - pressure '{pressure}', temperature '{temperature}', altitude '{altitude}''")
                data = {'pressure': round(pressure, DECIMAL_POINTS),
                        'temperature': round(temperature, DECIMAL_POINTS),
                        'altitude': round(altitude, DECIMAL_POINTS)}

                logging.debug(f"Publishing BMP085 data to topic - '{MQTT_TOPIC}'")
                client.publish(MQTT_TOPIC, json.dumps(data))
            else:
                logging.error(f"Failed to read sensor values. Check you wiring and configuration. Retrying in {SENSOR_CHECK_INTERVAL}...")

        except Exception as e:
            logging.error(f"Something went wrong when trying to read the sensor and this shouldn't happen... Details: {e}")
        finally:
            time.sleep(SENSOR_CHECK_INTERVAL)
