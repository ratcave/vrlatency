import click
import VRLatency as vrl

@click.command()
@click.option('--port', default='COM9', help="Port that Arduino board is connected to")
@click.option('--baudrate', default=250000, help="Serial communication baudrate")
@click.option('--trials', default=20, help="Number of trials for measurement")
@click.argument('experiment_type')
def main(experiment_type, trials, port, baudrate):

    # connect to arduino
    # arduino = vrl.Arduino(experiment_type=experiment_type, port=port, baudrate=baudrate)

    # create an stimulus
    stim = vrl.Stimulus(position=(0, 0), color=(1, 0, 0))

    if experiment_type == 'Display':
        exp = vrl.DisplayExperiment(#arduino=arduino,
                                    stim=stim, on_width=0.1, off_width=[0.01, .1], trials=trials)
    elif experiment_type == 'Tracking':
        exp = vrl.TrackingExperiment(arduino=arduino)
    elif experiment_type == 'Total':
        exp = vrl.TotalExperiment(arduino=arduino)
    else:
        raise ValueError("Experiment type can only take the following arguements:"
                         "\n-Display"
                         "\n-Tracking"
                         "\n-Total")

    exp.run()


if __name__ == "__main__":
    main()
