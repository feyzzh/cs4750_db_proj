# HoosWell
HoosWell is an app for UVA students to track their health metrics. Users can log their sleep, nutrition, and fitness activities to see trends in their health and track progress of created goals.

# Build Project
1. `git clone https://github.com/feyzzh/cs4750_db_proj.git` in terminal
2. Set up and activate a virtual environment
3. In the root folder of the project, install the dependencies of the project by running `pip install -r requirements.txt`
4. In the `/cs4750_db_proj/cavcore` directory, run `py manage.py makemigrations` and `py manage.py migrate`

# Run Project
In the `/cs4750_db_proj/cavcore` directory, run `py manage.py runserver`. Replace `py` with your variable of the Python interpreter. Next, follow the local host link generated in the terminal to view the web app.
