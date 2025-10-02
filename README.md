🏘️ Neighborhood Asset Sharing API
Project Title: Community Resource Sharing API
The Neighborhood Asset Sharing API is a Django REST Framework (DRF) backend designed to facilitate local, community-level resource sharing. It connects neighbors, enabling them to easily lend and borrow household items, tools, books, and appliances, fostering sustainability and collaboration within the community.

This API serves as the robust backend for a potential web or mobile application, handling all data management, user authentication, and lending logic.

🌟 Key Features
The API provides RESTful endpoints for the core functionalities:

User Management: Secure user registration, authentication (planned for Week 4), and profile management.

Item Management: CRUD operations for items, including details like condition, description, and availability status.

Lending/Borrowing System (In Progress): Logic to handle lending requests, approval/denial, and tracking returns.

Availability Calendar (In Progress): System for owners to mark specific blackout dates for their items.

Messaging System (Planned): Basic internal messaging for users to coordinate logistics.

🚀 Getting Started
Follow these steps to set up and run the API locally for development.

1. Prerequisites
You will need the following installed on your system:

Python 3.8+

Git

pip (Python package installer)

2. Local Setup
Clone the repository:

Bash

git clone https://github.com/daniel-aba/Alx_BE_Capstone_Project.git
cd Alx_BE_Capstone_Project
Create and activate the virtual environment:

Bash

python -m venv venv
source venv/Scripts/activate  # On Linux/macOS: source venv/bin/activate
Install dependencies:

Bash

pip install -r requirements.txt
# Note: If you don't have a requirements.txt yet, run:
# pip install django djangorestframework
Run migrations:

Bash

python manage.py makemigrations
python manage.py migrate
Create a superuser (required to access the admin site and create test items):

Bash

python manage.py createsuperuser
Run the server:

Bash

python manage.py runserver
The API will be available at http://127.0.0.1:8000/.

🗺️ API Endpoints
The API is accessible through the browsable interface at http://127.0.0.1:8000/api/.

Endpoint	Method	Description	Status
/api/users/	GET, POST	List all users, Create a new user (Registration)	Complete (Model/Serializer)
/api/users/<pk>/	GET, PUT, DELETE	Retrieve, Update, or Delete a specific user	Complete
/api/items/	GET, POST	List all items, Create a new item	Complete (CRUD)
/api/items/<pk>/	GET, PUT, DELETE	Retrieve, Update, or Delete a specific item	Complete
/api/lending-requests/	GET, POST	List requests, Create a new request	Planned (Week 2)
/api/messages/	GET, POST	List messages, Send a new message	Planned (Week 3)
/api-auth/login/	POST	Token/Auth endpoint for front-end access	Planned (Week 4)

Export to Sheets
📅 Project Timeline & Status
This project is being developed over a 5-week period.

Week	Focus	Status
1	Setup & Core Models	✅ Completed (Users, Items, Basic CRUD)
2	Lending System & Relationships	In Progress
3	Messaging & Availability Logic	To Do
4	Authentication & Security	To Do
5	Deployment & Final Touches	To Do

Export to Sheets
🤝 Contributing
Contributions are welcome! If you find a bug or have a suggestion, please open an issue or submit a pull request.

📄 License
This project is licensed under the [Choose a License, e.g., MIT License] - see the LICENSE.md file for details.

👤 Author
Daniel Njoroge

GitHub: https://github.com/daniel-aba 

www.linkedin.com/in/daniel-njoroge-119092272
