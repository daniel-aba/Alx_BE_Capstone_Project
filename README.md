🏘️ Neighborhood Asset Sharing API
Project Title: Neighborhood Asset Sharing API

The Neighborhood Asset Sharing API is a Django REST Framework (DRF) backend designed to facilitate local, community-level resource sharing. It connects neighbors, enabling them to easily lend and borrow household items, tools, books, and appliances, fostering sustainability and collaboration within the community.
This API serves as the robust backend for a potential web or mobile application, handling all data management, secure user authentication, and lending logic.


🌟 Key Features
The API provides RESTful endpoints for the core functionalities:
•	User Management & Security (Complete): Secure registration, token-based authentication, and dedicated endpoints (/api/me/) for profile management, including profile picture uploads.
•	Item Management (Complete): CRUD operations for items, including detailed fields like deposit and insurance_required. Supports multiple item images and category tagging for better discoverability.
•	Lending/Borrowing System (Complete): Logic to handle lending requests, approval/denial, and tracking returns using custom permissions.
•	Availability Calendar (Complete): System for owners to mark specific blackout dates for their items and check future availability.
•	Messaging System (Complete): Internal messaging system for users to coordinate logistics and receive automated notifications.


🚀 Getting Started
Follow these steps to set up and run the API locally for development.
Prerequisites
You will need the following installed on your system, plus the Pillow library for image handling:
•	Python 3.8+
•	Git
•	pip (Python package installer)


Local Setup
Clone the repository:
git clone [https://github.com/daniel-aba/Alx_BE_Capstone_Project.git](https://github.com/daniel-aba/Alx_BE_Capstone_Project.git)
cd Alx_BE_Capstone_Project


Create and activate the virtual environment:
python -m venv venv
source venv/Scripts/activate # On Linux/macOS: source venv/bin/activate
# On Windows: venv\Scripts\activate


Install dependencies (including Pillow):
pip install -r requirements.txt


Note: If you don't have a requirements.txt yet, run:
pip install django djangorestframework djangosimplejwt Pillow


Run migrations:
python manage.py makemigrations
python manage.py migrate


Create a superuser (required to access the admin site and create test items):
python manage.py createsuperuser


Run the server:
python manage.py runserver


The API will be available at http://127.0.0.1:8000/.


🗺️ API Endpoints
The API is accessible through the browsable interface at http://127.0.0.1:8000/api/.
Endpoint	Method	Description	Status
/api/users/	POST	Create a new user (Registration).	Complete
/api/me/	GET, PUT, PATCH	Retrieve or update the authenticated user's profile.	Complete
/api/auth/token/login/	POST	Log in a user and retrieve an authentication token.	Complete
/api/auth/token/logout/	POST	Log out a user by invalidating the token.	Complete
/api/items/	GET, POST	List all items (catalog), Create a new item.	Complete
/api/items/<int:pk>/	GET, PUT, DELETE	Retrieve, Update, or Delete a specific item.	Complete
/api/lending-requests/	GET, POST	List requests, Create a new request.	Complete
/api/messages/	GET, POST	List messages, Send a new message.	Complete


📅 Project Timeline & Status
This project is being developed over a 5-week period.
Week	Focus	Status
1	Setup & Core Models	✅ Completed (Users, Items, Basic CRUD)
2	Authentication & Advanced Models	✅ Completed (Auth, Profile Pic, Item Images/Category)
3	Lending System & Relationships	✅ Completed (Request/Approval Workflow, Custom Permissions)
4	Messaging & Availability Logic	✅ Completed (Internal Messaging, Availability Tracking)
5	Deployment & Final Touches	✅ Completed (Final testing and optimization)


🤝 Contributing
Contributions are welcome! If you find a bug or have a suggestion, please open an issue or submit a pull request.

👤 Author
Daniel Njoroge
GitHub: https://github.com/daniel-aba LinkedIn: www.linkedin.com/in/daniel-njoroge-119092272
 f08842275eaca2f45e80dcc86d295c3534194858
