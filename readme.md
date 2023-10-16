## Project Overview

Welcome to the UniTrack repository! UniTrack is a simple web application created to aunitrackt you in managing student information, colleges, and courses. This is a flask application that uses MySQL as its database. It also uses TailwindCSS for styling.

## Prerequisites

Before you begin working on this project, ensure you have the following prerequisites installed on your system:

- Python 3.x
- Node.js 18.x
- MySQL 8.x
- Pipenv

## Getting Started

Follow these steps to set up and run the project on your local machine:

1. **Clone the Repository:**

   ```shell
   git clone https://github.com/mjcarnaje/uni-track.git
   cd uni-track
   ```

2. **Install Dependencies:**

   ```shell
   npm install
   ```

   ```shell
   pipenv install
   ```

   Note: If you don't have pipenv installed, you can install it using `pip install pipenv`. And every time you want to run the project, you can use `pipenv run python main.py`. If you want to install packages, you can use `pipenv install <package-name>`.

3. **Activate the Virtual Environment:**

   ```shell
   pipenv shell
   ```

4. **Create a Database:**

   - Create a database named `unitrack` in MySQL.

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
- `unitrack/`: A Python package containing the Flask application (indicated by the presence of `__init__.py`).
  - `__init__.py`: Initialization file for the Flask application package.
  - `static/`: Directory for static assets like CSS and JavaScript files.
  - `templates/`: Directory for HTML templates used in the project.
  - `configs/`: Directory for configuration files.
  - `db/`: Directory for database files.
  - `routes/`: Directory for blueprint files.
  - `utils/`: Directory for utility files.
  - `models/`: Directory for database model files.
