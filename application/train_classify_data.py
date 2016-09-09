#! usr/bin/env python3

start_interval = 200
end_interval = 5100
interval = 100

for reviews_to_train in range(start_interval, end_interval, interval):

#This module calls the data_prep module, which pulls data out of the database in a format that scikit-learn can use.
