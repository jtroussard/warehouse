# Installation Guide

This application is built for and tested on Ubuntu Linux. We make no claims about how it may or may not run in other environments.

### Dependencies: python3, pip3, git, postgresql

To retrieve the source code for the application run

```git clone https://github.com/smiller657/warehouse.git```

To install the required python packages run

```sudo pip3 install flask```

```sudo pip3 install psycopg2```

```sudo pip3 install tabulate```

At this point all required software should be installed. To initialize the database schema source the file lib/warehouse.sql in postgres.
Now everything the application needs to run should be set up. To run the application use the command

```sudo python3 server.py```

After running this command the app should be up and accessible.
