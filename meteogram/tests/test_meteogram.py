"""Test use of the meteogram module."""

import datetime
from pathlib import Path
from unittest.mock import patch

import numpy as np
from numpy.testing import assert_almost_equal, assert_array_almost_equal
import pytest

from meteogram import meteogram


@pytest.fixture
def load_example_asos():
    """Fixture to load example data"""
    example_data_path = Path(__file__).resolve().parent / 'staticdata'
    data_path = example_data_path / 'AMW_example_data.csv'
    return meteogram.download_asos_data(data_path)


#
# Example starter test
#
def test_degF_to_degC_at_freezing():
    """
    Test if celsius conversion is correct at freezing.
    """
    # Setup
    freezing_degF = 32.0
    freezing_degC = 0.0

    # Exercise
    result = meteogram.degF_to_degC(freezing_degF)

    # Verify
    assert result == freezing_degC

    # Cleanup - none necessary

#
# Instructor led introductory examples
#
def test_title_case():
    # Setup
    in_string = 'this is a test string'
    desired = 'This Is A Test String'

    # Exercise
    actual = in_string.title()

    # Verify
    assert actual == desired

    # Cleanup - none necessary
#
# Instructor led examples of numerical comparison
#

#
# Exercise 1
#
def test_build_asos_request_url_single_digit_datetimes():
    """
    Test building URL with single digit month and day.
    """
    # Setup
    start_date = datetime.datetime(2020, 2, 1, 1)
    end_date = datetime.datetime(2020, 2, 5, 1)
    station = 'EST'

    desired = r'https://mesonet.agron.iastate.edu/request/asos/1min_dl.php?station%5B%5D=EST&tz=UTC&year1=2020&month1=02&day1=01&hour1=01&minute1=00&year2=2020&month2=02&day2=05&hour2=01&minute2=00&vars%5B%5D=tmpf&vars%5B%5D=dwpf&vars%5B%5D=sknt&vars%5B%5D=drct&sample=1min&what=view&delim=comma&gis=yes'

    # Exercise
    result = meteogram.build_asos_request_url(station, start_date, end_date)

    # Verify
    assert result == desired

    # Cleanup - none necessary


def test_build_asos_request_url_double_digit_datetimes():
    """
    Test building URL with double digit month and day.
    """
    # Setup
    start_date = datetime.datetime(2019, 12, 24, 1)
    end_date = datetime.datetime(2019, 12, 25, 1)
    station = 'EST'

    desired = r'https://mesonet.agron.iastate.edu/request/asos/1min_dl.php?station%5B%5D=EST&tz=UTC&year1=2019&month1=12&day1=24&hour1=01&minute1=00&year2=2019&month2=12&day2=25&hour2=01&minute2=00&vars%5B%5D=tmpf&vars%5B%5D=dwpf&vars%5B%5D=sknt&vars%5B%5D=drct&sample=1min&what=view&delim=comma&gis=yes'

    # Exercise
    result = meteogram.build_asos_request_url(station, start_date, end_date)

    # Verify
    assert result == desired

    # Cleanup - none necessary

#
# Exercise 1 - Stop Here
#


def test_does_three_equal_three():
    assert 3 == 3
#
# Exercise 2 - Add calculation tests here
#


def test_floating_subtraction():
    # Setup
    desired = 0.293

    # Exercise
    actual = 1 - 0.707

    # Verify
    assert_almost_equal(actual, desired)

    # Cleanup - None necessary
#
# Exercise 2 - Stop Here
#


def test_wind_components_zero_speed():
    # Setup
    speed = 0
    direction = 0
    desired_u = 0
    desired_v = 0

    # Exercise
    actual = meteogram.wind_components(speed, direction)

    # Verify
    assert_almost_equal(actual, (desired_u, desired_v))
    # Cleanup - None needed


def test_wind_components_0_deg():
    # Setup
    speed = 10
    direction = 0
    desired_u = 0
    desired_v = -10

    # Exercise
    actual = meteogram.wind_components(speed, direction)

    # Verify
    assert_almost_equal(actual, (desired_u, desired_v))
    # Cleanup - None necessary


