# gpxstats
get some statistic infos from your gpx files

gpxstats -h
usage: gpxstats [-h] (-f FILES [FILES ...] | -d DIRECTORY) [-r] [-m MINMPS] [-md MINDISTANCEFORSLOPECALCULATION]
                [-t TIMEZONE] [-g {2d,3d,2D,3D}] [-c CSV] [-s] [-v]

options:
  -h, --help            show this help message and exit
  -f, --files FILES [FILES ...]
                        gpx file(s) to process
  -d, --directory DIRECTORY
                        directory containing gpx files to process
  -r, --recursive       search for gpx files recursively in subdirectories
  -m, --MinMPS MINMPS   minimum meters per second for moving time calculation (default: {DEFAULT_MIN_MPS} m/s)
  -md, --MinDistanceForSlopeCalculation MINDISTANCEFORSLOPECALCULATION
                        minimum distance in meters to consider for slope calculations (default:
                        {DEFAULT_MIN_DISTANCE_FOR_SLOPE_CALCULATION} m)
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
MinDistanceForSlopeCalculation: 10.0
csv: None
verbose: True
sumTotal: True



Processing file: 2026-09-03 16.36.27.gpx...
        Processing track: 2026-09-03 16:36:27...
Processing file: 2026-09-07 14.58.01.gpx...
        Processing track: 2026-09-07 14:58:01...
Processing file: 2026-09-10 14.59.02.gpx...
        Processing track: 2026-09-10 14:59:02...
Processing file: 2026-09-12 16.41.08.gpx...
        Processing track: 2026-09-12 16:41:08...
Processing file: 2026-09-17 20.44.28.gpx...
        Processing track: 2026-09-17 20:44:28...
Processing file: 2026-09-19 15.28.27.gpx...
        Processing track: 2026-09-19 15:28:27...
Processing file: 2026-09-23 14.06.55.gpx...
        Processing track: 2026-09-23 14:06:55...
Processing file: 2026-09-25 14.22.31.gpx...
        Processing track: 2026-09-25 14:22:31...
Processing file: 2026-09-27 15.05.24.gpx...
        Processing track: 2026-09-27 15:05:24...

Total Results:

GPX File count:                9.00
Track count:                   9.00
Total distance (km):           374.03
Total minimum start time:      08:36:43
Total maximum end time:        20:44:28
Total activity time:           2 days 12:59:24
Total moving time:             2 days 00:19:00
Total break time:              0 days 12:40:24
Total maximum speed (km/h):    68.56
Total average speed (km/h):    7.67
Total elevation gain (m):      11688.60
Total elevation loss (m):      -10968.81
Total maximum height (m):      1797.22
Total distance (km) Slope > 25% 2.66
Total distance (km) Slope > 20% 3.02
Total distance (km) Slope > 15% 10.46
Total distance (km) Slope > 10% 25.92
Total distance (km) Slope 0-10% 166.46
Total distance (km) Slope < 0% 127.78
Total distance (km) Slope < -10% 29.22
Total distance (km) Slope < -20% 6.59
Total distance (km) Slope < -30% 1.92

PS C:\git_projects\gpxstats>  C:\git_projects\gpxstats\gpxstats.py -f 2026-09*.gpx -m 0.9 -v                                  
Options:                                                                                                                 

files: ['2026-09*.gpx']
directory: None
recursive: False
min_mps: 0.9
timezone: Europe/Berlin
geodesic_calc_method: 3d
MinDistanceForSlopeCalculation: 10.0
csv: None
verbose: True
sumTotal: False



Processing file: 2026-09-03 16.36.27.gpx...
        Processing track: 2026-09-03 16:36:27...
Processing file: 2026-09-07 14.58.01.gpx...
        Processing track: 2026-09-07 14:58:01...
Processing file: 2026-09-10 14.59.02.gpx...
        Processing track: 2026-09-10 14:59:02...
Processing file: 2026-09-12 16.41.08.gpx...
        Processing track: 2026-09-12 16:41:08...
Processing file: 2026-09-17 20.44.28.gpx...
        Processing track: 2026-09-17 20:44:28...
Processing file: 2026-09-19 15.28.27.gpx...
        Processing track: 2026-09-19 15:28:27...
Processing file: 2026-09-23 14.06.55.gpx...
        Processing track: 2026-09-23 14:06:55...
Processing file: 2026-09-25 14.22.31.gpx...
        Processing track: 2026-09-25 14:22:31...
Processing file: 2026-09-27 15.05.24.gpx...
        Processing track: 2026-09-27 15:05:24...
