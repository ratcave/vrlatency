import click
import VRLatency as vrl

@click.command()
@click.option('--port', default='COM9', help="Port that Arduino board is connected to")
@click.option('--baud', default=250000, help="Serial communication baudrate")
@click.option('--trials', default=0, help="Number of trials for measurement")
@click.argument('mode')

def main(mode, trials, port, baud):

    # connect to arduino
    arduino = vrl.Arduino(experiment_type='Display', )

    # create an experiment objecta and attach the device to it
    exp = vrl.BaseExperiment(trials=trials, arduino=arduino)

    exp.run(mode=mode, on_width=.05, off_width=[.1, .3])


if __name__ == "__main__":
    main()
