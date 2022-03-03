import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities=['chicago','new york','washington']
        try:
            city=input("Enter which city data you would like to see, Chicago, New York or Washington:\n").lower()
        except KeyboardInterrupt:
            print('\nNo input taken')
            break
        if city not in cities:
            print("That\'s not a valid city! Enter city in Chicago, New York or Washington")
            continue
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        months=['january','february','march','april','may','june','all']
        try:
            time=input('Do you want to analyse by month, day or all:')
        except KeyboardInterrupt:
            print('\nNo input taken')
        if time=='month':
            try:
                month=input('Enter the month to analyse in January, February, March, April, May, June or all:\n').lower()
                day='all'
            except KeyboardInterrupt:
                print('\nNo input taken')
                break
            if month not in months:
                print('That\'s not a valid month! Input month in January, February, March, April, May, June or all')
                continue
            else:
                break
                break
    # get user input for day of week (all, monday, tuesday, ... sunday)
        elif time =='day':
            days=[0,1,2,3,4,5,6]
            try:
                day=int(input('Enter the day to analyse, type your response as an integer in 0~6(e.g.,1=Sunday):\n'))
                month='all'
            except KeyboardInterrupt:
                    print('\nNo input taken')
                    break
            except ValueError:
                    print('\nThat\'s not a valid number!')
                    continue
            if day not in days:
                print('That\'s not a valid day! Please input 0~6:')
                continue
            else:
                break

        elif time =='all':
            month='all'
            day='all'
            break
        else:
            print('That\'s invalid! Do you want to analyse by month,day or all?')
            continue
    print('-'*40)
    return city, month,day
    df=get_filters()
    print(df.head())

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday

    if month!='all':
        months=['january','february','march','april','may','june']
        month=months.index(month)+1
        df=df[df['month']==month]

    if day!='all':
        df=df[df['day_of_week']==day]
    return df
    print(df.head())

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most popular Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month=df['month'].mode()[0]

    # display the most common day of week
    popular_weekday=df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    popular_start_hour=df['hour'].mode()[0]

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]

    print("\nThe most popular month: {},\nThe most popualar weekday: {},\
    \nThe most popular start hour: {},\nThe most popular hour: {}".format(popular_month,\
    popular_weekday,popular_start_hour,popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_count=df['Start Station'].value_counts()[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_count =df['End Station'].value_counts()[0]
    # display most frequent combination of start station and end station trip
    #popular_trip = df.groupby(['Start Station','End Station']).size().nlargest(1)
    popular_trip = df.groupby(['Start Station','End Station']).size().nlargest(1)
    popular_trip_count=df.groupby(['Start Station','End Station'])['Start Station'].count().reset_index(name='count').sort_values('count',ascending=False)
    print("The most popular start station: {},Count:{}\nThe most popular end station: {},Count:{}\
    \nThe most popular trip:                Count:\n{}\n\n{}\n\n".format(popular_start_station,popular_start_count,\
    popular_end_station,popular_end_count, popular_trip, popular_trip_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_trip_duration=df['Trip Duration'].sum()
    print('\nThe total trip duration is:{}'.format(str(datetime.timedelta(seconds=int(total_trip_duration)))))
    # display mean travel time
    mean_trip_duration=df['Trip Duration'].mean()
    print('\nThe mean trip duration is:{}'.format(str(datetime.timedelta(seconds=int(mean_trip_duration)))))
    print("\nThis took % seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('The breakdown of users:\n{}'.format(user_counts))
    # Display counts of gender
    if 'Gender'in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nThe counts of gender types:\n{}\n'.format(gender_counts))
    else:
        print('Sorry, gender info in this city is not valid!')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year'in df.columns:
        elder_birth = df['Birth Year'].min()
        youngest_birth=df['Birth Year'].max()
        common_birth=df['Birth Year'].mode()[0]
        print('\nThe earliest year of birth is:{},\
        \nThe yougest year of birth is:{},\
        \nThe most common year of birth is:{}'.format(elder_birth,youngest_birth,common_birth))
    else:
        print('Sorry,birth info in this city is not valid ')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """ Display 5 lines raw data as requested by the user."""
    start_loc=0
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no:\n').lower()
    while True:
        if view_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = input('Do you wish to continue?: Enter yes or no\n').lower()
            if (view_data == 'yes'):
                continue
            else:
                break
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
