# Use TS information:
import csv, sys

slowdownx = float(sys.argv[1])
last_microsecond = 0
with open('/opt/temp/tstamps.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    current_microsecond = int(row[2])
    if line_count > 0:
      print("file '/opt/temp/out.%06d.raw.tiff'\nduration %08f" % (int(row[1]), slowdownx * float(current_microsecond - last_microsecond) / float(1000000)))
    line_count += 1
    last_microsecond = current_microsecond
