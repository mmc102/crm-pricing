import psycopg2
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os

# Database connection details
db_config = {
    'host': '0.0.0.0',
'port':5433,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'mysecretpassword'
}

# Connect to PostgreSQL
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Fetch pricing data
cursor.execute("""
    SELECT
        companies.company_name,
        plans_with_pricing.plan_name,
        plans_with_pricing.price,
        plans_with_pricing.billing_cycle
    FROM plans_with_pricing
    JOIN companies ON plans_with_pricing.company_id = companies.company_id
""")
pricing_data = cursor.fetchall()
print(pricing_data)
generation_date = datetime.now().strftime("%Y-%m-%d")


# Close the connection
cursor.close()
conn.close()


# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('pricing_table.html')

# Render the HTML with the data
output = template.render(pricing_data=pricing_data, generation_date=generation_date)

# Save the output to an HTML file
output_directory = '.'
os.makedirs(output_directory, exist_ok=True)
with open(os.path.join(output_directory, 'index.html'), 'w') as f:
    f.write(output)

print("HTML file generated successfully.")

