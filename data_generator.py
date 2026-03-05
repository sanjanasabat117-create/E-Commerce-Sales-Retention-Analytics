import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Ensure the 'data' directory exists
os.makedirs('data', exist_ok=True)

# ----------------- Configuration -----------------
NUM_USERS = 5000
NUM_PRODUCTS = 200
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 3, 1)
DAYS_RANGE = (END_DATE - START_DATE).days

# ----------------- 1. Generate Products -----------------
print("Generating Products...")
# Business Context: We define categories with realistic ranges. 
# Clothing has higher return rates due to sizing, while Beauty has the lowest due to hygiene restrictions.
categories = {
    'Electronics': {'price_range': (50, 1500), 'cost_margin': (0.6, 0.8), 'return_rate': 0.1},
    'Clothing': {'price_range': (15, 200), 'cost_margin': (0.3, 0.5), 'return_rate': 0.15},
    'Home & Kitchen': {'price_range': (20, 500), 'cost_margin': (0.4, 0.6), 'return_rate': 0.08},
    'Sports': {'price_range': (25, 300), 'cost_margin': (0.5, 0.7), 'return_rate': 0.05},
    'Beauty': {'price_range': (10, 150), 'cost_margin': (0.2, 0.4), 'return_rate': 0.03}
}

products = []
for i in range(1, NUM_PRODUCTS + 1):
    category = random.choice(list(categories.keys()))
    price = round(random.uniform(*categories[category]['price_range']), 2)
    # Cost is a percentage of price
    cost = round(price * random.uniform(*categories[category]['cost_margin']), 2)
    products.append({
        'product_id': i,
        'category': category,
        'product_name': f"{category} Item {i}",
        'price': price,
        'cost': cost
    })

df_products = pd.DataFrame(products)
df_products.to_csv('data/products.csv', index=False)


# ----------------- 2. Generate Users -----------------
print("Generating Users...")
countries = ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'France', 'India', 'Japan']
country_weights = [0.4, 0.15, 0.1, 0.1, 0.08, 0.07, 0.05, 0.05]

users = []
for i in range(1, NUM_USERS + 1):
    join_date = START_DATE + timedelta(days=random.randint(0, DAYS_RANGE))
    users.append({
        'user_id': i,
        'first_name': f"User_{i}_First",
        'last_name': f"User_{i}_Last",
        'email': f"user{i}@example.com",
        'country': random.choices(countries, weights=country_weights)[0],
        'join_date': join_date.strftime('%Y-%m-%d'),
        'age': random.randint(18, 65)
    })

df_users = pd.DataFrame(users)
df_users['join_date'] = pd.to_datetime(df_users['join_date'])
df_users.to_csv('data/users.csv', index=False)


# ----------------- 3. Generate Sessions -----------------
print("Generating Sessions...")
devices = ['Mobile', 'Desktop', 'Tablet']
device_weights = [0.6, 0.35, 0.05]

NUM_SESSIONS = NUM_USERS * random.randint(3, 8) 
sessions = []
for i in range(1, NUM_SESSIONS + 1):
    user_id = random.randint(1, NUM_USERS)
    # Data Integrity Check: Session date MUST be after user join date. 
    # Realistically, users spend some time on the site after joining.
    user_join = df_users.loc[df_users['user_id'] == user_id, 'join_date'].values[0]
    user_join = pd.to_datetime(user_join)
    
    max_days = (END_DATE - user_join).days
    if max_days < 0:
        continue
        
    session_date = user_join + timedelta(days=random.randint(0, max_days))
    duration = random.randint(10, 3600) # seconds
    bounce = 1 if duration < 30 else 0
    
    sessions.append({
        'session_id': i,
        'user_id': user_id,
        'session_start': session_date.strftime('%Y-%m-%d %H:%M:%S'),
        'duration_seconds': duration,
        'is_bounce': bounce,
        'device': random.choices(devices, weights=device_weights)[0]
    })

df_sessions = pd.DataFrame(sessions)
df_sessions['session_start'] = pd.to_datetime(df_sessions['session_start'])


# ----------------- 4. Generate Orders & Order Items -----------------
print("Generating Orders and Order Items...")
orders = []
order_items = []

order_counter = 1
order_item_counter = 1

# Filter sessions that did not bounce - potential buyers
valid_sessions = df_sessions[df_sessions['is_bounce'] == 0]

for _, session in valid_sessions.iterrows():
    # 15% conversion rate from valid sessions
    if random.random() < 0.15:
        user_id = session['user_id']
        order_date = session['session_start']
        
        num_items = random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.3, 0.1, 0.05, 0.05])[0]
        
        order_total = 0
        items_in_order = []
        
        for _ in range(num_items):
            product = random.choice(products)
            qtw = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0]
            price = product['price']
            
            items_in_order.append({
                'order_item_id': order_item_counter,
                'order_id': order_counter,
                'product_id': product['product_id'],
                'quantity': qtw,
                'unit_price': price
            })
            order_total += price * qtw
            order_item_counter += 1
            
        # Funnel Logic: Most orders are delivered, but we maintain a small percentage 
        # of cancellations and processing states for operational realism.
        status = random.choices(['Delivered', 'Shipped', 'Processing', 'Cancelled'], 
                                weights=[0.85, 0.05, 0.02, 0.08])[0]
                                
        orders.append({
            'order_id': order_counter,
            'user_id': user_id,
            'session_id': session['session_id'],
            'order_date': order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'total_amount': round(order_total, 2),
            'status': status
        })
        order_items.extend(items_in_order)
        order_counter += 1

df_orders = pd.DataFrame(orders)
df_order_items = pd.DataFrame(order_items)


# ----------------- 5. Generate Returns -----------------
print("Generating Returns...")
returns = []
return_counter = 1

reasons = ['Defective', 'Wrong Item', 'No Longer Needed', 'Did Not Like', 'Other']

delivered_orders = df_orders[df_orders['status'] == 'Delivered']

# Map return rate from products category
product_return_rates = {p['product_id']: categories[p['category']]['return_rate'] for p in products}

for _, item in df_order_items.iterrows():
    if item['order_id'] in delivered_orders['order_id'].values:
        ret_rate = product_return_rates[item['product_id']]
        if random.random() < ret_rate:
            order_info = delivered_orders[delivered_orders['order_id'] == item['order_id']].iloc[0]
            order_date = pd.to_datetime(order_info['order_date'])
            # Return happens 1 to 30 days after order
            return_date = order_date + timedelta(days=random.randint(1, 30))
            
            returns.append({
                'return_id': return_counter,
                'order_id': item['order_id'],
                'product_id': item['product_id'],
                'return_date': return_date.strftime('%Y-%m-%d %H:%M:%S'),
                'reason': random.choice(reasons)
            })
            return_counter += 1

df_returns = pd.DataFrame(returns)


# ----------------- Save Remaining CSVs -----------------
print("Saving all datasets to 'data' directory...")
df_sessions.to_csv('data/sessions.csv', index=False)
df_orders.to_csv('data/orders.csv', index=False)
df_order_items.to_csv('data/order_items.csv', index=False)
df_returns.to_csv('data/returns.csv', index=False)

print(f"Data Generation Complete!")
print(f"Users: {len(df_users)}")
print(f"Products: {len(df_products)}")
print(f"Sessions: {len(df_sessions)}")
print(f"Orders: {len(df_orders)}")
print(f"Order Items: {len(df_order_items)}")
print(f"Returns: {len(df_returns)}")

