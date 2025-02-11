import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker

# Set random seed for reproducibility
np.random.seed(150)
fake = Faker('en_IN')

# Generate dataset
num_orders = 100000
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

# Customers Data
customers = [{
    'customer_id': fake.unique.random_number(digits=8),
    'customer_name': fake.name(),
    'email': fake.email(),
    'phone': f"+91{fake.msisdn()[3:]}",
    'registration_date': fake.date_between(start_date=start_date, end_date=end_date),
    'customer_segment': random.choice(['New', 'Regular', 'Premium', 'Inactive'])
} for _ in range(num_orders // 2)]

# Products Data
categories = ['Fruits', 'Dairy', 'Snacks', 'Beverages', 'Frozen', 'Grocery']
products = [{
    'product_id': fake.unique.random_number(digits=6),
    'product_name': fake.word() + ' ' + fake.word(),
    'category': random.choice(categories),
    'price': round(random.uniform(10, 1000), 2)
} for _ in range(200)]

# Orders Data
orders = []
order_items = []

for _ in range(num_orders):
    customer = random.choice(customers)
    order_date = fake.date_time_between(start_date=start_date, end_date=end_date)
    order_id = fake.unique.random_number(digits=10)
    num_items = random.randint(1, 8)
    order_products = random.sample(products, num_items)
    order_total = sum(p['price'] for p in order_products)
    
    orders.append({
        'order_id': order_id,
        'customer_id': customer['customer_id'],
        'order_date': order_date,
        'order_total': round(order_total, 2)
    })
    
    for product in order_products:
        order_items.append({
            'order_id': order_id,
            'product_id': product['product_id'],
            'quantity': random.randint(1, 3),
            'unit_price': product['price']
        })

# Convert to DataFrames
df_customers = pd.DataFrame(customers)
df_products = pd.DataFrame(products)
df_orders = pd.DataFrame(orders)
df_order_items = pd.DataFrame(order_items)

# Merge all into one dataset
df = df_orders.merge(df_order_items, on='order_id', how='outer')
df = df.merge(df_customers, on='customer_id', how='outer')
df = df.merge(df_products, on='product_id', how='outer')

# Save to CSV
df.to_csv('blinkit_complete_data.csv', index=False)
print("Merged dataset saved as blinkit_complete_data.csv")
