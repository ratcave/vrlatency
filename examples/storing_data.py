import vrlatency as vrl

data = vrl.Data()

# let's create some imaginary data
data.values = [1,2,3,4,5,6,7,8,9]

# set the parameters of the experiment
exp_params = {'Model':'XYZ', 'Name':'Uknown', 'Type':'Some_type', 'Made in':'Iran'}

# set the culomn names of the data
culomn_labels = ['culomn_1', 'culomn_2', 'culomn_3']

# set the path
path = "C:/Users/Mohammad Bashiri/Desktop/testing.csv"

# save the data now
data.to_csv(path, experiment_params=exp_params, data_culomns=culomn_labels)
