## Project Overview

Welcome to the UniTrack repository! UniTrack is a simple web application created to aunitrackt you in managing student information, colleges, and courses.

## Prerequisites

Before you begin working on or using this project, ensure you have the following prerequisites installed on your system:

- Python 3.x (recommended: Python 3.9+)
- Node.js 18.x (recommended: Node.js 18.18.0 LTS)

## Getting Started

Follow these steps to set up and run the project on your local machine:

1. **Clone the Repository:**

   ```shell
   git clone https://github.com/mjcarnaje/uni-track.git
   cd uni-track
   ```

2. **Create an environment:**

   ```shell
   python3 -m venv .venv
   ```

3. **Activate the Virtual Environment:**

   - On macOS and Linux:

     ```shell
     source .venv/bin/activate
     ```

   - On Windows:

     ```shell
     .venv\Scripts\activate
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
- `unitrack/`: A Python package containing the Flask application (indicated by the presence of `__init__.py`).
  - `__init__.py`: Initialization file for the Flask application package.
  - `static/`: Directory for static assets like CSS and JavaScript files.
  - `templates/`: Directory for HTML templates used in the project.
  - `configs/`: Directory for configuration files.
  - `db/`: Directory for database files.
  - `routes/`: Directory for blueprint files.
  - `utils/`: Directory for utility files.
  - `models/`: Directory for database model files.
