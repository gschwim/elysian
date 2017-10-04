#!/usr/bin/python3

import click, time, tsxlib, json

@click.group()
def cli():
    pass
#
# @click.group()
# def mount():
#     pass
#
# @click.group()
# def camera():
#     pass
#
# # cli = click.CommandCollection(sources=[mount, camera])


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
def mount_status(ip):
    mount = tsxlib.mount(ip)
    print(json.dumps(mount.GetStatus()))


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





if __name__ == '__main__':
    cli()
