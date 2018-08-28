import vrlatency as vrl
from vrlatency.analysis import read_csv, get_display_latencies
import matplotlib.pyplot as plt
import seaborn as sns

path = "C:/Users/sirotalab/Desktop/Measurement/display_exp_test.csv"

# specify and connect to device
myarduino = vrl.Arduino.from_experiment_type(experiment_type='Display', port='COM9', baudrate=250000)

# create a stimulus
mystim = vrl.Stimulus(position=(0, 0), size=300)

# create an experiment
myexp = vrl.DisplayExperiment(arduino=myarduino,
                              trials=100,
                              fullscreen=True, screen_ind=1,
                              stim=mystim,
                              on_width=[.03, .06])

myexp.run()
myexp.save(path)

df = read_csv(path)
print(df.head())

latencies = get_display_latencies(df)

sns.distplot(latencies.iloc[1:] / 1000.)
plt.show()
