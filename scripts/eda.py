import pandas as pd
import matplotlib.pyplot as plt

listings = pd.read_csv('data/listings_enriched.csv')

print("Data loaded for EDA.")
print(f"Shape: {listings.shape}")

plt.figure(figsize=(10, 6))
plt.hist(listings['price_clean'].dropna(), bins=50)
plt.xlabel('Price (THB)')
plt.ylabel('Number of Listings')
plt.title('Price Distribution - Bangkok Airbnb Listings')
plt.savefig('reports/price_distribution.png')
plt.close()
print("Chart saved.")

plt.figure(figsize=(10, 6))
plt.hist(listings[listings['price_clean'] < 10000]['price_clean'].dropna(), bins=50)
plt.xlabel('Price (THB)')
plt.ylabel('Number of Listings')
plt.title('Price Distribution - Bangkok Airbnb Listings (Under 10,000 THB)')
plt.savefig('reports/price_distribution.png')
plt.close()
print("Chart saved.")

# Box Plot

plt.figure(figsize=(10, 6))
filtered = listings[listings['price_clean'] < 10000]
filtered.boxplot(column='price_clean', by='room_type')
plt.xlabel('Room Type')
plt.ylabel('Price (THB)')
plt.title('Price Distribution by Room Type - Bangkok Airbnb')
plt.suptitle('')  # removes default matplotlib title
plt.savefig('reports/price_by_roomtype.png')
plt.close()
print("Chart saved.")

print(listings.groupby('room_type')['price_clean'].describe())

# Filter outliers and remove missing coordinates for clean mapping
plt.figure(figsize=(12, 10))
filtered_geo = listings[listings['price_clean'] < 10000].dropna(subset=['latitude', 'longitude', 'price_clean'])

# Plot each listing as a point colored by price (yellow = expensive, purple = cheap)
scatter = plt.scatter(filtered_geo['longitude'], filtered_geo['latitude'], 
                       c=filtered_geo['price_clean'], cmap='viridis', 
                       s=10, alpha=0.6)

# Add color legend to interpret price scale
plt.colorbar(scatter, label='Price (THB)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Bangkok Airbnb Listings - Location & Price')

# Save chart to reports folder for inclusion in final report
plt.savefig('reports/geographic_price_map.png')
plt.close()
print("Geographic map saved.")

# top 10 biggest hosts
host_counts = listings.groupby('host_id').size().sort_values(ascending=False)
print(host_counts.head(10))
print(host_counts.describe())

#measuring the power law
total_listings = host_counts.sum()
top_1_percent_count = int(len(host_counts) * 0.01)
top_1_percent_listings = host_counts.head(top_1_percent_count).sum()
concentration_pct = (top_1_percent_listings / total_listings) * 100

print(f"Total hosts: {len(host_counts)}")
print(f"Total listings: {total_listings}")
print(f"Top 1% of hosts ({top_1_percent_count} hosts) control: {concentration_pct:.2f}% of all listings")

plt.figure(figsize=(10, 6))
top_10_hosts = host_counts.head(10)

#Top 10 Hosts by Listing Count bar graph
plt.bar(range(len(top_10_hosts)), top_10_hosts.values)
plt.xlabel('Host Rank (Top 10)')
plt.ylabel('Number of Listings')
plt.title('Top 10 Hosts by Listing Count - Bangkok Airbnb')
plt.xticks(range(len(top_10_hosts)), [f"Host {i+1}" for i in range(len(top_10_hosts))], rotation=45)
plt.savefig('reports/host_concentration.png')
plt.close()
print("Host concentration chart saved.")
