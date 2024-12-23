import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # Clean up the 'native-country' column to avoid formatting issues
    df['native-country'] = df['native-country'].str.replace('--', '-').str.strip()

    # How many of each race are represented in this dataset?
    race_count = df['race'].value_counts()  # counts num of occurrences 

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    bachelors_sum = df[df['education'] == 'Bachelors'].shape[0]  # num of rows where education is bachelors 
    education_sum = df['education'].count()  # total num of entries in education 
    percentage_bachelors = round((bachelors_sum / education_sum) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    advancedEducation = ['Bachelors', 'Masters', 'Doctorate']
    percentage_advancedEducation = round(
        (df[(df['education'].isin(advancedEducation)) & (df['salary'] == '>50K')].shape[0] / education_sum) * 100, 1
    )

    # What percentage of people without advanced education make more than 50K?
    percentage_withoutAdvancedEducation = round(
        (df[(~df['education'].isin(advancedEducation)) & (df['salary'] == '>50K')].shape[0] / education_sum) * 100, 1
    )
    
    # percentage with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[df['education'].isin(advancedEducation)].shape[0]
    lower_education = df[~df['education'].isin(advancedEducation)].shape[0]

    # Fixing the percentage with salary >50K
    higher_education_rich = round(
        (df[(df['education'].isin(advancedEducation)) & (df['salary'] == '>50K')].shape[0] / higher_education) * 100, 1
    )
    lower_education_rich = round(
        (df[(~df['education'].isin(advancedEducation)) & (df['salary'] == '>50K')].shape[0] / lower_education) * 100, 1
    )

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min() 

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[df['hours-per-week'] == min_work_hours].shape[0]
    num_min_workers_rich = df[(df['hours-per-week'] == min_work_hours) & (df['salary'] == '>50K')].shape[0]
    rich_percentage = round((num_min_workers_rich / num_min_workers) * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    country_earnings = df.groupby('native-country').apply(
        lambda x: (x[x['salary'] == '>50K'].shape[0] / len(x)) * 100
    )
    highest_earning_country = country_earnings.idxmax()
    highest_earning_country_percentage = round(country_earnings.max(), 1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df['salary'] == '>50K') & (df['native-country'] == 'India')]['occupation'].value_counts().idxmax()

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
