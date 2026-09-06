# gpxstats
get some statistic infos from your gpx files

gpxstats -h
usage: gpxstats.py [-h] (-f FILES [FILES ...] | -d DIRECTORY) [-r] [-m MINMPS] [-t TIMEZONE] [-g {2d,3d,2D,3D}]
                   [-c CSV] [-s] [-v]

options:
  -h, --help            show this help message and exit
  -f, --files FILES [FILES ...]
                        gpx file(s) to process
  -d, --directory DIRECTORY
                        directory containing gpx files to process
  -r, --recursive       search for gpx files recursively in subdirectories
  -m, --MinMPS MINMPS   minimum meters per second for moving time calculation (default: 0.1 m/s)
  -t, --timezone TIMEZONE
                        timezone for date/time calculations (default: Europe/Berlin)
  -g, --geodesic_calc_method {2d,3d,2D,3D}
                        method for geodesic distance calculation: '2d' or '3d' (default: 2d)
  -c, --csv CSV         output results to CSV file
  -s, --sumTotal        sum total results only, without individual file results
  -v, --verbose         display verbose output

Examples:

gpxstats.py -d '.' -v -s

Options:

files: None
directory: ['.']
recursive: False
min_mps: 0.1
timezone: Europe/Berlin
geodesic_calc_method: 2d
csv: None
verbose: True
sumTotal: True



Processing file: .\2026-08-27 17.21.15.gpx...
        Processing track: 2026-08-27 17:21:15...
Processing file: .\2026-08-30 15.55.16.gpx...
        Processing track: 2026-08-30 15:55:16...
Processing file: .\2026-09-03 16.36.27.gpx...
        Processing track: 2026-09-03 16:36:27...

Total Results:

GPX File count:           3.00
Track count:              3.00
Total distance (km):      169.92
Total minimum start time: 08:08:14
Total maximum end time:   17:21:14
Total activity time:      1 days 00:44:21
Total moving time:        0 days 19:25:06
Total break time:         0 days 05:19:15
Total maximum speed (km/h): 62.73
Total average speed (km/h): 8.82
Total elevation gain (m): 4790.96
Total elevation loss (m): -4620.68
Total maximum height (m): 1797.22

PS C:\git_projects\gpxstats>  C:\git_projects\gpxstats\gpxstats.py -f *.gpx -v -g 3d -m 0.9                                  
Options:                                                                                                                 

files: ['*.gpx']
directory: None
recursive: False
min_mps: 0.9
timezone: Europe/Berlin
geodesic_calc_method: 3d
csv: None
verbose: True
sumTotal: False



Processing file: 2026-08-27 17.21.15.gpx...
        Processing track: 2026-08-27 17:21:15...
Processing file: 2026-08-30 15.55.16.gpx...
        Processing track: 2026-08-30 15:55:16...
Processing file: 2026-09-03 16.36.27.gpx...
        Processing track: 2026-09-03 16:36:27...
1.GPX-File:               2026-08-27 17.21.15.gpx
1.Track:                  2026-08-27 17:21:15
Distance (km):            79.20
Start Time:               2026-08-27 08:08:14+02:00
End Time:                 2026-08-27 17:21:14+02:00
Activity Time:            9:13:00
Moving Time:              5:45:33
Break Time:               3:27:27
Max Speed (km/h):         63.80
Avg Speed (km/h):         13.48
Elevation Gain (m):       2011.34
Elevation Loss (m):       -1969.42
Max Height (m):           1634.49

2.GPX-File:               2026-08-30 15.55.16.gpx
1.Track:                  2026-08-30 15:55:16
Distance (km):            65.02
Start Time:               2026-08-30 08:19:13+02:00
End Time:                 2026-08-30 15:55:16+02:00
Activity Time:            7:36:03
Moving Time:              4:42:39
Break Time:               2:53:24
Max Speed (km/h):         52.59
Avg Speed (km/h):         13.45
Elevation Gain (m):       1227.89
Elevation Loss (m):       -1196.21
Max Height (m):           528.52

3.GPX-File:               2026-09-03 16.36.27.gpx
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

# Standalone MS-Windows binary distribution in dist folder

just copy the dist folder to your local computer and run there gpxstats.exe...
