import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        try:
            city = input('please enter name of the city you to explore: ').lower()
            filename = CITY_DATA[city]
            break
        except:
            print('Oops...please enter a valid city name: ')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            all_months = input('do you want results for all months?. please enter "y" if yes and "n" no:')
            if all_months == 'y' :
                month = 'all'
            elif all_months == 'n':
                month = input('which month do you want results to be for: please note that available months are from januray to june: ')    
            check_month =['all','january', 'february', 'march', 'april', 'may', 'june'].index(month.lower())
            break
        except:
            print('please enter a valid value')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            all_days = input('do you want results for all days?. please enter "y" if yes and "n" no:')
            if all_days == 'y' :
                day = 'all'
            elif all_days == 'n':
                day = input('which day do you want results to be for: ')
            check_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'satrday', 'sunday', 'all'].index(day.lower())
            break
        except:
            print('please enter a valid day')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('most common month of the year is: ',most_common_month)
    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('most common day of the week is: ',most_common_day)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('most common start station is: ',most_common_start_station)
    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('most common end station is: ',most_common_end_station)
    # display most frequent combination of start station and end station trip
    trips = (df['Start Station'].astype(str) +'  to   ')+ df['End Station']
    popular_trip = trips.mode()[0]
    print('Most Popular trip:', popular_trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('total travel time is: ', total_time)
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('average travel time is: ', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('counts of user types is: ', user_types)

    # Display counts of gender    
    try:
        gender_counts = df['Gender'].value_counts()
        print('counts of gender is: ', gender_counts)
        # Display earliest, most recent, and most common year of birth
        sorted_birth_year = df['Birth Year'].copy().sort_values()
        most_recent =  sorted_birth_year.dropna().values[-1]
        earliest_year = sorted_birth_year.values[0]
        most_common = df['Birth Year'].mode()[0]
        print('most recent year is: ', most_recent)
        print('earlist year is: ',earliest_year)
        print('most common year is: ',most_common)
        view_raw_data = input('would you like to see a data sample:enter y for yes and n for no ')
        while view_raw_data == 'y' :
            print(df.head())
            view_raw_data = input('would you like to see a data sample:enter y for yes and n for no ')
    except:
        print('washington has no data on gender or birth date')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'no':
            break
        else:
            main()


if __name__ == "__main__":
	main()