1.GPX-File:               2026-09-03 16.36.27.gpx
1.Track:                  2026-09-03 16:36:27
Distance (km):            26.46
Start Time:               2026-09-03 08:41:09+02:00
End Time:                 2026-09-03 16:36:27+02:00
Activity Time:            7:55:18
Moving Time:              2:49:15
Break Time:               5:06:03
Max Speed (km/h):         47.41
Avg Speed (km/h):         6.92
Elevation Gain (m):       1551.73
Elevation Loss (m):       -1455.05
Max Height (m):           1797.22
Distance (km) Slope > 25%: 1.02 (3.86%)
Distance (km) Slope > 20%: 0.77 (2.92%)
Distance (km) Slope > 15%: 1.40 (5.31%)
Distance (km) Slope > 10%: 3.28 (12.38%)
Distance (km) Slope 0-10%: 8.06 (30.47%)
Distance (km) Slope < 0%: 6.05 (22.84%)
Distance (km) Slope < -10%: 3.75 (14.18%)
Distance (km) Slope < -20%: 1.68 (6.36%)
Distance (km) Slope < -30%: 0.44 (1.68%)

2.GPX-File:               2026-09-07 14.58.01.gpx
1.Track:                  2026-09-07 14:58:01
Distance (km):            40.43
Start Time:               2026-09-07 08:45:09+02:00
End Time:                 2026-09-07 14:58:01+02:00
Activity Time:            6:12:52
Moving Time:              3:42:05
Break Time:               2:30:47
Max Speed (km/h):         68.56
Avg Speed (km/h):         10.51
Elevation Gain (m):       1163.50
Elevation Loss (m):       -1147.50
Max Height (m):           1264.50
Distance (km) Slope > 25%: 0.08 (0.19%)
Distance (km) Slope > 20%: 0.22 (0.55%)
Distance (km) Slope > 15%: 0.98 (2.43%)
Distance (km) Slope > 10%: 2.62 (6.47%)
Distance (km) Slope 0-10%: 19.50 (48.23%)
Distance (km) Slope < 0%: 13.47 (33.32%)
Distance (km) Slope < -10%: 2.79 (6.91%)
Distance (km) Slope < -20%: 0.63 (1.56%)
Distance (km) Slope < -30%: 0.14 (0.34%)

3.GPX-File:               2026-09-10 14.59.02.gpx
1.Track:                  2026-09-10 14:59:02
Distance (km):            44.33
Start Time:               2026-09-10 09:28:11+02:00
End Time:                 2026-09-10 14:59:02+02:00
Activity Time:            5:30:51
Moving Time:              3:03:34
Break Time:               2:27:17
Max Speed (km/h):         28.83
Avg Speed (km/h):         13.71
Elevation Gain (m):       335.00
Elevation Loss (m):       -276.60
Max Height (m):           608.30
Distance (km) Slope > 25%: 0.03 (0.07%)
Distance (km) Slope > 20%: 0.03 (0.06%)
Distance (km) Slope > 15%: 0.04 (0.09%)
Distance (km) Slope > 10%: 0.17 (0.39%)
Distance (km) Slope 0-10%: 29.01 (65.44%)
Distance (km) Slope < 0%: 14.75 (33.27%)
Distance (km) Slope < -10%: 0.29 (0.65%)
Distance (km) Slope < -20%: 0.01 (0.03%)
Distance (km) Slope < -30%: 0.00 (0.00%)

4.GPX-File:               2026-09-12 16.41.08.gpx
1.Track:                  2026-09-12 16:41:08
Distance (km):            41.94
Start Time:               2026-09-12 08:37:49+02:00
End Time:                 2026-09-12 16:41:08+02:00
Activity Time:            8:03:19
Moving Time:              4:01:14
Break Time:               4:02:05
Max Speed (km/h):         51.23
Avg Speed (km/h):         9.78
Elevation Gain (m):       1587.78
Elevation Loss (m):       -1485.51
Max Height (m):           1257.70
Distance (km) Slope > 25%: 0.38 (0.91%)
Distance (km) Slope > 20%: 0.57 (1.37%)
Distance (km) Slope > 15%: 1.59 (3.79%)
Distance (km) Slope > 10%: 3.01 (7.18%)
Distance (km) Slope 0-10%: 18.63 (44.44%)
Distance (km) Slope < 0%: 12.28 (29.29%)
Distance (km) Slope < -10%: 3.82 (9.12%)
Distance (km) Slope < -20%: 1.32 (3.14%)
Distance (km) Slope < -30%: 0.32 (0.77%)

5.GPX-File:               2026-09-17 20.44.28.gpx
1.Track:                  2026-09-17 20:44:28
Distance (km):            85.66
Start Time:               2026-09-17 10:25:13+02:00
End Time:                 2026-09-17 20:44:28+02:00
Activity Time:            10:19:15
Moving Time:              6:42:07
Break Time:               3:37:08
Max Speed (km/h):         66.52
Avg Speed (km/h):         12.44
Elevation Gain (m):       1645.99
Elevation Loss (m):       -1598.75
Max Height (m):           536.62
Distance (km) Slope > 25%: 0.14 (0.17%)
Distance (km) Slope > 20%: 0.12 (0.14%)
Distance (km) Slope > 15%: 0.71 (0.83%)
Distance (km) Slope > 10%: 2.90 (3.38%)
Distance (km) Slope 0-10%: 40.66 (47.47%)
Distance (km) Slope < 0%: 36.80 (42.96%)
Distance (km) Slope < -10%: 3.52 (4.10%)
Distance (km) Slope < -20%: 0.70 (0.81%)
Distance (km) Slope < -30%: 0.12 (0.14%)

