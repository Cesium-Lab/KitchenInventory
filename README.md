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

# Backend API Requirements
- General
  - Uses pint library for quantities
- Objects
  - Details
    - Expiration (probably most important)
    - Description
    - Vendor
    - Price
  - MassItem
    - Amount driven by mass
    - Default density ($\rho$) conversion is $1\ g/cm^3$
  - VolumeItem
    - Amount driven by volume (e.g. milk)
  - QuantityItem
    - Amount driven by quantity (e.g. eggs)
  - Recipe
    - List of items required and amounts
    - Informs user of missing items, and how much to get
    - Can make fractional amounts of recipes
  - ToolInventory
    - Which kitchen tools I have
    - Details - when I got them (for when to get new ones?)
    - Condition
- Backend
  - Search 
    - Can search by expiration date
    - Can search by item type

# Frontend Requirements