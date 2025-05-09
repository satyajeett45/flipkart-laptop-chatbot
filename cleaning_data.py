import pandas as pd
import re
import numpy as np

# Load CSV
df = pd.read_csv(r'C:\Users\Admin\OneDrive\Desktop\chatBot project\data\laptops.csv')

# Function to parse laptop name and extract details
def parse_laptop_details(name):
    # Initialize default values
    laptop_name = "Unknown"
    processor = "Unknown"
    ram = "Unknown"
    storage = "Unknown"
    os = "Unknown"
    other_specs = []

    # Clean name
    name = name.strip()

    # Extract laptop name (brand and model, before processor details)
    name_parts = re.split(r' - | Intel | AMD | Qualcomm | Copilot', name, 1)
    if len(name_parts) > 0:
        laptop_name = name_parts[0].strip()
        # Simplify name to brand and model (e.g., "DELL 15", "SAMSUNG Galaxy Book4")
        laptop_name = re.sub(r'\s*\(.*?\)', '', laptop_name)  # Remove parenthetical content
        laptop_name = re.sub(r'\s+', ' ', laptop_name).strip()

    # Extract processor
    processor_match = re.search(r'(Intel Core (?:i3|i5|i7|i9|Ultra \d+)|Intel Celeron|Intel Pentium|Intel Atom|Intel N\d+)|AMD Ryzen \d+|Qualcomm Snapdragon', name, re.IGNORECASE)
    if processor_match:
        processor = processor_match.group(0)
        # Extract generation
        gen_match = re.search(r'(\d{1,2}(?:th|st|nd|rd)? Gen|\d{4}[U|H|HS|HX|P])', name, re.IGNORECASE)
        if gen_match:
            processor = f"{processor} {gen_match.group(1)}"

    # Extract RAM
    ram_match = re.search(r'(\d{1,2}\s*GB)\s*(?:RAM|Memory)?', name, re.IGNORECASE)
    if ram_match:
        ram = ram_match.group(1)

    # Extract storage
    storage_match = re.search(r'(\d{1,3}\s*(?:GB|TB)\s*(?:SSD|HDD))', name, re.IGNORECASE)
    if storage_match:
        storage = storage_match.group(1)

    # Extract operating system
    os_match = re.search(r'(Windows \d{1,2}\s*(?:Home|Pro)|DOS|Linux|Chrome OS|macOS)', name, re.IGNORECASE)
    if os_match:
        os = os_match.group(1)

    # Extract other specs (graphics, display, etc.)
    graphics_match = re.search(r'(NVIDIA GeForce [^\s,]+|Intel [^\s,]+ Graphics|AMD Radeon)', name, re.IGNORECASE)
    if graphics_match:
        other_specs.append(graphics_match.group(0))
    
    display_match = re.search(r'(\d{2}(?:\.\d)?\s*(?:inch|cm)\s*Display)', name, re.IGNORECASE)
    if display_match:
        other_specs.append(display_match.group(0))

    # Add thin and light or gaming if mentioned
    if 'Thin and Light' in name:
        other_specs.append('Thin and Light')
    if 'Gaming' in name:
        other_specs.append('Gaming')

    return {
        'Name': laptop_name,
        'Processor': processor,
        'RAM': ram,
        'Storage': storage,
        'Operating_System': os,
        'Other_Spec': other_specs if other_specs else "None"
    }

# Apply parsing to extract details
parsed_data = df['name'].apply(parse_laptop_details)
parsed_df = pd.DataFrame(parsed_data.tolist())

# Combine with original columns
df = pd.concat([parsed_df, df[['price', 'rating', 'url']]], axis=1)

# Clean and standardize data
# Remove ₹ symbol from price and convert to numeric
df['Price'] = df['price'].str.replace('₹', '').str.replace(',', '').astype(float)

# Handle missing ratings
df['Rating'] = df['rating'].replace('N/A', np.nan).astype(float)

# Rename columns for consistency
df = df.rename(columns={
    'url': 'URL',
    'rating': 'Rating'
})

# Remove duplicates based on Name, Price, Processor, RAM, Storage, Operating_System
df = df.drop_duplicates(subset=['Name', 'Price', 'Processor', 'RAM', 'Storage', 'Operating_System'], keep='first')

# Create description column
def create_description(row):
    description_parts = []
    
    # Add Processor
    if row['Processor'] != 'Unknown':
        description_parts.append(row['Processor'])
    
    # Add RAM
    if row['RAM'] != 'Unknown':
        description_parts.append(row['RAM'])
    
    # Add Storage
    if row['Storage'] != 'Unknown':
        description_parts.append(row['Storage'])
    
    # Add Operating System
    if row['Operating_System'] != 'Unknown':
        description_parts.append(row['Operating_System'])
    
    # Add Other Specs
    if row['Other_Spec'] != 'None':
        if isinstance(row['Other_Spec'], list):
            description_parts.extend(row['Other_Spec'])
        else:
            description_parts.append(row['Other_Spec'])
    
    return ", ".join(description_parts) if description_parts else "No description available"

df['Description'] = df.apply(create_description, axis=1)

# Select requested columns
final_columns = ['Name', 'Price', 'Rating', 'Processor', 'RAM', 'Storage', 'Operating_System', 'Other_Spec', 'URL', 'Description']
df = df[final_columns]

# Save the cleaned DataFrame
df.to_csv('laptops_with_description.csv', index=False)
print("Cleaned dataset with description saved to 'laptops_with_description.csv'.")