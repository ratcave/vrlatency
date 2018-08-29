import click
import vrlatency as vrl


@click.command()
@click.option('--type', type=click.Choice(['display', 'tracking', 'total']))
@click.option('--port', default='COM9', help="Port that Arduino board is connected to")
@click.option('--baudrate', default=250000, help="Serial communication baudrate")
@click.option('--trials', default=20, help="Number of trials for measurement")
@click.option('--stimdistance', default=.01, help="Percent of screen width to move stimulus in Total experiment.")
@click.option('--stimsize', default=10, help="Size of light stimulus projected onscreen.")
@click.option('--screen', default=0, help="Monitor number to display stimulus on.")
@click.option('--interval', default=.05, help="Time duration that a stimulus is shown in a trial, in seconds.")
@click.option('--jitter/--no-jitter', default=True, help="Whether to add a randomized delay to the onset of stimulus presentation.")
@click.option('--rigid_body', default='LED', help="Name of rigid body from tracker that represents the arduino's LEDs.")
def main(type, trials, port, baudrate, stimdistance, stimsize, screen, interval, jitter, rigid_body):

    experiment_type = type
    if experiment_type.lower() != 'display':
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
    else:
        led = None

    stim = vrl.Stimulus(position=(0, 0), color=(255, 255, 255), size=stimsize)
    experiments = {'display': vrl.DisplayExperiment, 'tracking': vrl.TrackingExperiment, 'total': vrl.TotalExperiment}

    arduino = vrl.Arduino.from_experiment_type(experiment_type=experiment_type.title(), port=port, baudrate=baudrate)

    on_width = [interval, interval * 2] if jitter else interval

    params = dict(arduino=arduino, trials=trials, fullscreen=True, on_width=on_width)

    additional_params = {'display': dict(screen_ind=screen, stim=stim),
                         'tracking': dict(rigid_body=led),
                         'total': dict(screen_ind=screen, stim=stim, rigid_body=led, stim_distance=stimdistance)}
    params.update(additional_params[experiment_type.lower()])

    exp = experiments[experiment_type](**params)
    exp.run()
    exp.save()

if __name__ == "__main__":
    main()
