import sqlite3

# Create a SQLite database
conn = sqlite3.connect('partners.db')
c = conn.cursor()

# Create a table to store partner information
c.execute('''
		CREATE TABLE IF NOT EXISTS partners (
				id INTEGER PRIMARY KEY,
				name TEXT,
				organization_type TEXT,
				resources_available TEXT,
				contact_name TEXT,
				contact_email TEXT,
				contact_phone TEXT
		)
''')

# Function to add a new partner
def add_partner():
		name = input("Enter partner name: ")
		organization_type = input("Enter organization type: ")
		resources_available = input("Enter resources available: ")
		contact_name = input("Enter contact name: ")
		contact_email = input("Enter contact email: ")
		contact_phone = input("Enter contact phone: ")

		c.execute('''
				INSERT INTO partners (name, organization_type, resources_available, contact_name, contact_email, contact_phone)
				VALUES (?, ?, ?, ?, ?, ?)
		''', (name, organization_type, resources_available, contact_name, contact_email, contact_phone))

		conn.commit()
		print("Partner added successfully!")

# Function to search and filter partners
def search_partners():
		keyword = input("Enter a keyword to search: ")
		c.execute('''
				SELECT * FROM partners
				WHERE name LIKE ? OR organization_type LIKE ? OR resources_available LIKE ? OR contact_name LIKE ?
		''', ('%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%'))

		partners = c.fetchall()
		if partners:
				print("\nSearch Results:")
				for partner in partners:
						print(partner)
		else:
				print("No matching partners found.")

# Main menu
while True:
		print("\n1. Add Partner")
		print("2. Search Partners")
		print("3. Exit")

		choice = input("Enter your choice (1/2/3): ")

		if choice == '1':
				add_partner()
		elif choice == '2':
				search_partners()
		elif choice == '3':
				break
		else:
				print("Invalid choice. Please enter 1, 2, or 3.")

# Close the database connection
conn.close()