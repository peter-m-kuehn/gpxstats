import argparse
import sys
import os
import glob
import gpxpy
import pandas as pd
import numpy as np
from geopy import distance
from math import sqrt, floor
import datetime
import pytz
from dataclasses import dataclass, field

@dataclass
class GPXStatsRecord:
    gpx_file_count: int
    gpx_track_count: int
    total_distance: float = 0.0
    total_minimum_start_time: datetime.datetime = None
    total_maximum_end_time: datetime.datetime = None
    total_activity_time: float = 0.0
    total_maximum_speed: float = 0.0
    total_average_speed: float = 0.0
    total_moving_time: float = 0.0
    total_elevation_gain: float = 0.0
    total_maximum_height: float = 0.0
    total_maximum_elevation_gain: float = 0.0
    total_average_elevation_gain: float = 0.0
    total_elevation_loss: float = 0.0
    total_maximum_elevation_loss: float = 0.0
    total_average_elevation_loss: float = 0.0

@dataclass
class GPXTrackStatsRecord:
    track_name: str = ""
    track_distance: float = 0.0
    track_start_time: datetime.datetime = None
    track_end_time: datetime.datetime = None
    track_activity_time: float = 0.0
    track_break_time: float = 0.0
    track_maximum_speed: float = 0.0
    track_average_speed: float = 0.0
    track_moving_time: float = 0.0
    track_elevation_gain: float = 0.0
    track_maximum_height: float = 0.0
    track_elevation_loss: float = 0.0   

@dataclass
class GPXFileStatsRecord:
    file_name: str = "" 
    tracks: list[GPXTrackStatsRecord] = field(default_factory=list)

DEFAULT_TIMEZONE = 'Europe/Berlin'
DEFAULT_MIN_MPS = 0.1
DEFAULT_GEODESIC_DISTANCE_CALC_METHOD = '2d'  # Options: '2d', '3d'

def gpx_files(value):
    """Check if the provided value is a valid GPX file."""
    if not value.lower().endswith('.gpx'):
        raise argparse.ArgumentTypeError(f"{value} is not a valid GPX file.")
    return value

def existing_dir(path):
    """Validate that directory exists."""
    import os
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"Directory not found: {path}")
    return path

def existing_timezone(tz):
    """Validate that the provided timezone is valid."""
    if tz not in pytz.all_timezones:
        raise argparse.ArgumentTypeError(f"Invalid timezone: {tz}")
    return tz


def process_gpx_files(args, files, gpxFileList):
    """Process one or more GPX files and print basic statistics."""
    file_list = []
    for file in files:
        file_list.extend(glob.glob(file))
    
    if not file_list:
        return

    for file_path in file_list:
        if not os.path.isfile(file_path):
            print(f"Skipping missing file: {file_path}")
            continue
        if args.verbose:
            print(f"Processing file: {file_path}...")
        with open(file_path, "r", encoding="utf-8") as f:
            gpx = gpxpy.parse(f)

        process_gpx(gpx, file_path, args, gpxFileList)

