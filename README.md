# web_scraping_without_selenium
This project provides a solution to scrape and gather property prices data from the real estate website "Makaan". The collected data is stored in both a CSV file and an SQLite database, making it easily accessible and ready to be analyzed.
## CSV File
The makaan_locality_prices.csv file contains the following columns:
* city: The name of the city.
* locality: The name of the locality.
* price: The average property price in the locality (in Rupees).

## SQLite Database
The makaan_locality_prices.db database contains a single table makaan_locality_prices with the same data as the CSV file. The table has the following columns:
* city: The name of the city.
* locality: The name of the locality.
* price: The average property price in the locality (in Rupees).
## Usage
To use the CSV file, simply open the file in a text editor or spreadsheet program and view the data. To use the SQLite database, you can use a SQLite client program or run SQL queries in a programming language such as Python.
## Contributions
If you would like to contribute to this project, please fork the repository and create a pull request with your changes. The project maintainers will review your changes and merge them if appropriate.
