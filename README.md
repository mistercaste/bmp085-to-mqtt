# bmp085-to-mqtt
An ARM-RaspberryPI dockerized Python application to send BMP085 sensor values to an MQTT broker 

- Setup a static IP address (optional, strongly suggested) with `nmtui`
- Rasperry PI's I2C interfacing must be enabled (`raspi-config` -> `Interface options` -> `I2C` -> REBOOT)
- Before running, please create a `.env` file in the main folder, looking like:

## Docker sample
```
docker run -name bmp085-to-mqtt --privileged --restart=unless-stopped --network host -e MQTT_HOSTNAME=nas.home -e MQTT_USERNAME=${MQTT_USERNAME} -e MQTT_PASSWORD=${MQTT_PASSWORD} mistercaste/bmp085-to-mqtt
```

## Docker compose sample
```
services:
  bmp085-to-mqtt:
    image: mistercaste/bmp085-to-mqtt:1.0.1
    container_name: bmp085-to-mqtt
    network_mode: host
    privileged: true
    restart: always
    environment:
      - MQTT_HOSTNAME=nas.home
      - MQTT_USERNAME=${MQTT_USERNAME}
      - MQTT_PASSWORD=${MQTT_PASSWORD}
```
