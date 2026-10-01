# Source Data

The Companies House bulk data file is not committed 
to this repository due to its size (2.6GB).

To reproduce this data product locally:

1. Download the BasicCompanyDataAsOneFile CSV from:
   https://download.companieshouse.gov.uk/en_output.html

2. Place the CSV file in this folder:
   data/raw/

3. Update the filename reference in:
   models/staging/stg_companies_house.sql

The file contains approximately 5.7 million 
UK registered company records and is updated 
monthly by Companies House.
