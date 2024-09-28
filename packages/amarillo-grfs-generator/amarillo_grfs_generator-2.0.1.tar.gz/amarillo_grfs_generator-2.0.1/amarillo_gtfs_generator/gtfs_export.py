
from collections.abc import Iterable
from datetime import datetime, timedelta
from zipfile import ZipFile
import csv
import gettext
import logging
import re

from amarillo.utils.utils import assert_folder_exists
from .models.gtfs import GtfsAgency, GtfsRoute, GtfsStop, GtfsTrip, GtfsCalendar, GtfsCalendarDate, GtfsShape, GtfsDriver, GtfsAdditionalRidesharingInfo
from amarillo_stops.stops import is_carpooling_stop
from .gtfs_constants import *
from .models.Carpool import Agency
from amarillo.models.Carpool import Driver, RidesharingInfo
from amarillo.utils.utils import geodesic_distance_in_m
from .services.trips import Trip


logger = logging.getLogger(__name__)

class GtfsExport:
    
    stops_counter = 0
    trips_counter = 0
    trip_counter = 0

    stored_stops = {}
    
    def __init__(self, agencies :  {str, Agency}, feed_info, ridestore, stopstore, bbox = None):
        self.stops = {}
        self.routes = []
        self.calendar_dates = []
        self.calendar = []
        self.trips = []
        self.stop_times = []
        self.calendar = []
        self.shapes = []
        self.drivers = {} #use a dictionary to avoid duplicate ids
        self.additional_ridesharing_infos = []
        # GtfsAgency(dict["id"], dict["name"], dict["url"], dict["timezone"], dict["lang"], dict["email"])
        self.agencies = [GtfsAgency(agency.id, agency.name, agency.url, agency.timezone, agency.lang, agency.email) for agency in agencies.values()]
        self.feed_info = feed_info
        self.localized_to = " nach "
        self.localized_short_name = "Mitfahrgelegenheit"
        self.stopstore = stopstore
        self.ridestore = ridestore
        self.bbox = bbox
            
    def export(self, gtfszip_filename, gtfsfolder):
        assert_folder_exists(gtfsfolder)
        self._prepare_gtfs_feed(self.ridestore, self.stopstore)
        self._write_csvfile(gtfsfolder, 'agency.txt', self.agencies)
        self._write_csvfile(gtfsfolder, 'feed_info.txt', self.feed_info)
        self._write_csvfile(gtfsfolder, 'routes.txt', self.routes)
        self._write_csvfile(gtfsfolder, 'trips.txt', self.trips)
        self._write_csvfile(gtfsfolder, 'calendar.txt', self.calendar)
        self._write_csvfile(gtfsfolder, 'calendar_dates.txt', self.calendar_dates)
        self._write_csvfile(gtfsfolder, 'stops.txt', self.stops.values())
        self._write_csvfile(gtfsfolder, 'stop_times.txt', self.stop_times)
        self._write_csvfile(gtfsfolder, 'shapes.txt', self.shapes)
        self._write_csvfile(gtfsfolder, 'driver.txt', self.drivers.values())
        self._write_csvfile(gtfsfolder, 'additional_ridesharing_info.txt', self.additional_ridesharing_infos)
        self._zip_files(gtfszip_filename, gtfsfolder)

    def _zip_files(self, gtfszip_filename, gtfsfolder):
        gtfsfiles = ['agency.txt', 'feed_info.txt', 'routes.txt', 'trips.txt', 
                'calendar.txt', 'calendar_dates.txt', 'stops.txt', 'stop_times.txt', 
                'shapes.txt', 'driver.txt', 'additional_ridesharing_info.txt']
        with ZipFile(gtfszip_filename, 'w') as gtfszip:
            for gtfsfile in gtfsfiles:
                gtfszip.write(gtfsfolder+'/'+gtfsfile, gtfsfile)
        
    def _prepare_gtfs_feed(self, ridestore, stopstore):
        """
        Prepares all gtfs objects in memory before they are written
        to their respective streams.
        
        For all wellknown stops a GTFS stop is created and
        afterwards all ride offers are transformed into their
        gtfs equivalents.
        """
        for stopSet in stopstore.stopsDataFrames:
            for stop in stopSet["stops"].itertuples():
                self._load_stored_stop(stop)
        cloned_trips = dict(ridestore.trips)
        groups, cloned_trips = self.group_trips_into_routes(cloned_trips)
        for group in groups:
            if self.bbox is None or any(trip.intersects(self.bbox) for trip in group.values()):
                self.convert_route(group)
        for url, trip in cloned_trips.items():
            # TODO: convert ridesharing info and driver data
            if self.bbox is None or trip.intersects(self.bbox):
                self._convert_trip(trip)

    def group_trips_into_routes(self, trips: dict):
        ungrouped_trips = dict(trips)
        route_groups = list()
        current_route_id = 1

        while len(ungrouped_trips) > 0:
            trip_id, current_trip = ungrouped_trips.popitem()

            current_group = {trip_id: current_trip}
            current_trip.route_id = current_route_id

            for other_id, other_trip in list(ungrouped_trips.items()):
                # if an ungrouped trip is from the same agency close to any of the grouped trips, add it to the route group
                # TODO: it should be possible to optimize this
                if (any(grouped_trip.agency == other_trip.agency and self.trips_are_close(other_trip, grouped_trip) for grouped_trip in current_group.values())):
                    current_group[other_id] = ungrouped_trips.pop(other_id)
                    current_group[other_id].route_id = current_route_id

            
            route_groups.append(current_group)
            current_route_id += 1

        return route_groups, trips
    
    def trips_are_close(self, trip1, trip2):
        trip1_start = trip1.path.coordinates[0]
        trip1_end = trip1.path.coordinates[-1]

        trip2_start = trip2.path.coordinates[0]
        trip2_end = trip2.path.coordinates[-1]

        res = self.within_range(trip1_start, trip2_start) and self.within_range(trip1_end, trip2_end)
        return res
    
    def within_range(self, stop1, stop2):
        MERGE_RANGE_M = 500
        return geodesic_distance_in_m(stop1, stop2) <= MERGE_RANGE_M
    
    def convert_route(self, route_group):
        agency = "multiple"

        #if there is only one agency, use that
        agencies = set(trip.agency for id, trip in route_group.items())
        if len(agencies) == 1: agency = agencies.pop()
        trip : Trip = next(iter(route_group.values())) # grab any trip, relevant values should be the same

        self.routes.append(self._create_route(agency, trip.route_id, trip.route_name, trip.route_color, trip.route_text_color))

    def _convert_trip(self, trip: Trip):
        self.trip_counter += 1
        self.calendar.append(self._create_calendar(trip))
        if not trip.runs_regularly:
            self.calendar_dates.append(self._create_calendar_date(trip))
        self.trips.append(self._create_trip(trip, self.trip_counter))
        self._append_stops_and_stop_times(trip)
        self._append_shapes(trip, self.trip_counter)

        if(trip.driver is not None):
            self.drivers[trip.driver.driver_id] = self._convert_driver(trip.driver)
        if(trip.additional_ridesharing_info is not None):
            self.additional_ridesharing_infos.append(
                self._convert_additional_ridesharing_info(trip.trip_id, trip.additional_ridesharing_info))
    
    def _convert_driver(self, driver: Driver):
        return GtfsDriver(driver.driver_id, driver.profile_picture, driver.rating)

    def _convert_additional_ridesharing_info(self, trip_id, info: RidesharingInfo):
        # if we don't specify .value, the enum will appear in the export as e.g. LuggageSize.large
        # and missing optional values get None
        def get_enum_value(enum):
            return enum.value if enum is not None else None
        
        def format_date(date: datetime):
            return date.strftime("%Y%m%d %H:%M:%S")
        
        return GtfsAdditionalRidesharingInfo(
            trip_id, info.number_free_seats, get_enum_value(info.same_gender), get_enum_value(info.luggage_size), get_enum_value(info.animal_car), 
            info.car_model, info.car_brand, format_date(info.creation_date), get_enum_value(info.smoking), info.payment_method)

    def _trip_headsign(self, destination):
        destination = destination.replace('(Deutschland)', '')
        destination = destination.replace(', Deutschland', '')
        appendix = ''
        if 'Schweiz' in destination or 'Switzerland' in destination:
            appendix = ', Schweiz'
            destination = destination.replace('(Schweiz)', '')
            destination = destination.replace(', Schweiz', '')
            destination = destination.replace('(Switzerland)', '')
        
        try:
            matches = re.match(r"(.*,)? ?(\d{4,5})? ?(.*)", destination)
        
            match = matches.group(3).strip() if matches != None else destination.strip()
            if match[-1]==')' and not '(' in match:
                match = match[0:-1] 
        
            return match + appendix
        except Exception as ex:
            logger.error("error for "+destination )
            logger.exception(ex)
            return destination
   
    def _create_route(self, agency, route_id, long_name, color, text_color): 
        return GtfsRoute(agency, route_id, long_name, RIDESHARING_ROUTE_TYPE, "", color, text_color)
        
    def _create_calendar(self, trip):
        # TODO currently, calendar is not provided by Fahrgemeinschaft.de interface.
        # We could apply some heuristics like requesting multiple days and extrapolate
        # if multiple trips are found, but better would be to have these provided by the
        # offical interface. Then validity periods should be provided as well (not
        # sure if these are available)
        # For fahrgemeinschaft.de, regurlar trips are recognizable via their url
        # which contains "regelmaessig". However, we don't know on which days of the week,
        # nor until when. As a first guess, if datetime is a mo-fr, we assume each workday,
        # if it's sa/su, only this...
        
        feed_start_date = datetime.today()
        stop_date = self._convert_stop_date(feed_start_date)
        return GtfsCalendar(trip.trip_id, stop_date, self._convert_stop_date(feed_start_date + timedelta(days=31)), *(trip.weekdays))
    
    def _create_calendar_date(self, trip):
        return GtfsCalendarDate(trip.trip_id, self._convert_stop_date(trip.start), CALENDAR_DATES_EXCEPTION_TYPE_ADDED)
    
    def _create_trip(self, trip : Trip, shape_id):
        driver_id = None if trip.driver is None else trip.driver.driver_id
        return GtfsTrip(trip.route_id, trip.trip_id, driver_id, trip.trip_id, shape_id, trip.trip_headsign, NO_BIKES_ALLOWED, trip.url)
    
    def _convert_stop(self, stop):
        """
        Converts a stop represented as pandas row to a gtfs stop.
        Expected attributes of stop: id, stop_name, x, y (in wgs84)
        """
        if stop.id:
            id = stop.id
        else:
            self.stops_counter += 1
            id = "tmp-{}".format(self.stops_counter)

        stop_name = "k.A." if stop.stop_name is None else stop.stop_name
        return GtfsStop(id, stop.y, stop.x, stop_name)
        
    def _append_stops_and_stop_times(self, trip):
        # Assumptions: 
        # arrival_time = departure_time
        # pickup_type, drop_off_type for origin: = coordinate/none
        # pickup_type, drop_off_type for destination: = none/coordinate
        # timepoint = approximate for origin and destination (not sure what consequences this might have for trip planners)
        for stop_time in trip.stop_times:
            # retrieve stop from stored_stops and mark it to be exported
            wkn_stop = self.stored_stops.get(stop_time.stop_id)
            if not wkn_stop:
                logger.warning("No stop found in stop_store for %s. Will skip stop_time %s of trip %s", stop_time.stop_id, stop_time.stop_sequence, trip.trip_id)
            else:
                self.stops[stop_time.stop_id] = wkn_stop
                # Append stop_time
                self.stop_times.append(stop_time)
        
    def _append_shapes(self, trip, shape_id):
        counter = 0
        for point in trip.path.coordinates:
                counter += 1
                self.shapes.append(GtfsShape(shape_id, point[0], point[1], counter))
            
    def _stop_hash(self, stop):
        return "{}#{}#{}".format(stop.stop_name,stop.x,stop.y)
        
    def _should_always_export(self, stop):
        """ 
        Returns true, if the given stop shall be exported to GTFS,
        regardless, if it's part of a trip or not.

        This is necessary, as potential stops are required 
        to be part of the GTFS to be referenced later on 
        by dynamicly added trips.
        """
        if self.bbox:
            return (self.bbox[0] <= stop.stop_lon <= self.bbox[2] and 
                self.bbox[1] <= stop.stop_lat <= self.bbox[3])
        else:
            return is_carpooling_stop(stop.stop_id, stop.stop_name)
            
    def _load_stored_stop(self, stop):
        gtfsstop = self._convert_stop(stop)
        stop_hash = self._stop_hash(stop)
        self.stored_stops[gtfsstop.stop_id] = gtfsstop
        if self._should_always_export(gtfsstop):
            self.stops[gtfsstop.stop_id] = gtfsstop

    def _get_stop_by_hash(self, stop_hash):
        return self.stops.get(stop_hash, self.stored_stops.get(stop_hash))
    
    def _get_or_create_stop(self, stop):
        stop_hash = self._stop_hash(stop)
        gtfsstop = self.stops.get(stop_hash)
        if gtfsstop is None:
            gtfsstop = self.stored_stops.get(stop_hash, self._convert_stop(stop))
            self.stops[stop_hash] = gtfsstop
        return gtfsstop
            
    def _convert_stop_date(self, date_time):
        return date_time.strftime("%Y%m%d")
    
    def _write_csvfile(self, gtfsfolder, filename, content):
        with open(gtfsfolder+"/"+filename, 'w', newline="\n", encoding="utf-8") as csvfile:
            self._write_csv(csvfile, content)
    
    def _write_csv(self, csvfile, content):
        if hasattr(content, '_fields'):
            writer = csv.DictWriter(csvfile, content._fields)
            writer.writeheader()
            writer.writerow(content._asdict())
        else:
            if content:
                writer = csv.DictWriter(csvfile, next(iter(content))._fields)
                writer.writeheader()
                for record in content:
                    writer.writerow(record._asdict())

    