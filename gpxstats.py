import argparse
import sys
import os
import glob
import gpxpy
from networkx import display
import pandas as pd
import numpy as np
from geopy import distance
from math import sqrt, floor
import datetime
import pytz
from dataclasses import dataclass, field
from enum import Enum

class VerticalDirection(Enum):
    UP = 1
    DOWN = -1
    FLAT = 0

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
    track_dist_slope_gt_25: float = 0.0
    track_dist_slope_gt_20: float = 0.0
    track_dist_slope_gt_15: float = 0.0
    track_dist_slope_gt_10: float = 0.0
    track_dist_slope_0_10: float = 0.0
    track_dist_slope_lt_0: float = 0.0
    track_dist_slope_lt_minus_10: float = 0.0
    track_dist_slope_lt_minus_20: float = 0.0
    track_dist_slope_lt_minus_30: float = 0.0

@dataclass
class GPXFileStatsRecord:
    file_name: str = "" 
    tracks: list[GPXTrackStatsRecord] = field(default_factory=list)

DEFAULT_TIMEZONE = 'Europe/Berlin'
DEFAULT_MIN_MPS = 0.1
DEFAULT_MAX_PLAUSIBLE_MPS = 28.0
DEFAULT_GEODESIC_DISTANCE_CALC_METHOD = '3d'  # Options: '2d', '3d'
DEFAULT_MIN_DELTA_DISTANCE = 10.0  # Minimum distance in meters to consider for slope calculations
DEFAULT_MIN_DISTANCE_FOR_SLOPE_CALCULATION = 10.0  # Minimum distance in meters to consider for slope calculations

def get_vertical_direction(delta_elev):
    if delta_elev > 0:
        return VerticalDirection.UP
    elif delta_elev < 0:
        return VerticalDirection.DOWN
    else:
        return VerticalDirection.FLAT

def positive_float(val):
    f = float(val)
    if f <= 0:
        raise argparse.ArgumentTypeError("Value must be greater than zero.")
    return f

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

def elevation_difference(point1, point2):
    """Calculate the elevation difference between two GPX points."""
    return point2.elevation - point1.elevation

