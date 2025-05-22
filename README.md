# KitchenInventory
Kitchen Inventory Tracker

# Planning


## Backend
Two types of backends available. These will both use the same interface, but some will have a ```NotImplementedError()``` based on the backend API
### Step 1: Excel
- Stored in an excel with columns for each attribute
### Step 2: SQL
- Better searching functionality
- Stored in a large table

# Backend Requirements
- General
  - Uses pint library for quantities
- Objects
  - Details
    - Expiration (probably most important)
    - Description
    - Vendor
    - Price
  - Item
    - Amount driven by mass or volume
    - "Canonical" amount is mass, with density as conversion
    - Default density ($\rho$) conversion is $1\ g/cm^3$
  - CountableItem
    - Amount driven by quantity (e.g. eggs)
  - Inventory
    - Stores items in database or table
    - Can add by strings
  - Recipe
    - List of items required and amounts
    - Informs user of missing items, and how much to get
    - Can make fractional amounts of recipes
  - ToolInventory
    - Which kitchen tools I have
    - Details - when I got them (for when to get new ones?)
    - Condition
- API
  - Search 
    - Can search by expiration date
    - Can search by item type

# Frontend Requirements