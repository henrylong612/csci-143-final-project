# Twitter Clone
This repository contains a script for a local interactive twitter clone according to the specifictions of [project_05](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_05).


The `twitter_clone.db` file contains the database of users and messages for the website. The `db_create.py` file creates the original database, and the `db_access.py` file accesses the database of users and messages. The `project.py` file contains the scrpit for the actual website. The website can be accessed locally using the ip address http://127.0.0.1:5000/. The `templates/` folder contains the templates for each of the webpages, which all extend the `base.html` file. The `static/css/` folder contains the css for the website, and the `static/img/` folder contains the image for the website's logo. The `markdown_compiler2.py` contains a markdown compiler that is used to make the message box compatible with markdown syntax.
