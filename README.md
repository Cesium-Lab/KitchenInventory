# KitchenInventory
Kitchen Inventory Tracker
"Hey, do we have any flour left?" 
"Hmm I gotta track this stuff"
-----
# Planning


## Backend
Two types of databases available. These will both use the same interface, but some will have a ```NotImplementedError()``` based on the backend API
### DB 1: Excel
- Stored in an excel with columns for each attribute
### DB 2: SQL
- Better searching functionality
- Stored in a large table

## Server interaction

### Handshake
Keeps track of state hashing by ip and socket (must go through in order)
 1. C queries S to make a kitchen with a specific username, and "API key"
 2. If key is correct and no kitchen with that username
    1. S responds with some version of "Hello World!" and lists current inventories
 3.  C either makes a new one with a name, or loads old one with empty name
1.  Loop
    1.  S sends current options
    2.  C selects options

### Kitchen Functions
1. List items with food_type ("empty" for all)
2. List recipes with cuisine_type (empty for all)
3. 

-----
# Backend Requirements
- General
  - Uses pint library for quantities
  - Input validation that throws error with relevant message
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
    - Can add by functions
  - Recipe
    - List of items required and amounts
    - Informs user of missing items, and how much to get
    - Can make fractional amounts of recipes
  - KitchenTool
    - Which kitchen tools I have
    - Details - when I got them (for when to get new ones?)
    - Condition
  - RecipeBook
    - Stores recipes in yaml
    - Can add by functions
  <!-- - Kitchen
    - Contains inventory
    - Contains 
    - "Interface" for the kitchen itself
    - Saves inventory
      - Upon deletion
      - Every set interval (specified when the ) -->
- API
  - Databases
    - Inventories - all inventories
    - Recipes - all recipes
  - Kitchen Manager
    - Functions
      - Creates instance of kitchen if no one if connected to the inventory
        - Keeps track of which user hash is connected to which inventory.
        - "Downtime" of 1 minute before user "relinquishes" command of the inventory
        - Can send a notification to the current user with a message, but only every 30 seconds
      - List inventories
      - Open inventory
  - Calendar
    - Basically keeps track of inventory and recipes over time
    - For each calendar date, can have a list of recipes
    - "Parsing" will propogate the recipes to the current day
    - "Projecting" after parsing will project current inventory to a future date
      - Kitchen Manager can use this to predict when to buy groceries
      - Takes into account expiration dates and marks them with specific dates
      - Return list of dates between now and then that food expires
  - Search 
    - Can search by expiration date
    - Can search by item type

# Frontend Requirements