import vrlatency as vrl
from vrlatency.analysis import read_csv, get_total_latencies
import natnetclient as natnet
import matplotlib.pyplot as plt
import seaborn as sns


path = "C:/Users/sirotalab/Desktop/Measurement/total_exp_test.csv"

# connect to device
myarduino = vrl.Arduino.from_experiment_type(experiment_type='Total', port='COM9', baudrate=250000)

# create a stimulus
mystim = vrl.Stimulus(position=(800, 400), size=700)

# specify the object that is being tracked
client = natnet.NatClient()
led = client.rigid_bodies['LED']

# create an experiment app
myexp = vrl.TotalExperiment(arduino=myarduino,
                            stim=mystim,
                            on_width=[.1, .3],
                            rigid_body=led,
                            trials=100,
                            screen_ind=1,
                            fullscreen=True)
myexp.run()
myexp.save(path)

df = read_csv(path)
print(df.head())

latencies = get_total_latencies(df)
sns.distplot(latencies)
plt.show()

# # get the data
# dd = np.array(myexp.data.values).reshape(-1, 5)
#
# # plot the data
# plt.plot(dd[:, 0]/1000, dd[:, 1])
# plt.plot(dd[:, 0]/1000, dd[:, 2])
# plt.plot(dd[:, 0]/1000, dd[:, 4]*350)
# plt.xlabel('Time (ms)')
# plt.show()
