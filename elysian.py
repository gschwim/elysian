#!/usr/bin/python3

import click, time, tsxlib, json
import paho.mqtt.client as mqtt

@click.group()
def cli():
    pass


@cli.command()
@click.option('--ip', required=True)
@click.option('--plain', is_flag=True)
def mount_state(ip, plain):
    mount = tsxlib.mount(ip)
    try:
        output = {
            'time': time.ctime(),
            'parked': mount.IsParked()
        }
        if plain:
            print(output['parked']['parked'])
        else:
            print(output)
            return output
    except:
        state = 'Could not enumerate mount park state!'
        print(state)
        return state

@cli.command()
@click.option('--ip', required=True)
@click.option('--mqtt-ip')
@click.option('--mqtt-topic')
def mount_status(ip, mqtt_ip, mqtt_topic):
    data = tsxlib.mount(ip).GetStatus()
    mqtt_publish(mqtt_ip, mqtt_topic, json.dumps(data))



@cli.command()
@click.option('--ip', default='127.0.0.1')
@click.option('--plain', is_flag=True)
def park(ip, plain):
    mount = tsxlib.mount(ip)
    try:
        output = {
            'time': time.ctime(),
            'output': mount.ParkAndDoNotDisconnect()
        }
        if plain:
            print(output['output'])
        else:
            print(output)
            return(output)
    except:
        output = 'Could not park!'
        print(output)
        return output


#
# @mount.command()
# def park():
#     pass
# @camera.command()
# def image():
#     pass
#
#
# # mount.add_command(park)
# # camera.add_command(image)

def mqtt_publish(mqtt_ip, mqtt_topic, data):
    mqttc = mqtt.Client(client_id="elysian")
    mqttc.connect(mqtt_ip)
    mqttc.publish(mqtt_topic, str(data))
    mqttc.loop(2)





if __name__ == '__main__':
    cli()
