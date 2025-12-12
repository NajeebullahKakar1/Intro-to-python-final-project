**The app was written by all members of the group. For the purpose of testing we had to download and reupload everything. Check the commit history for proof.**

app

This is the main entry point of the whole system. It contains the create_app() function, which creates the Flask application, loads configuration settings, initializes the database, and registers all the route blueprints. Every time the app runs, this file is responsible for assembling all the parts of the project and connecting them together. If you ever add new route files or features, this is the place where you register them.

config.py

This file stores configuration settings for the project, such as the database file name and secret key. By keeping all settings here, it becomes easier to maintain or modify the app (for example, switching to another database or enabling debug mode). Whenever the application starts, it loads values from this file so everything is centralized and easy to update.

database.py

This file handles all database communication. It includes the init_db() function, which creates the required tables (users, books, borrow) if they do not already exist. It also contains the query() function, which is used everywhere in the project to read or write data in the SQLite database. Keeping database logic here makes it easier to change or extend the data layer later.

 Routes Folder

The routes/ folder contains all blueprint route files. Each file represents a different set of functionalities, keeping the project clean and organized.

routes/auth_routes.py

Handles everything related to user authentication: registration, login, logout, and session management. It validates user credentials, assigns roles (normal or admin), and ensures users are redirected to the correct pages after signing in. Maintaining this file ensures your login system stays secure and consistent.

routes/book_routes.py

Contains the routes that manage books, such as adding new books, editing them (if implemented), and listing them on the dashboard. It also contains the search logic, allowing users to find books by title, author, language, or year. All book-related forms and actions connect to this file, making it easy to maintain book functionalities in one place.

routes/borrow_routes.py

Handles borrowing and returning books. When a user clicks “Borrow” or “Return,” this file updates the book’s availability and logs the action in the borrow table. Keeping these actions separate from book routes makes the borrow/return logic easier to maintain and expand (e.g., due dates or limits).

routes/admin_routes.py

Contains admin-only functionality, such as viewing all users, updating user roles, and deleting users. It uses the admin_required decorator to ensure only admin accounts can access these pages. This file is where you would add any new admin features in the future, like book removal or system logs.

routes/api_routes.py

Provides API endpoints for external applications or for JavaScript-based features in the future. These routes return JSON data rather than HTML, making them useful for integrations or dynamic interfaces. If you want to build a mobile app or a React frontend later, this file is ready to handle those requests.

 Templates Folder (HTML files)

The templates folder contains all frontend HTML pages used by the app. They are rendered by route functions and use shared CSS styling.

login.html

The login page where users enter their username and password. It sends form data to /login and displays error messages when needed. Keeping it simple makes it easy to restyle or customize the layout later.

register.html

The user registration page. It collects the username and password and sends them to /register. This is where new normal users or admins (James1/2) get created. Any future permission settings or form validation changes would be updated here.

dashboard.html

The main page users see after logging in. It lists books, contains the search bar, and shows borrow/return buttons. If the logged in user is an admin, the page also displays admin-only buttons like “Add Book” or “Manage Users.” This is the center of the application’s user interface.

history.html

Displays a user’s borrow history, showing which books they have borrowed or returned. It gets entries from the database and renders them in a readable table format. You can expand this file to show more details, like dates or statuses.

manage_users.html

An admin-only page showing all registered users. Admins can update roles or delete accounts. This file makes it easy to maintain user-related controls and reorganize how user lists are displayed.

static/styles.css

Contains all the styling used across the project: layout, buttons, forms, colors, and tables. By keeping all styles in one CSS file, you can quickly redesign the whole project without touching the backend. If you add new HTML templates later, just include this CSS file to keep the design consistent.
