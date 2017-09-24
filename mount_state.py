#!/usr/bin/python3

import click, time, tsxlib


@click.command()
@click.option('--ip', required=True)
def mount_state(ip):
    mount = tsxlib.mount(ip)
    try:
        state = mount.IsParked()
        output = {
            'time': time.ctime(),
            'parked': state
        }
        print(output)
        return output
    except:
        state = 'Could not enumerate mount park state!'
        print(state)
        return state


if __name__ == '__main__':
    mount_state()