6.GPX-File:               2026-09-19 15.28.27.gpx
1.Track:                  2026-09-19 15:28:27
Distance (km):            31.97
Start Time:               2026-09-19 09:25:41+02:00
End Time:                 2026-09-19 15:28:26+02:00
Activity Time:            6:02:45
Moving Time:              3:11:08
Break Time:               2:51:37
Max Speed (km/h):         54.30
Avg Speed (km/h):         9.33
Elevation Gain (m):       1186.00
Elevation Loss (m):       -1093.70
Max Height (m):           1300.50
Distance (km) Slope > 25%: 0.08 (0.26%)
Distance (km) Slope > 20%: 0.07 (0.21%)
Distance (km) Slope > 15%: 1.22 (3.82%)
Distance (km) Slope > 10%: 3.41 (10.67%)
Distance (km) Slope 0-10%: 14.22 (44.49%)
Distance (km) Slope < 0%: 8.90 (27.83%)
Distance (km) Slope < -10%: 2.91 (9.11%)
Distance (km) Slope < -20%: 0.90 (2.80%)
Distance (km) Slope < -30%: 0.26 (0.80%)

7.GPX-File:               2026-09-23 14.06.55.gpx
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
Distance (km) Slope > 25%: 0.58 (2.74%)
Distance (km) Slope > 20%: 0.80 (3.77%)
Distance (km) Slope > 15%: 2.06 (9.72%)
Distance (km) Slope > 10%: 2.52 (11.87%)
Distance (km) Slope 0-10%: 5.32 (25.10%)
Distance (km) Slope < 0%: 5.28 (24.89%)
Distance (km) Slope < -10%: 3.70 (17.43%)
Distance (km) Slope < -20%: 0.52 (2.45%)
Distance (km) Slope < -30%: 0.43 (2.01%)

8.GPX-File:               2026-09-25 14.22.31.gpx
1.Track:                  2026-09-25 14:22:31
Distance (km):            32.69
Start Time:               2026-09-25 09:19:49+02:00
End Time:                 2026-09-25 14:22:30+02:00
Activity Time:            5:02:41
Moving Time:              2:53:07
Break Time:               2:09:34
Max Speed (km/h):         56.52
Avg Speed (km/h):         10.76
Elevation Gain (m):       1313.80
Elevation Loss (m):       -1219.70
Max Height (m):           1607.80
Distance (km) Slope > 25%: 0.28 (0.86%)
Distance (km) Slope > 20%: 0.31 (0.94%)
Distance (km) Slope > 15%: 1.50 (4.59%)
Distance (km) Slope > 10%: 3.05 (9.33%)
Distance (km) Slope 0-10%: 11.14 (34.08%)
Distance (km) Slope < 0%: 12.64 (38.67%)
Distance (km) Slope < -10%: 2.94 (9.01%)
Distance (km) Slope < -20%: 0.62 (1.90%)
Distance (km) Slope < -30%: 0.21 (0.63%)

9.GPX-File:               2026-09-27 15.05.24.gpx
1.Track:                  2026-09-27 15:05:24
Distance (km):            49.34
Start Time:               2026-09-27 08:43:12+02:00
End Time:                 2026-09-27 15:05:24+02:00
Activity Time:            6:22:12
Moving Time:              4:09:05
Break Time:               2:13:07
Max Speed (km/h):         56.45
Avg Speed (km/h):         11.68
Elevation Gain (m):       1563.60
Elevation Loss (m):       -1461.90
Max Height (m):           1671.90
Distance (km) Slope > 25%: 0.06 (0.12%)
Distance (km) Slope > 20%: 0.13 (0.27%)
Distance (km) Slope > 15%: 0.94 (1.91%)
Distance (km) Slope > 10%: 4.97 (10.07%)
Distance (km) Slope 0-10%: 19.91 (40.35%)
Distance (km) Slope < 0%: 17.61 (35.69%)
Distance (km) Slope < -10%: 5.50 (11.15%)
Distance (km) Slope < -20%: 0.21 (0.42%)
Distance (km) Slope < -30%: 0.01 (0.02%)


# Standalone MS-Windows binary distribution in dist folder (created with pyinstaller - see https://pyinstaller.org/en/stable/operating-mode.html)

just copy the dist folder to your local computer and run there gpxstats.exe...
