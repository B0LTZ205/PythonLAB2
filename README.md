# Student Management System

## Project Overview
This Student Management System is a web application built to manage student records in an educational institution. The system provides a comprehensive interface for creating, reading, updating, and deleting student information (CRUD operations). It includes features such as:

- Student record management with details like student ID, name, email, program, and enrollment date
- Profile image upload and management for students
- User authentication and role-based access control (user, admin, superadmin)
- Admin dashboard for user management
- Responsive data tables with search, pagination, and sorting capabilities

The application follows a structured MVC (Model-View-Controller) architecture to separate concerns and maintain clean, organized code.

## Technologies Used

### Backend
- **Python**: Core programming language
- **Flask**: Web framework for building the application
- **Blueprint**: Flask component for organizing the application into modules
- **MongoDB**: NoSQL database for storing student and user data
- **PyMongo**: MongoDB driver for Python
- **GridFS**: MongoDB's solution for storing and retrieving large files (student images)

### Frontend
- **HTML/CSS**: Structure and styling of web pages
- **Bootstrap 5**: Frontend framework for responsive design
- **JavaScript**: Client-side scripting
- **jQuery**: JavaScript library for DOM manipulation
- **DataTables**: jQuery plugin for enhanced table functionality

### Security & Authentication
- **Flask Session**: For managing user sessions
- **Role-based Access Control**: Restricting access based on user roles (user, admin, superadmin)
- **Form Validation**: Both client-side and server-side validation

### Development Tools
- **Flask Debug Mode**: For development environment
- **Test Data Generator**: Script to populate the database with sample student data

## Project Structure
The application follows a modular structure using Flask Blueprints:
- **Controllers**: Handle request processing and business logic
  - `create_student_controller.py`: Manages student creation
  - `read_student_controller.py`: Handles student data retrieval
  - `update_student_controller.py`: Manages student data updates
  - `delete_student_controller.py`: Handles student deletion
  - `auth_controller.py`: Manages authentication
  - `admin_controller.py`: Handles admin functionality
- **Models**: Interact with the database
  - `students_model.py`: Student data operations
- **Templates**: HTML views
  - Main templates for student management
  - Admin templates for user management
- **Static**: CSS, JavaScript, and image files

## Features
- **Student Management**: Complete CRUD operations for student records
- **Image Management**: Upload and display student profile images
- **User Authentication**: Secure login system
- **Role-based Access**: Different permissions for different user roles
- **Responsive Design**: Works on various screen sizes
- **Data Tables**: Advanced features for data display and manipulation
- **Flash Messages**: User feedback for actions