def test_wind_components_45_deg():
    # Setup
    speed = 12
    direction = 45
    desired_u = - np.sqrt(2) / 2 * 12  # prefer to hard code the float
    desired_v = - np.sqrt(2) / 2 * 12

    # Exercise
    actual = meteogram.wind_components(speed, direction)

    # Verify
    assert_almost_equal(actual, (desired_u, desired_v))

    # Cleanup - None necessary


def test_wind_components_360_deg():
    # Setup
    speed = 1
    direction = 360
    desired_u = 0
    desired_v = - 1

    # Exercise
    actual = meteogram.wind_components(speed, direction)

    # Verify
    assert_almost_equal(actual, (desired_u, desired_v))

    # Cleanup - None necessary


def test_wind_components_array():
    # vectorized version to combine tests
    # Setup
    speed = np.array([10, 10, 10, 0])
    direction = np.array([0, 45, 360, 45])

    # Exercise
    actual = meteogram.wind_components(speed, direction)

    # Verify
    true_components = np.array(([0, -7.0710, 0, 0], [-10, -7.0710, -10, 0]))
    assert_array_almost_equal(actual, true_components, 3)

    # Cleanup - None


#
# Instructor led mock example
#
# RG: mocks are to replace a different function


def mocked_current_utc_time():
    """Mock utc time function for testing with defaults"""
    return datetime.datetime(2018, 3, 26, 12)

@patch('meteogram.meteogram.current_utc_time', new=mocked_current_utc_time)
def test_that_mock_works():
    """Test that we used mocked current_utc_time correctly"""
    # Setup - None
    # Exercise
    result = meteogram.current_utc_time()

    # Verify
    truth = datetime.datetime(2018, 3, 26, 12)
    assert result == truth

#
# Exercise 3
#


# ideally, test three cases:
#     start_time but no end_time
#     no start_time but end_time
#     and the one below,
@patch('meteogram.meteogram.current_utc_time', new=mocked_current_utc_time)
def test_build_asos_request_url_default_times():
    # Setup
    station = 'EST'

    # Exercise
    actual = meteogram.build_asos_request_url(station)

    # Verify
    desired = r'https://mesonet.agron.iastate.edu/request/asos/1min_dl.php?station%5B%5D=EST&tz=UTC&year1=2018&month1=03&day1=25&hour1=12&minute1=00&year2=2018&month2=03&day2=26&hour2=12&minute2=00&vars%5B%5D=tmpf&vars%5B%5D=dwpf&vars%5B%5D=sknt&vars%5B%5D=drct&sample=1min&what=view&delim=comma&gis=yes'
    assert actual == desired

    # Cleanup - None
#
# Exercise 3 - Stop Here
#

#
# Exercise 4 - Add any tests that you can to increase the library coverage.
# think of cases that may not change coverage, but should be tested
# for as well.
#
# RG:  run $pytest --cov-report term-missing --cov


def test_current_utc_time():
    # Setup - None

    # Exercise
    actual = meteogram.current_utc_time()

    # Verify
    assert abs(actual - datetime.datetime.utcnow()) < datetime.timedelta(seconds=1)

    # Cleanup - None


def test_potential_temperature():
    # Setup
    pressure = 800  #hPa
    temperature = 273  # K

    # Exercise
    actual = meteogram.potential_temperature(pressure, temperature)

    # Verify
    desired = 290.96  # K
    assert_almost_equal(actual, desired, 2)
#
# Exercise 4 - Stop Here
#

#
# Instructor led example of image testing
#


@pytest.mark.mpl_image_compare(remove_text=True)
def test_plotting_meteogram_defaults(load_example_asos):
    # Setup
    # Exercise
    fig, _, _, _ = meteogram.plot_meteogram(load_example_asos)

    # Verify - Done elsewhere

    # Cleanup - None
    return fig
#
# Exercise 5
#

#
# Exercise 5 - Stop Here
#

#
# Exercise 6
#

#
# Exercise 6 - Stop Here
#

#
# Exercise 7
#

#
# Exercise 7 - Stop Here
#

# Demonstration of TDD here (time permitting)