def calculate_track_statistics(gpxPoints, gpxTrackStatsRecord, args):
    delta_elev = [0]    # change in elevation between records
    delta_time = [0]    # time interval between records
    delta_geo2d = [0]   # segment distance from geodesic method only
    delta_geo3d = [0]   # segment distance from geodesic method, adjusted for elevation
    df = pd.DataFrame(columns=['lon', 'lat', 'elev', 'time'])

    for point in gpxPoints:
        df = pd.concat([df, pd.DataFrame({'lon' : [point.longitude], 'lat' : [point.latitude], 'elev' : [point.elevation], 'time' : [point.time]})], ignore_index=True)

    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['time'] = df['time'].dt.tz_convert(args.timezone)
        
    for idx in range(1, len(gpxPoints)): 
        start = gpxPoints[idx-1]
        end = gpxPoints[idx]

        # elevation
        temp_delta_elev = end.elevation - start.elevation
        delta_elev.append(temp_delta_elev)

        # time
        temp_delta_time = (end.time - start.time).total_seconds()
        delta_time.append(temp_delta_time)

        # distance from geodesic model
        temp_delta_geo2d = distance.distance((start.latitude, start.longitude), (end.latitude, end.longitude)).m

        if (args.geodesic_calc_method.lower() == '2d'):
            delta_geo2d.append(temp_delta_geo2d)
            gpxTrackStatsRecord.track_distance += temp_delta_geo2d
        else:
            temp_delta_geo3d = sqrt(temp_delta_geo2d**2 + temp_delta_elev**2)
            delta_geo3d.append(temp_delta_geo3d)
            gpxTrackStatsRecord.track_distance += temp_delta_geo3d

    gpxTrackStatsRecord.track_activity_time = datetime.timedelta(seconds=sum(delta_time))
    gpxTrackStatsRecord.track_elevation_gain = sum([e for e in delta_elev if e > 0])
    gpxTrackStatsRecord.track_maximum_height = max([p.elevation for p in gpxPoints])
    gpxTrackStatsRecord.track_elevation_loss = sum([e for e in delta_elev if e < 0])
    temp_start_time = pd.to_datetime(gpxPoints[0].time, errors='coerce')
    gpxTrackStatsRecord.track_start_time = temp_start_time.tz_convert(args.timezone)
    temp_end_time = pd.to_datetime(gpxPoints[-1].time, errors='coerce')
    gpxTrackStatsRecord.track_end_time = temp_end_time.tz_convert(args.timezone)
    df['delta_time'] = delta_time

    if (args.geodesic_calc_method.lower() == '2d'):
        df['delta_geo2d'] = delta_geo2d 
        df['inst_mps'] = df['delta_geo2d'] / df['delta_time']
    else:
        df['delta_geo3d'] = delta_geo3d
        df['inst_mps'] = df['delta_geo3d'] / df['delta_time']

    df_moving = df[df['inst_mps'] >= args.MinMPS]
    avg_mov_mps = (sum((df_moving['inst_mps'] * df_moving['delta_time'])) / sum(df_moving['delta_time']))
    gpxTrackStatsRecord.track_maximum_speed = df['inst_mps'].max(axis=0)
    gpxTrackStatsRecord.track_average_speed = avg_mov_mps
    gpxTrackStatsRecord.track_moving_time = datetime.timedelta(seconds=sum(df_moving['delta_time']))
    gpxTrackStatsRecord.track_break_time = datetime.timedelta(seconds=gpxTrackStatsRecord.track_activity_time.total_seconds() - gpxTrackStatsRecord.track_moving_time.total_seconds())
    return

def process_gpx(gpx, file_path, args, gpxFileList):
    """Process a single GPX file"""
    # Initialize statistics
    gpxFileStatsRecord = GPXFileStatsRecord()
    gpxFileStatsRecord.file_name = os.path.basename(file_path)

    for track in gpx.tracks:
       if args.verbose:
           print(f"\tProcessing track: {track.name if track.name else 'Unnamed Track'}...")  
       gpxTrackStatsRecord = GPXTrackStatsRecord()
       gpxTrackStatsRecord.track_name = track.name if track.name else "Unnamed Track"
       gpxPoints = []
       for segment in track.segments:
            for point in segment.points:
                gpxPoints.append(point)

       calculate_track_statistics(gpxPoints, gpxTrackStatsRecord, args)
       
       gpxFileStatsRecord.tracks.append(gpxTrackStatsRecord)

    gpxFileList.append(gpxFileStatsRecord)

def process_gpx_directory(args, gpxFileList):
    """Process all GPX files in a directory, optionally recursively."""
    directory = args.directory[0] if isinstance(args.directory, list) else args.directory
    if directory is None:
        return

    if args.recursive:
        matches = []
        for root, _, files in os.walk(directory):
            for name in files:
                if name.lower().endswith(".gpx"):
                    matches.append(os.path.join(root, name))
    else:
        matches = [
            os.path.join(directory, name)
            for name in os.listdir(directory)
            if name.lower().endswith(".gpx")
        ]

    process_gpx_files(args, matches, gpxFileList)

def printResults(rows):
    """Print the rows in a formatted table."""
    colwidth=25
    for row in rows:
        print("{} {}".format(f"{row['file_no']}.GPX-File:".ljust(colwidth), f"{row['file_name']}"), 
        "{} {}".format(f"{row['track_no']}.Track:".ljust(colwidth), f"{row['track_name']}"), 
        "{} {}".format(f"Distance (km):".ljust(colwidth), f"{row['distance_km']:.2f}"),
        "{} {}".format(f"Start Time:".ljust(colwidth), f"{row['start_time']}"),
        "{} {}".format(f"End Time:".ljust(colwidth), f"{row['end_time']}"),
        "{} {}".format(f"Activity Time:".ljust(colwidth), f"{datetime.timedelta(seconds=row['activity_time_s'])}"),
        "{} {}".format(f"Moving Time:".ljust(colwidth), f"{datetime.timedelta(seconds=row['moving_time_s'])}"),
        "{} {}".format(f"Break Time:".ljust(colwidth), f"{datetime.timedelta(seconds=(row['break_time_s']))}"),
        "{} {}".format(f"Max Speed (km/h):".ljust(colwidth), f"{row['maximum_speed_kmph']:.2f}"),
        "{} {}".format(f"Avg Speed (km/h):".ljust(colwidth), f"{row['average_speed_kmph']:.2f}"), 
        "{} {}".format(f"Elevation Gain (m):".ljust(colwidth), f"{row['elevation_gain_m']:.2f}"), 
        "{} {}".format(f"Elevation Loss (m):".ljust(colwidth), f"{row['elevation_loss_m']:.2f}"),
        "{} {}".format(f"Max Height (m):".ljust(colwidth), f"{row['maximum_height_m']:.2f}"), 
        sep='\n', end='\n\n')

