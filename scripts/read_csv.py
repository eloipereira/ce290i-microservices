from gps_replay.ingestors import gps_generator_from_csv

data = gps_generator_from_csv("data/dataset_gps.csv")
print(next(data))
print(next(data))
print(next(data))