def distance_between_points(point1, point2, calc_method='2d'):
    """Calculate the distance between two GPX points using geodesic method."""
    temp_delta_geo2d = distance.distance((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).m
    if (calc_method == '2d'):
        return temp_delta_geo2d
    else:
        # Calculate 3D distance (including elevation)
        temp_delta_geo3d = np.sqrt(temp_delta_geo2d**2 + (elevation_difference(point1, point2))**2)
        return temp_delta_geo3d

# Calculate slope between points based on distance and elevation change
# Find sections in delta_ele where the vertical direction is UP or DOWN and calculate slope if the distance is greater or equal to min_distance
# Sections with FLAT vertical direction are ignored and slope is set to None
# Also, if slope is calculated, the distance for that slope is stored in slopedist, otherwise None is stored in slopedist
def calculate_slope_distances(delta_dist, delta_ele, min_distance, gpxTrackStatsRecord):
    n = len(delta_dist) - 1
    i = 1
    dist_slope_gt_25 = 0
    dist_slope_gt_20 = 0
    dist_slope_gt_15 = 0
    dist_slope_gt_10 = 0
    dist_slope_lt_0 = 0
    dist_slope_lt_minus_10 = 0
    dist_slope_lt_minus_20 = 0
    dist_slope_lt_minus_30 = 0

    slope = [None]          # slope between records
    slopedist = [None]      # distance between records with calculated slope

    while i <= n:
        # set i to start position with vertical direction UP or DOWN
 
        while True:
            if i > n:
                break
            
            verticalDirection = get_vertical_direction(delta_ele[i])
            if verticalDirection == VerticalDirection.FLAT:
                 i += 1
            else:
                break
            
        if i > n:
                break
            
        # init variables on start position
        j = i
        sum_delta_dist = 0
        sum_delta_ele = 0
        
        # advance cursor j as long j <= n and sum_delta_dist < min_distance
        # and verticalDirection does not change
        while True:
            if j > n:
                break
            
            sum_delta_dist += delta_dist[j]
            sum_delta_ele += delta_ele[j]
            
            if sum_delta_dist >= min_distance and get_vertical_direction(delta_ele[j]) == verticalDirection:
                slope.append(100 * sum_delta_ele / sum_delta_dist)
                slopedist.append(sum_delta_dist)
                j += 1
                break
            elif get_vertical_direction(delta_ele[j]) == verticalDirection:
                j += 1
            elif get_vertical_direction(delta_ele[j]) == VerticalDirection.FLAT: # turning point
                j += 1
                break
            else: # reverse direction
                break
                
        # last statements in outer loop
        i = j

    # calculate slope distance statistics
    for i in range(len(slope)):
        if slope[i] is None:
            pass
        elif slope[i] > 25:
            dist_slope_gt_25 += slopedist[i]
        elif slope[i] > 20:
            dist_slope_gt_20 += slopedist[i]
        elif slope[i] > 15:
            dist_slope_gt_15 += slopedist[i]
        elif slope[i] > 10:
            dist_slope_gt_10 += slopedist[i]
        elif slope[i] < -30:
            dist_slope_lt_minus_30 += slopedist[i]
        elif slope[i] < -20:
            dist_slope_lt_minus_20 += slopedist[i]
        elif slope[i] < -10:
            dist_slope_lt_minus_10 += slopedist[i]
        elif slope[i] < 0:
            dist_slope_lt_0 += slopedist[i]
        else:
            pass

    gpxTrackStatsRecord.track_dist_slope_gt_25 = dist_slope_gt_25
    gpxTrackStatsRecord.track_dist_slope_gt_20 = dist_slope_gt_20
    gpxTrackStatsRecord.track_dist_slope_gt_15 = dist_slope_gt_15 
    gpxTrackStatsRecord.track_dist_slope_gt_10 = dist_slope_gt_10
    gpxTrackStatsRecord.track_dist_slope_lt_0 = dist_slope_lt_0
    gpxTrackStatsRecord.track_dist_slope_lt_minus_10 = dist_slope_lt_minus_10
    gpxTrackStatsRecord.track_dist_slope_lt_minus_20 = dist_slope_lt_minus_20
    gpxTrackStatsRecord.track_dist_slope_lt_minus_30 = dist_slope_lt_minus_30
    gpxTrackStatsRecord.track_dist_slope_0_10 = gpxTrackStatsRecord.track_distance - (gpxTrackStatsRecord.track_dist_slope_gt_25 + gpxTrackStatsRecord.track_dist_slope_gt_20 + gpxTrackStatsRecord.track_dist_slope_gt_15 + gpxTrackStatsRecord.track_dist_slope_gt_10 + dist_slope_lt_0 + dist_slope_lt_minus_10 + dist_slope_lt_minus_20 + dist_slope_lt_minus_30)

    return
                    

def calculate_track_statistics(gpxPoints, gpxTrackStatsRecord, args):
    delta_elev = [0]    # change in elevation between records
    delta_time = [0]    # time interval between records
    delta_geo  = [0]   # segment distance from geodesic method only
    df = pd.DataFrame(columns=['lon', 'lat', 'elev', 'time'])

    for point in gpxPoints:
        df = pd.concat([df, pd.DataFrame({'lon' : [point.longitude], 'lat' : [point.latitude], 'elev' : [point.elevation], 'time' : [point.time]})], ignore_index=True)

    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['time'] = df['time'].dt.tz_convert(args.timezone)
        
    for idx in range(1, len(gpxPoints)): 
        start = gpxPoints[idx-1]
        end = gpxPoints[idx]

        # elevation
        delta_elev.append(elevation_difference(start, end))

        # time
        temp_delta_time = (end.time - start.time).total_seconds()
        delta_time.append(temp_delta_time)

        # distance from geodesic model
        dist = distance_between_points(start, end, args.geodesic_calc_method.lower())

        delta_geo.append(dist)
        gpxTrackStatsRecord.track_distance += dist

    gpxTrackStatsRecord.track_activity_time = datetime.timedelta(seconds=sum(delta_time))
    gpxTrackStatsRecord.track_elevation_gain = sum([e for e in delta_elev if e > 0])
    gpxTrackStatsRecord.track_maximum_height = max([p.elevation for p in gpxPoints])
    gpxTrackStatsRecord.track_elevation_loss = sum([e for e in delta_elev if e < 0])
    temp_start_time = pd.to_datetime(gpxPoints[0].time, errors='coerce')
    gpxTrackStatsRecord.track_start_time = temp_start_time.tz_convert(args.timezone)
    temp_end_time = pd.to_datetime(gpxPoints[-1].time, errors='coerce')
    gpxTrackStatsRecord.track_end_time = temp_end_time.tz_convert(args.timezone)

    df['delta_time'] = delta_time
    df["delta_elev"] = delta_elev
    calculate_slope_distances(delta_geo, delta_elev, args.MinDistanceForSlopeCalculation, gpxTrackStatsRecord)
    # df['slope'] = slope
    # df['slopedist'] = slopedist
 
    df['delta_geo'] = delta_geo 
    df['inst_mps'] = df['delta_geo'] / df['delta_time']
 
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(subset=["inst_mps"], how="all", inplace=True)
    with pd.option_context('display.max_rows', None, 'display.max_columns', 0):  # more options can be specified also
        print(df)
    df_moving = df[df['inst_mps'] >= args.MinMPS]
    avg_mov_mps = (sum((df_moving['inst_mps'] * df_moving['delta_time'])) / sum(df_moving['delta_time']))
    gpxTrackStatsRecord.track_maximum_speed = df[df['inst_mps'] <= DEFAULT_MAX_PLAUSIBLE_MPS]['inst_mps'].max(axis=0)
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
        "{} {}".format(f"Activity Time:".ljust(colwidth), f"{datetime.timedelta(seconds=row['activity_time_s'], microseconds=0)}"),
        "{} {}".format(f"Moving Time:".ljust(colwidth), f"{datetime.timedelta(seconds=row['moving_time_s'], microseconds=0)}"),
        "{} {}".format(f"Break Time:".ljust(colwidth), f"{datetime.timedelta(seconds=(row['break_time_s']), microseconds=0)}"),
        "{} {}".format(f"Max Speed (km/h):".ljust(colwidth), f"{row['maximum_speed_kmph']:.2f}"),
        "{} {}".format(f"Avg Speed (km/h):".ljust(colwidth), f"{row['average_speed_kmph']:.2f}"), 
        "{} {}".format(f"Elevation Gain (m):".ljust(colwidth), f"{row['elevation_gain_m']:.2f}"), 
        "{} {}".format(f"Elevation Loss (m):".ljust(colwidth), f"{row['elevation_loss_m']:.2f}"),
        "{} {}".format(f"Max Height (m):".ljust(colwidth), f"{row['maximum_height_m']:.2f}"), 
        "{} {}".format(f"Distance (km) Slope > 25%:".ljust(colwidth), f"{row['dist_slope_gt_25_km']:.2f} ({row['dist_slope_gt_25_km_percent']:.2f}%)"),
        "{} {}".format(f"Distance (km) Slope > 20%:".ljust(colwidth), f"{row['dist_slope_gt_20_km']:.2f} ({row['dist_slope_gt_20_km_percent']:.2f}%)"),
        "{} {}".format(f"Distance (km) Slope > 15%:".ljust(colwidth), f"{row['dist_slope_gt_15_km']:.2f} ({row['dist_slope_gt_15_km_percent']:.2f}%)"),
        "{} {}".format(f"Distance (km) Slope > 10%:".ljust(colwidth), f"{row['dist_slope_gt_10_km']:.2f} ({row['dist_slope_gt_10_km_percent']:.2f}%)"),
        "{} {}".format(f"Distance (km) Slope 0-10%:".ljust(colwidth), f"{row['dist_slope_0_10_km']:.2f} ({row['dist_slope_0_10_km_percent']:.2f}%)"),
        "{} {}".format(f"Distance (km) Slope < 0%:".ljust(colwidth), f"{row['dist_slope_lt_0_km']:.2f} ({row['dist_slope_lt_0_km_percent']:.2f}%)"),
        "{} {}".format(f"Distance (km) Slope < -10%:".ljust(colwidth), f"{row['dist_slope_lt_minus_10_km']:.2f} ({row['dist_slope_lt_minus_10_km_percent']:.2f}%)"),
        "{} {}".format(f"Distance (km) Slope < -20%:".ljust(colwidth), f"{row['dist_slope_lt_minus_20_km']:.2f} ({row['dist_slope_lt_minus_20_km_percent']:.2f}%)"),
        "{} {}".format(f"Distance (km) Slope < -30%:".ljust(colwidth), f"{row['dist_slope_lt_minus_30_km']:.2f} ({row['dist_slope_lt_minus_30_km_percent']:.2f}%)"),
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
        "maximum_height_m": "Max Height (m)",
        "dist_slope_gt_25_km": "Distance (km) Slope > 25%",
        "dist_slope_gt_20_km": "Distance (km) Slope > 20%",
        "dist_slope_gt_15_km": "Distance (km) Slope > 15%",
        "dist_slope_gt_10_km": "Distance (km) Slope > 10%",
        "dist_slope_0_10_km": "Distance (km) Slope 0-10%",
        "dist_slope_lt_0_km": "Distance (km) Slope < 0%",
        "dist_slope_lt_minus_10_km": "Distance (km) Slope < -10%",
        "dist_slope_lt_minus_20_km": "Distance (km) Slope < -20%",
        "dist_slope_lt_minus_30_km": "Distance (km) Slope < -30%"
     }, inplace=True)
     for col in results.columns:
       if col in ['Activity Time', 'Moving Time', 'Break Time']:
            results[col] = results[col].apply(lambda x: pd.Timedelta(seconds=x, microseconds=0))
       elif col in ['Start Time', 'End Time']:
            results[col] = results[col].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d %H:%M:%S'))
       elif col in ['Distance (km)', 'Max Speed (km/h)', 'Avg Speed (km/h)', 'Elevation Gain (m)', 'Max Height (m)', 'Elevation Loss (m)', 'Distance (km) Slope > 25%', 'Distance (km) Slope > 20%', 'Distance (km) Slope > 15%', 'Distance (km) Slope > 10%', 'Distance (km) Slope 0-10%', 'Distance (km) Slope < 0%', 'Distance (km) Slope < -10%', 'Distance (km) Slope < -20%', 'Distance (km) Slope < -30%']:
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
                "dist_slope_gt_25_km": track.track_dist_slope_gt_25 / 1000.0,   
                "dist_slope_gt_25_km_percent": track.track_dist_slope_gt_25 * 100 / track.track_distance,               
                "dist_slope_gt_20_km": track.track_dist_slope_gt_20 / 1000.0,
                "dist_slope_gt_20_km_percent": track.track_dist_slope_gt_20 * 100 / track.track_distance,
                "dist_slope_gt_15_km": track.track_dist_slope_gt_15 / 1000.0,
                "dist_slope_gt_15_km_percent": track.track_dist_slope_gt_15 * 100 / track.track_distance,
                "dist_slope_gt_10_km": track.track_dist_slope_gt_10 / 1000.0,
                "dist_slope_gt_10_km_percent": track.track_dist_slope_gt_10 * 100 / track.track_distance,
                "dist_slope_0_10_km": track.track_dist_slope_0_10 / 1000.0,
                "dist_slope_0_10_km_percent": track.track_dist_slope_0_10 * 100 / track.track_distance,
                "dist_slope_lt_0_km": track.track_dist_slope_lt_0 / 1000.0,
                "dist_slope_lt_0_km_percent": track.track_dist_slope_lt_0 * 100 / track.track_distance,
                "dist_slope_lt_minus_10_km": track.track_dist_slope_lt_minus_10 / 1000.0,
                "dist_slope_lt_minus_10_km_percent": track.track_dist_slope_lt_minus_10 * 100 / track.track_distance,
                "dist_slope_lt_minus_20_km": track.track_dist_slope_lt_minus_20 / 1000.0,
                "dist_slope_lt_minus_20_km_percent": track.track_dist_slope_lt_minus_20 * 100 / track.track_distance,
                "dist_slope_lt_minus_30_km": track.track_dist_slope_lt_minus_30 / 1000.0,
                "dist_slope_lt_minus_30_km_percent": track.track_dist_slope_lt_minus_30 * 100 / track.track_distance,
             })

    results = pd.DataFrame(rows)
    if args.sumTotal and not results.empty:
        totals ={"File count": len(gpxFileList),
                 "Track count": sum(len(gpx_file.tracks) for gpx_file in gpxFileList),
                 "Total distance (km)": round(results['distance_km'].sum(), 2),       
                 "Total minimum start time": results['start_time'].dt.strftime("%H:%M:%S").min(),
                 "Total maximum end time": results['end_time'].dt.strftime("%H:%M:%S").max(),   
                 "Total activity time": datetime.timedelta(seconds=results['activity_time_s'].sum(), microseconds=0),
                 "Total moving time": datetime.timedelta(seconds=results['moving_time_s'].sum(), microseconds=0),       
                 "Total break time": datetime.timedelta(seconds=results['break_time_s'].sum(), microseconds=0),
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
        type=positive_float,
        required=False,
        default=DEFAULT_MIN_MPS,
        help="minimum meters per second for moving time calculation (default: {DEFAULT_MIN_MPS} m/s)",
    )
    parser.add_argument(
            "-md",
            "--MinDistanceForSlopeCalculation",
            type=positive_float,
            required=False,
            default=DEFAULT_MIN_DISTANCE_FOR_SLOPE_CALCULATION,
            help="minimum distance in meters to consider for slope calculations (default: {DEFAULT_MIN_DISTANCE_FOR_SLOPE_CALCULATION} m)",
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
        help="method for geodesic distance calculation: '2d' or '3d' (default: 3d)",
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
        print(f"MinDistanceForSlopeCalculation: {args.MinDistanceForSlopeCalculation}")
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
