from typing import NewType, Tuple, Union
from enum import Enum

class DaysOfWeek(str, Enum):
    Sunday = "Sunday"
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"

type Year = int
type Month = int
type Day = Union[int, float]
type Hour = int
type Minutes = int
type Seconds = float
type JulianDate = float
type DecimalTime = float
type Epoch = float
type Angle = int
type RightAscension = Time
type DecimalDegrees = float
type Obliquity = DecimalDegrees


Degrees = NewType('Degrees', Tuple[Angle, Minutes, Seconds])
Date = NewType('Date', Tuple[Year, Month, Day])
Time = NewType('Time', Tuple[Hour, Minutes, Seconds])
FullDate = NewType('FullDate', Tuple[Date, Time])
Declination = NewType('Declination', Degrees)
HourAngle = NewType('HourAngle', Time)
Longitude = Union[Degrees, DecimalDegrees, Angle]
Latitude =  Union[Degrees, DecimalDegrees, Angle]
Azimuth = NewType('Azimuth', Degrees)
Altitude = NewType('Altitude', Degrees)
GeographicCoordinates = NewType('GeographicCoordinates', Tuple[Latitude, Longitude])
HorizontalCoordinates = NewType('HorizontalCoordinates', Tuple[Altitude, Azimuth])
EquatorialCoordinatesHourAngle = NewType('EquatorialCoordinatesHourAngle', Tuple[Declination, HourAngle])
EquatorialCoordinates = NewType('EquatorialCoordinates', Tuple[Declination, RightAscension])
EclipticCoordinates = NewType('EclipticCoordinates', Tuple[Latitude, Longitude])
GalacticCoordinates = NewType('GalacticCoordinates', Tuple[Latitude, Longitude])