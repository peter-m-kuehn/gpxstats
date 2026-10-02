# gpxstats
get some statistic infos from your gpx files

gpxstats -h
usage: gpxstats.py [-h] (-f FILES [FILES ...] | -d DIRECTORY) [-r] [-m MINMPS] [-md MINDISTANCEFORSLOPECALCULATION] [-t TIMEZONE] [-g {2d,3d,2D,3D}] [-c CSV] [-s] [-v]

options:
  -h, --help            show this help message and exit
  -f, --files FILES [FILES ...]
                        gpx file(s) to process
  -d, --directory DIRECTORY
                        directory containing gpx files to process
  -r, --recursive       search for gpx files recursively in subdirectories
  -m, --MinMPS MINMPS   minimum meters per second for moving time calculation (default: 0.1 m/s)
  -md, --MinDistanceForSlopeCalculation MINDISTANCEFORSLOPECALCULATION
                        minimum distance in meters to consider for slope calculations (default: 20.0 m)
  -t, --timezone TIMEZONE
                        timezone for date/time calculations (default: Europe/Berlin)
  -g, --geodesic_calc_method {2d,3d,2D,3D}
                        method for geodesic distance calculation: '2d' or '3d' (default: 3d)
  -c, --csv CSV         output results to CSV file
  -s, --sumTotal        sum total results only, without individual file results
  -v, --verbose         display verbose output

Examples:

gpxstats.py -f 2026-09*.gpx -v -s
Options:

files: ['2026-09*.gpx']
directory: None
recursive: False
min_mps: 0.1
timezone: Europe/Berlin
geodesic_calc_method: 3d
MinDistanceForSlopeCalculation: 20.0
csv: None
verbose: True
sumTotal: True



Processing file: 2026-09-07 14.58.01-elefixed.gpx...
        Processing track: 2026-09-07 14:58:01...
Processing file: 2026-09-07 14.58.01-org.gpx...
        Processing track: 2026-09-07 14:58:01...
Processing file: 2026-09-23 14.06.55.gpx...
        Processing track: 2026-09-23 14:06:55...

Total Results:

GPX File count:                3.00
Track count:                   3.00
Total distance (km):           102.24
Total minimum start time:      08:36:43
Total maximum end time:        14:58:01
Total activity time:           0 days 17:58:47
Total moving time:             0 days 13:40:17
Total break time:              0 days 04:18:30
Total maximum speed (km/h):    68.78
Total average speed (km/h):    7.34
Total elevation gain (m):      3939.80
Total elevation loss (m):      -3718.20
Total maximum height (m):      1660.40
Total distance (km) Slope > 25% 0.92
Total distance (km) Slope > 20% 1.22
Total distance (km) Slope > 15% 4.05
Total distance (km) Slope > 10% 7.84
Total distance (km) Slope 0-10% 46.96
Total distance (km) Slope < 0% 29.02
Total distance (km) Slope < -10% 9.56
Total distance (km) Slope < -20% 2.13
Total distance (km) Slope < -30% 0.55

gpxstats.py -f 2026-09*.gpx -m 0.9 -v                                  
Options:

files: ['2026-09*.gpx']
directory: None
recursive: False
min_mps: 0.9
timezone: Europe/Berlin
geodesic_calc_method: 3d
MinDistanceForSlopeCalculation: 20.0
csv: None
verbose: True
sumTotal: False



Processing file: 2026-09-07 14.58.01-elefixed.gpx...
        Processing track: 2026-09-07 14:58:01...
Processing file: 2026-09-07 14.58.01-org.gpx...
        Processing track: 2026-09-07 14:58:01...
Processing file: 2026-09-23 14.06.55.gpx...
        Processing track: 2026-09-23 14:06:55...
1.GPX-File:               2026-09-07 14.58.01-elefixed.gpx
1.Track:                  2026-09-07 14:58:01
Distance (km):            40.49
Start Time:               2026-09-07 08:43:43+02:00
End Time:                 2026-09-07 14:58:01+02:00
Activity Time:            6:14:18
Moving Time:              3:42:23
Break Time:               2:31:55
Max Speed (km/h):         68.78
Avg Speed (km/h):         10.51
Elevation Gain (m):       1340.40
Elevation Loss (m):       -1340.40
Max Height (m):           1259.80
Distance (km) Slope > 25%: 0.19 (0.48%)
Distance (km) Slope > 20%: 0.27 (0.66%)
Distance (km) Slope > 15%: 1.00 (2.48%)
Distance (km) Slope > 10%: 2.80 (6.91%)
Distance (km) Slope 0-10%: 20.80 (51.36%)
Distance (km) Slope < 0%: 11.00 (27.16%)
Distance (km) Slope < -10%: 3.35 (8.27%)
Distance (km) Slope < -20%: 0.97 (2.39%)
Distance (km) Slope < -30%: 0.12 (0.30%)

2.GPX-File:               2026-09-07 14.58.01-org.gpx
1.Track:                  2026-09-07 14:58:01
Distance (km):            40.56
Start Time:               2026-09-07 08:43:43+02:00
End Time:                 2026-09-07 14:58:01+02:00
Activity Time:            6:14:18
Moving Time:              3:42:37
Break Time:               2:31:41
Max Speed (km/h):         68.56
Avg Speed (km/h):         10.51
Elevation Gain (m):       1258.20
Elevation Loss (m):       -1147.70
Max Height (m):           1264.50
Distance (km) Slope > 25%: 0.20 (0.49%)
Distance (km) Slope > 20%: 0.19 (0.47%)
Distance (km) Slope > 15%: 0.89 (2.20%)
Distance (km) Slope > 10%: 2.45 (6.05%)
Distance (km) Slope 0-10%: 20.60 (50.79%)
Distance (km) Slope < 0%: 12.97 (31.97%)
Distance (km) Slope < -10%: 2.52 (6.20%)
Distance (km) Slope < -20%: 0.66 (1.62%)
Distance (km) Slope < -30%: 0.09 (0.22%)

3.GPX-File:               2026-09-23 14.06.55.gpx
1.Track:                  2026-09-23 14:06:55
Distance (km):            21.19
Start Time:               2026-09-23 08:36:43+02:00
End Time:                 2026-09-23 14:06:54+02:00
Activity Time:            5:30:11
Moving Time:              2:20:28
Break Time:               3:09:43
Max Speed (km/h):         52.57
Avg Speed (km/h):         8.01
Elevation Gain (m):       1341.20
Elevation Loss (m):       -1230.10
Max Height (m):           1660.40
Distance (km) Slope > 25%: 0.53 (2.50%)
Distance (km) Slope > 20%: 0.76 (3.60%)
Distance (km) Slope > 15%: 2.15 (10.15%)
Distance (km) Slope > 10%: 2.59 (12.23%)
Distance (km) Slope 0-10%: 5.56 (26.24%)
Distance (km) Slope < 0%: 5.06 (23.86%)
Distance (km) Slope < -10%: 3.69 (17.43%)
Distance (km) Slope < -20%: 0.51 (2.40%)
Distance (km) Slope < -30%: 0.34 (1.58%)


# Standalone MS-Windows binary distribution in dist folder (created with pyinstaller - see https://pyinstaller.org/en/stable/operating-mode.html)

just copy the dist folder to your local computer and run there gpxstats.exe...
