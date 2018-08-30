import click
import vrlatency as vrl
from vrlatency.analysis import perc_range
import matplotlib.pyplot as plt
import seaborn as sns
import time

def get_rigid_body(rigid_body):
    try:
        import natnetclient as natnet
        client = natnet.NatClient()
        try:
            led = client.rigid_bodies[rigid_body]
        except KeyError:
            raise KeyError("No Motive Rigid Body detected named '{}'.".format(rigid_body))
        if led.position is None:
            raise IOError("Motive is not sending rigid body positions")
    except ConnectionResetError:
        raise ConnectionResetError("Cannot detect Tracking Client.  Is your tracking system sending data?")

    return led


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


common_options = [
    click.option('--port', default='COM9', help="Port that Arduino board is connected to"),
    click.option('--baudrate', default=250000, help="Serial communication baudrate"),
    click.option('--trials', default=20, help="Number of trials for measurement"),
    click.option('--interval', default=.05, help="Time duration that a stimulus is shown in a trial, in seconds."),
    click.option('--jitter/--no-jitter', default=True, help="Whether to add a randomized delay to the onset of stimulus presentation.")
]


@click.group()
def cli():
    pass


@cli.command()
@add_options(common_options)
@click.option('--stimsize', default=10, help="Size of light stimulus projected onscreen.")
@click.option('--delay', default=.03, help="start delay length (secs) of trial to wait for stimulus to turn off")
@click.option('--screen', default=0, help="Monitor number to display stimulus on.")
@click.option('--allmodes/--singlemode', default=False, help="Whether to run experiment repeatedly, for all screen modes.")
def display(port, baudrate, trials, stimsize, delay, screen, interval, jitter, allmodes):
    arduino = vrl.Arduino.from_experiment_type(experiment_type='Display', port=port, baudrate=baudrate)

    stim = vrl.Stimulus(size=stimsize)
    on_width = [interval, interval * 2] if jitter else interval

    monitor = vrl.screens[screen]
    original_mode = monitor.get_mode()
    modes = monitor.get_modes() if allmodes else [original_mode]

    for mode in modes:
        if not arduino.is_connected:
            arduino.connect()

        if allmodes:
            monitor.set_mode(mode)
            time.sleep(10)

        exp = vrl.DisplayExperiment(arduino=arduino, trials=trials, fullscreen=True, on_width=on_width,
                                    trial_delay=delay, screen_ind=screen, stim=stim)
        exp.run()
        exp.save()

        df = vrl.read_csv(exp.filename)
        df['TrialTime'] = df.groupby('Trial').Time.apply(lambda x: x - x.min())

        click.echo(df.head())
        latencies = vrl.get_display_latencies(df)

        fig, (ax1, ax2, ax3) = plt.subplots(ncols=3)
        sns.distplot(df['SensorBrightness'], bins=50, ax=ax1)
        ax2.scatter(df['TrialTime'] / 1000, df['SensorBrightness'], alpha=.1, s=.2)
        # ax2.hlines([df.SensorBrightness.quantile(0.5)], *ax2.get_xlim())
        ax2.hlines([perc_range(df.SensorBrightness, .75)], *ax2.get_xlim())

        sns.distplot(latencies.iloc[1:] / 1000., bins=80, ax=ax3)
        ax3.set_xlim(0, 50)
        plt.show()


@cli.command()
@add_options(common_options)
@click.option('--rigid_body', default='LED', help="Name of rigid body from tracker that represents the arduino's LEDs.")
def tracking(port, baudrate, trials, interval, jitter, rigid_body):

    led = get_rigid_body(rigid_body)

    arduino = vrl.Arduino.from_experiment_type(experiment_type='Tracking', port=port, baudrate=baudrate)
    on_width = [interval, interval * 2] if jitter else interval
    exp = vrl.TrackingExperiment(arduino=arduino, trials=trials, fullscreen=True, on_width=on_width, rigid_body=led)
    exp.run()
    exp.save()


@cli.command()
@add_options(common_options)
@click.option('--stimdistance', default=.01, help="Percent of screen width to move stimulus in Total experiment.")
@click.option('--stimsize', default=10, help="Size of light stimulus projected onscreen.")
@click.option('--screen', default=0, help="Monitor number to display stimulus on.")
@click.option('--rigid_body', default='LED', help="Name of rigid body from tracker that represents the arduino's LEDs.")
@click.option('--allmodes/--singlemode', default=False, help="Whether to run experiment repeatedly, for all screen modes.")
def total(port, baudrate, trials, stimdistance, stimsize, screen, interval, jitter, rigid_body, allmodes):

    led = get_rigid_body(rigid_body)

    stim = vrl.Stimulus(size=stimsize)
    arduino = vrl.Arduino.from_experiment_type(experiment_type='Total', port=port, baudrate=baudrate)
    on_width = [interval, interval * 2] if jitter else interval
    exp = vrl.TotalExperiment(arduino=arduino, trials=trials, fullscreen=True, on_width=on_width, screen_ind=screen, stim=stim, rigid_body=led, stim_distance=stimdistance)
    exp.run()
    exp.save()


if __name__ == "__main__":
    cli()
