# NYPD Major Felony Incidents

This repo contains two slightly cleaned/transformed versions of the [NYPD 7 Major Felony Incidents data](https://data.cityofnewyork.us/Public-Safety/NYPD-7-Major-Felony-Incidents/hyij-8hr7/data):

- [2006 through 2009](//helloworlddata.github.io/nypd-major-felony-incidents/catalog/nypd-major-felony-incidents-through-2009.csv) (includes incidents from pre-2006 that were filed in later years)
- [2010 through 2015](//helloworlddata.github.io/nypd-major-felony-incidents/catalog/nypd-major-felony-incidents-2010-through-2015.csv)

The main difference is that unnecessary fields have been left out, the `Location 1` field has been split into lat/lng coordinates, and the datetime fields are in proper ISO format. And the header fields have been snake-cased.

You can preview the data format as CSV here: [catalog/samples/2010-sample.csv](catalog/samples/2010-sample.csv)

You can view the fetching/clean up scripts in [wrangle/scripts/](wrangle/scripts/)


The data is fetched from New York City's Socrata data portal: https://data.cityofnewyork.us/Public-Safety/NYPD-7-Major-Felony-Incidents/hyij-8hr7/data



