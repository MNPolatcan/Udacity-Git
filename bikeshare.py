
"""
Mustafa Necip Polatcan - Turkcell Energy Solutions
"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():

    """Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter """

    print("Hello! Let's explore some US bikeshare data!")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city =input("Would you like to see data for Chicago, New York, or Washington?\n").lower()
        if city in cities:
            break
        else:
            print('Please enter valid city. (Chicago, New York, Washington)')

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        selection = input("Would you like to filter the data by month, by day, or not filter by any date at all?\n(Day, Month, None)\n").lower()
        if selection == 'month':
            month = input("Please type the name of the month you want to filter. If you do not want monthly filter enter 'all'. \n(All, January, February, March, April, May, June)\n").lower()
            day = 'all'
            if month in months:
                break
            else:
                print('Please enter a valid month.\n')
        elif selection == 'day':
            day = input("Please enter the day of the week you want to explore. If you do not want to apply a day filter enter 'all'. \n(All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)\n").lower()#PB
            month = 'all'
            if day in days:
                break
            else:
                print('Please enter a valid day.\n')
        elif selection == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            print('Please enter valid selection. (Day, Month, None)\n')

    print('-'*60)
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


    # Data of chosen city
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #  Month and Day from Start Time to new columns which will be filtered and displayed
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday


    if month != 'all':

        # saw that needed to add one to get correct month since dt.month starts with 1 and no need to add plus 1 since dt.weekday starts with 0
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]


    if day != 'all':

        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nThe Most Popular Times of Bike Travel...\n')
    start_time = time.time()

    # Convert the Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Get month & day information
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]

    # Change numeric value to month name in text
    if popular_month == 1:
        popular_month = "January"
    elif popular_month == 2:
        popular_month = "February"
    elif popular_month == 3:
        popular_month = "March"
    elif popular_month == 4:
        popular_month = "April"
    elif popular_month == 5:
        popular_month = "May"
    elif popular_month == 6:
        popular_month = "June"
    print('Most Common Month: \n', popular_month)

    df['day'] = df['Start Time'].dt.weekday
    popular_day = df['day'].mode()[0]

    # Change numeric value to weekday name in text
    if popular_day == 0:
        popular_day = "Monday"
    elif popular_day == 1:
        popular_day = "Tuesday"
    elif popular_day == 2:
        popular_day = "Wednesday"
    elif popular_day == 3:
        popular_day = "Thursday"
    elif popular_day == 4:
        popular_day = "Friday"
    elif popular_day == 5:
        popular_day = "Saturday"
    elif popular_day == 6:
        popular_day = "Sunday"
    print('Most Common Day of the Week: \n', popular_day)

    # Show the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    if popular_hour < 12:
        print('Most Common Start Hour: \n', popular_hour, ' AM')
    elif popular_hour >= 12:
        if popular_hour > 12:
            popular_hour -= 12
        print('Most Common Start Hour: \n', popular_hour, ' PM')

#show calcation time for individual tasks
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nThe Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station: \n", popular_start_station)

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most Common End Station: \n", popular_end_station)

    # Display most frequent combination of start station and end station trip
    combo_station = df['Start Station'] + " to " +  df['End Station']
    common_combo_station = combo_station.mode()[0]
    print("Most Common Trip from Start to End:\n {}".format(common_combo_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nTrip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print("The Total Travel Time is {} Hours, {} Minutes, and {} Seconds.".format(hour, minute, second))

    # Display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    minute, second = divmod(average_duration, 60)
    if minute> 60:
        hour, minute = divmod(minute, 60)
        print('The Average Travel Time is {} Hours, {} Minutes, and {} seconds.'.format(hour, minute, second))
    else:
        print('The Average Trip Duration is {} Minutes and {} Seconds.'.format(minute, second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nUser Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of Each User Type:\n", user_types)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(' ' * 60)
        print('Counts of Each User Gender:')
        print(gender)
    except:
        print('Counts of Each User Gender:\nSorry, no gender data available for {}.'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min() #Oldest birth year
        recent = df['Birth Year'].max() #Youngest birth Year
        common = df['Birth Year'].mode() #This gives the Common Birth Year
        print(' ' * 60)
        print('Counts of User Birth Year:')
        print('Oldest User(s) Birth Year: ', int(earliest))
        print('Youngest User(s) Birth Year: ', int(recent))
        print('Most Common Birth Year: ', int(common))
    except:
        print('Counts of User Birth Year:\nSorry, no birth year data available for {}.'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def individual_data(df):
    # Ask user if they want to see individual trip data.
    start_data = 0
    end_data = 5
    df_length = len(df.index)

    while start_data < df_length:
        raw_data = input("\nWould you like to see individual trip data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':

            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        print("You selected {}, {}, and {}.".format(city.title(), month.title(), day.title()))

        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        individual_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
