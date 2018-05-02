import click
import VRLatency as vrl

@click.command()
@click.option('--port', default='COM9', help="Port that Arduino board is connected to")
@click.option('--baud', default=250000, help="Serial communication baudrate")
@click.option('--trials', default=0, help="Number of trials for measurement")
@click.argument('mode')

def main(mode, trials, port, baud):

    # connect to arduino
    arduino = vrl.connect_to_device(port=port, baudrate=baud)

    # create an experiment objecta and attach the device to it
    exp = vrl.Experiment(trials=trials, device=arduino)

    exp.create_window(screen_ind=0)

    exp.create_stim(type='Plane')
    exp.stim.point_size = 20.
    exp.stim.position.xyz = 0, 0, -3

    exp.run(mode=mode, on_width=.05, off_width=[.1, .3])


if __name__ == "__main__":
    main()
