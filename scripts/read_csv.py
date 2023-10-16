from data_layer.gps import gps_generator_from_csv
from data_layer.gps import replay_from_csv_to_redis

data = gps_generator_from_csv("data/dataset_gps.csv")
print(next(data))
print(next(data))
print(next(data))