def printTotals(rows):
    """Print the rows in a formatted table."""
    colwidth=30
    for row in rows:
        print("{} {}".format(f"GPX File count:".ljust(colwidth), f"{row['File count']:.2f}"), 
        "{} {}".format(f"Track count:".ljust(colwidth), f"{row['Track count']:.2f}"), 
        "{} {}".format(f"Total distance (km):".ljust(colwidth), f"{row['Total distance (km)']:.2f}"),
        "{} {}".format(f"Total minimum start time:".ljust(colwidth), f"{row['Total minimum start time']}"),
        "{} {}".format(f"Total maximum end time:".ljust(colwidth), f"{row['Total maximum end time']}"),
        "{} {}".format(f"Total activity time:".ljust(colwidth), f"{row['Total activity time']}"),
        "{} {}".format(f"Total moving time:".ljust(colwidth), f"{row['Total moving time']}"),
        "{} {}".format(f"Total break time:".ljust(colwidth), f"{row['Total break time']}"),
        "{} {}".format(f"Total maximum speed (km/h):".ljust(colwidth), f"{row['Total maximum speed (km/h)']:.2f}"),
        "{} {}".format(f"Total average speed (km/h):".ljust(colwidth), f"{row['Total average speed (km/h)']:.2f}"), 
        "{} {}".format(f"Total elevation gain (m):".ljust(colwidth), f"{row['Total elevation gain (m)']:.2f}"), 
        "{} {}".format(f"Total elevation loss (m):".ljust(colwidth), f"{row['Total elevation loss (m)']:.2f}"),
        "{} {}".format(f"Total maximum height (m):".ljust(colwidth), f"{row['Total maximum height (m)']:.2f}"), 
        sep='\n', end='\n\n')

def fix_columns(results):
     results.rename(columns={
        "file_name": "GPX-File",
        "file_no": "File No.",
        "track_name": "Track Name",
        "track_no": "Track No.",
        "distance_km": "Distance (km)",
        "start_time": "Start Time",
        "end_time": "End Time",
        "activity_time_s": "Activity Time",
        "moving_time_s": "Moving Time",
        "break_time_s": "Break Time",
        "maximum_speed_kmph": "Max Speed (km/h)",
        "average_speed_kmph": "Avg Speed (km/h)",
        "elevation_gain_m": "Elevation Gain (m)",
        "elevation_loss_m": "Elevation Loss (m)",
        "maximum_height_m": "Max Height (m)"
     }, inplace=True)
     for col in results.columns:
       if col in ['Activity Time', 'Moving Time', 'Break Time']:
            results[col] = results[col].apply(lambda x: pd.Timedelta(seconds=x))
       elif col in ['Start Time', 'End Time']:
            results[col] = results[col].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d %H:%M:%S'))
       elif col in ['Distance (km)', 'Max Speed (km/h)', 'Avg Speed (km/h)', 'Elevation Gain (m)', 'Max Height (m)', 'Elevation Loss (m)']:
            results[col] = results[col].apply(lambda x: round(x, 2))

