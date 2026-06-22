import pandas as pd

def load_data():
    print("Loading data...")
    
    listings = pd.read_csv('data/listings.csv.gz', compression='gzip')
    listings_simple = pd.read_csv('data/listings.csv')
    reviews = pd.read_csv('data/reviews.csv')
    calendar = pd.read_csv('data/calendar.csv.gz', compression='gzip')
    neighbourhoods = pd.read_csv('data/neighbourhoods.csv')
    
    # Get price from simple file and merge into detailed file
    listings_simple['price_clean'] = listings_simple['price'].replace('[\$,]', '', regex=True).astype(float)
    listings = listings.merge(listings_simple[['id', 'price_clean']], on='id', how='left')
    
    print(f"Listings: {listings.shape}")
    print(f"Reviews: {reviews.shape}")
    print(f"Calendar: {calendar.shape}")
    print(f"Neighbourhoods: {neighbourhoods.shape}")
    
    return listings, reviews, calendar, neighbourhoods

def profile_data(df, name):
    print(f"\n=== PROFILE: {name} ===")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"\nNull rates (%):")
    null_rates = (df.isnull().sum() / len(df) * 100).round(2)
    print(null_rates[null_rates > 0])
    print(f"\nColumn cardinality (unique values):")
    print(df.nunique())

def save_quality_report(listings, reviews, calendar, neighbourhoods):
    with open('reports/data_quality_report.txt', 'w', encoding='utf-8') as f:
        for df, name in [(listings, 'LISTINGS'), (reviews, 'REVIEWS'),
                         (calendar, 'CALENDAR'), (neighbourhoods, 'NEIGHBOURHOODS')]:
            f.write(f"\n=== {name} ===\n")
            f.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}\n")
            null_rates = (df.isnull().sum() / len(df) * 100).round(2)
            f.write(f"Null Rates:\n{null_rates[null_rates > 0]}\n\n")
            f.write(f"Unique Values:\n{df.nunique()}\n\n")

def check_duplicates(listings, reviews, calendar):
    print("\n=== DUPLICATE CHECK ===")
    print(f"Duplicate listings: {listings.duplicated(subset=['id']).sum()}")
    print(f"Duplicate reviews: {reviews.duplicated().sum()}")
    print(f"Duplicate calendar entries: {calendar.duplicated(subset=['listing_id','date']).sum()}")

def remove_duplicates(reviews):
    before = len(reviews)
    reviews = reviews.drop_duplicates()
    after = len(reviews)
    print(f"Removed {before - after} duplicate reviews")
    return reviews

def detect_outliers(listings):
    print("\n=== OUTLIER DETECTION ===")
    print("Price stats:")
    print(listings['price_clean'].describe())
    print("\nAvailability stats:")
    print(listings['availability_365'].describe())
    print("\nNumber of reviews stats:")
    print(listings['number_of_reviews'].describe())

# Run everything
listings, reviews, calendar, neighbourhoods = load_data()
profile_data(listings, "LISTINGS")
profile_data(reviews, "REVIEWS")
profile_data(calendar, "CALENDAR")
profile_data(neighbourhoods, "NEIGHBOURHOODS")
save_quality_report(listings, reviews, calendar, neighbourhoods)
print("Quality report saved.")
check_duplicates(listings, reviews, calendar)
reviews = remove_duplicates(reviews)
detect_outliers(listings)

listings_simple = pd.read_csv('data/listings.csv')
print(listings_simple['price'].head(10))
print(listings_simple['price'].dtype)