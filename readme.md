## Project Overview

Welcome to the Web-based Simple Student Information System (SSIS) repository! SSIS is a straightforward web application designed to help you manage student information, colleges, and courses.

## Prerequisites

Before you begin working on or using this project, ensure you have the following prerequisites installed on your system:

- Python 3.x (recommended: Python 3.9+)
- Node.js 18.x (recommended: Node.js 18.18.0 LTS)

## Getting Started

Follow these steps to set up and run the project on your local machine:

1. **Clone the Repository:**

   ```shell
   git clone https://github.com/mjcarnaje/web-ssis.git
   cd web-ssis
   ```

2. **Create an environment:**

   ```shell
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - On macOS and Linux:

     ```shell
     source venv/bin/activate
     ```

   - On Windows:

     ```shell
     venv\Scripts\activate
     ```

4. **Install Dependencies:**

   ```shell
   pip install -r requirements.txt
   ```

   ```shell
   npm install
   ```

5. **Run the Flask Application & TailwindCSS Compiler**:

   ```shell
   python main.py
   ```

   ```shell
   npm run compile:css
   ```

   The application will be available at http://localhost:5000/ by default.

## Folder Structure

- `main.py`: The main Python file of the project.
- `ssis/`: A Python package containing the Flask application (indicated by the presence of `__init__.py`).
  - `__init__.py`: Initialization file for the Flask application package.
  - `static/`: Directory for static assets like CSS and JavaScript files.
  - `templates/`: Directory for HTML templates used in the project.
  - `auth.py`: Module for authentication-related functionality.
  - `models.py`: Module for defining data models.
  - `views.py`: Module for defining views and routes for the Flask application.