def process_results(gpxFileList, args):
    """Output the statistics collected from the processed GPX files."""
    rows = []
    i_file = 0
    for gpx_file in gpxFileList:
        i_file += 1
        i_track = 0
        for track in gpx_file.tracks:
            i_track += 1
            rows.append({
                "file_name": gpx_file.file_name,
                "file_no" : i_file,
                "track_name": track.track_name,
                "track_no" : i_track,
                "distance_km": track.track_distance / 1000.0,
                "start_time": track.track_start_time,
                "end_time": track.track_end_time,
                "activity_time_s": track.track_activity_time.total_seconds(),
                "moving_time_s": track.track_moving_time.total_seconds(),
                "break_time_s": track.track_break_time.total_seconds(),
                "maximum_speed_kmph": 3.6 * track.track_maximum_speed,
                "average_speed_kmph": 3.6 * track.track_average_speed,
                "elevation_gain_m": track.track_elevation_gain,
                "elevation_loss_m": track.track_elevation_loss,
                "maximum_height_m": track.track_maximum_height,
             })

    results = pd.DataFrame(rows)
    if args.sumTotal and not results.empty:
        totals ={"File count": len(gpxFileList),
                 "Track count": sum(len(gpx_file.tracks) for gpx_file in gpxFileList),
                 "Total distance (km)": round(results['distance_km'].sum(), 2),       
                 "Total minimum start time": results['start_time'].dt.strftime("%H:%M:%S").min(),
                 "Total maximum end time": results['end_time'].dt.strftime("%H:%M:%S").max(),   
                 "Total activity time": datetime.timedelta(seconds=results['activity_time_s'].sum()),
                 "Total moving time": datetime.timedelta(seconds=results['moving_time_s'].sum()),       
                 "Total break time": datetime.timedelta(seconds=results['break_time_s'].sum()),
                 "Total maximum speed (km/h)": round(results['maximum_speed_kmph'].max(), 2),
                 "Total average speed (km/h)": round(results['average_speed_kmph'].mean(), 2),
                 "Total elevation gain (m)": round(results['elevation_gain_m'].sum(), 2),
                 "Total elevation loss (m)": round(results['elevation_loss_m'].sum(), 2),
                 "Total maximum height (m)": round(results['maximum_height_m'].max(), 2)
        }
        total = pd.DataFrame(totals, index=[0])
        
        if args.csv:
            total.to_csv(args.csv, index=False, sep=';', encoding='utf-8')
        else:
            print("\nTotal Results:\n")
            printTotals(total.to_dict('records'))

        sys.exit(0)

    if args.csv:
        fix_columns(results)
        results.to_csv(args.csv, index=False, sep=';', encoding='utf-8')
    elif results.empty:
        print("No GPX tracks found.")
    else:
        printResults(rows)

def main():
    # get command line arguments
    parser = argparse.ArgumentParser()
    file_dir_group = parser.add_mutually_exclusive_group(required=True)
    file_dir_group.add_argument(
        "-f",
        "--files",
        type=gpx_files,
        required=False,
        nargs='+',
        help="gpx file(s) to process",
    )
    file_dir_group.add_argument(
        "-d",
        "--directory",
        type=existing_dir,
        required=False,
        nargs=1,
        help="directory containing gpx files to process",
    )
    parser.add_argument(
            "-r",
            "--recursive",
            required=False,
            default=False,
            action="store_true",
            help="search for gpx files recursively in subdirectories",
        )
    parser.add_argument(
        "-m",
        "--MinMPS",
        type=float,
        required=False,
        default=DEFAULT_MIN_MPS,
        help="minimum meters per second for moving time calculation (default: {DEFAULT_MIN_MPS} m/s)",
    )
    parser.add_argument(
        "-t",
        "--timezone",
        type=existing_timezone,
        required=False,
        default=DEFAULT_TIMEZONE,
        help="timezone for date/time calculations (default: Europe/Berlin)",
    )
    parser.add_argument(
        "-g",
        "--geodesic_calc_method",
        type=str,
        required=False,
        default=DEFAULT_GEODESIC_DISTANCE_CALC_METHOD,
        choices=['2d', '3d', '2D', '3D'],
        help="method for geodesic distance calculation: '2d' or '3d' (default: 2d)",
    )
    parser.add_argument(
            "-c",
            "--csv",
            type=str,
            required=False,
            help="output results to CSV file",
        )
    parser.add_argument(
            "-s",
            "--sumTotal",
            action="store_true",
            required=False,
            default=False,
            help="sum total results only, without individual file results",
        )    
    parser.add_argument(
                "-v",
                "--verbose",
                action="store_true",
                required=False,
                default=False,
                help="display verbose output",
            )    
    
    args = parser.parse_args()
    if args.files and args.recursive:
        parser.error("--files and --recursive options cannot be used together.")
        sys.exit(1)
    if args.verbose:   
        print(f"Options:\n")     
        print(f"files: {args.files}")
        print(f"directory: {args.directory}")
        print(f"recursive: {args.recursive}")
        print(f"min_mps: {args.MinMPS}")
        print(f"timezone: {args.timezone}")
        print(f"geodesic_calc_method: {args.geodesic_calc_method}")
        print(f"csv: {args.csv}")
        print(f"verbose: {args.verbose}")
        print(f"sumTotal: {args.sumTotal}")
        print(f"\n\n")

    gpxFileList = list[GPXFileStatsRecord]()

    if args.files:
        process_gpx_files(args, args.files, gpxFileList)
    elif args.directory:
        process_gpx_directory(args, gpxFileList)
    else:
        print("No files [-f] or directory [-d] specified.")
        sys.exit(1)

    process_results(gpxFileList, args) 


if __name__ == "__main__":
    main()
