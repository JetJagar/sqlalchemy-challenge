# Climate Data Analysis and API

## Overview
This project analyzes and explores climate data using Python, SQLAlchemy, Pandas, and Matplotlib. Additionally, it provides a Flask API to serve climate-related data.

## Part 1: Analyze and Explore the Climate Data

### Requirements
- Python
- SQLAlchemy
- Pandas
- Matplotlib
- SQLite database (`hawaii.sqlite`)

### Steps
1. **Database Connection**
   - Use `SQLAlchemy create_engine()` to connect to the SQLite database.
   - Use `SQLAlchemy automap_base()` to reflect tables into classes (`station` and `measurement`).
   - Create a SQLAlchemy session.
   - Close the session at the end of the notebook.

2. **Precipitation Analysis**
   - Retrieve the most recent date from the dataset.
   - Query precipitation data for the last 12 months.
   - Load the data into a Pandas DataFrame, set column names, sort by date.
   - Plot precipitation results.
   - Print summary statistics of precipitation data.

3. **Station Analysis**
   - Query the total number of stations.
   - Identify the most active stations by counting observations.
   - Retrieve the lowest, highest, and average temperatures for the most active station.
   - Query temperature observations for the last 12 months for the most active station.
   - Plot results as a histogram with 12 bins.
   - Close the session.

## Part 2: Design Your Climate App

A Flask API is created based on the queries developed in Part 1.

### API Routes

- **/**
  - Lists all available API routes.

- **/api/v1.0/precipitation**
  - Returns the last 12 months of precipitation data as a JSON dictionary with date as the key and precipitation as the value.

- **/api/v1.0/stations**
  - Returns a JSON list of all stations.

- **/api/v1.0/tobs**
  - Returns the last 12 months of temperature observations for the most active station.

- **/api/v1.0/<start> and /api/v1.0/<start>/<end>**
  - Returns a JSON list containing the minimum, average, and maximum temperatures for the specified date range.

## Installation
1. Clone the repository:
   ```bash
   git clone <repo_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd climate-analysis
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the Jupyter Notebook to analyze the data.
7. Start the Flask API:
   ```bash
   python app.py
   ```

## Usage
- Open `climate_starter.ipynb` in Jupyter Notebook to perform climate analysis.
- Access the Flask API via `http://127.0.0.1:5000/` in your browser or a tool like Postman.

## License
This project is licensed under the MIT License.


