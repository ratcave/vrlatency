import vrlatency as vrl
from vrlatency.analysis import read_csv, get_tracking_latencies
import natnetclient as natnet
import matplotlib.pyplot as plt
import seaborn as sns

path = "C:/Users/sirotalab/Desktop/Measurement/tracking_exp_test.csv"

# connect to device
myarduino = vrl.Arduino.from_experiment_type(experiment_type='Tracking', port='COM9', baudrate=250000)

# specify the object that is being tracked
client = natnet.NatClient()
led = client.rigid_bodies['LED']

myexp = vrl.TrackingExperiment(arduino=myarduino,
                               rigid_body=led,
                               trials=100, trial_period=.1)

myexp.run()
myexp.save(path)

df = read_csv(path)

latencies = get_tracking_latencies(df)

sns.distplot(latencies.iloc[:-1] * 1000., bins=360)
plt.show()

# plot the data
# plt.plot(dd[:, 1]*1000, dd[:, 2])
# for x_val in np.unique(dd[:, 0]):
#     plt.axvline(x=x_val*1000, c='r')

# plt.xlabel('Time (ms)')
# plt.show()