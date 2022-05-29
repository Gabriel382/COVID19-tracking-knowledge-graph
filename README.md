# COVID19-tracking-knowledge-graph

## Problem Statement

The COVID-19 (SARS-CoV-2) spread around the globe could have been halted if we had had a better understanding of the situation and applied more restrictive measures for travel adapted to each country. This is due to a lack of efficient tools to visualize, analyze and control the virus dissemination. In the context of virus proliferation, analyzing flight connections between countries and COVID-19 data seems helpful to understand spatial and temporal information about the virus and its possible spread. To manage these complex, massive, and heterogeneous data, we propose a methodology based on knowledge graphs models by using Python and Neo4j.

## Pre-reqs

All the code is in the code folder, next to the requirements. I advise creating an environment with [venv](https://docs.python.org/3/library/venv.html) and installing the requirements with:

> $ pip install -r requirements.txt

## Running

You can start experimenting directly with Neo4j and data from January by loading the dump file in the dump folder.

You can also run *mapcode.py* to create your graph from scratch, followed by *flightcode.py* to push the flight connection data from *data/OpenSky* to Neo4j. You can download this data from [here](https://zenodo.org/record/6078268#.YpNV5DnP30p).