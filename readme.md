# Alumni ID Maker

A Django web application for creating and managing alumni ID cards.

## Features

- Upload and manage ID card background templates
- Register alumni with their personal information and photos
- Generate professional ID cards with customizable backgrounds
- Print-ready ID card generation
- List and manage all alumni records

## Prerequisites

- Python 3.8 or higher
- Django 5.0.2
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd id_maker
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

1. First, upload an ID background template through the "Upload Background" page
2. Register alumni information including their photo
3. View and print ID cards from the alumni list

## Project Structure

- `alumni_id/` - Main application directory
  - `models.py` - Database models for ID backgrounds and alumni profiles
  - `views.py` - View functions for handling requests
  - `forms.py` - Forms for data input
  - `urls.py` - URL routing
- `templates/` - HTML templates
- `media/` - Uploaded files (photos and backgrounds)
- `static/` - Static files (CSS, JavaScript, etc.)

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
