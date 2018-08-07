import vrlatency as vrl
import natnetclient as natnet
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# connect to device
myarduino = vrl.Arduino.from_experiment_type(experiment_type='Tracking', port='COM9', baudrate=250000)

# specify the object that is being tracked
client = natnet.NatClient()
led = client.rigid_bodies['LED']

myexp = vrl.TrackingExperiment(arduino=myarduino,
                               rigid_body=led,
                               trials=100, trial_period=[0.05, 1])

myexp.run()

# get the data (start_time, time, led_pos, trial_number)
dd = np.array(myexp.data.values).reshape(-1, 4)

# plot the data
plt.plot(dd[:, 1]*1000, dd[:, 2])
for x_val in np.unique(dd[:, 0]):
    plt.axvline(x=x_val*1000, c='r')

plt.xlabel('Time (ms)')
plt.show()

# ge the latency values
latencies = myexp.data.get_latency(experiment_type='Tracking',
                                   shape=(-1, 4),
                                   effect_index=2, trial_index=3,
                                   effect_time_index=1,
                                   trial_time_index=0)

# plot the histogram of the latency values
sns.distplot(latencies)
plt.show()

