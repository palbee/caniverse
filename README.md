
# Read Me

I'm hoping that people have had a chance to look at the first pass of caniverse. Please let me know what's good, bad, missing, or unneeded.

Please take a look at the issues and let me know if you want to tackle one.
# caniverse
Not a shoe...


This is part of the CANiverse project.




## Super Quick Start

### Depends
 * Python 3

### Install

 1. Clone the repository.
 2. Create and activate a Python3 virtual environment.
 3. Change to the directory you cloned into.
 4. Install the the requirements using:
       ```bash
       pip install -r requirements.txt
       ```
 5. Change to the caniverse directory.
 6. Setup the database.
       ```bash
       python3 ./manage.py migrate
       ```

 7. Create an administrative user

       ```bash
       python3 ./manage.py createsuperuser
       ```
 8. Run the development server.
       ```bash
       python3 ./manage.py runserver
       ```
 9. Navigate to http://127.0.0.1:8000/admin
10. Submit issues to https://github.com/palbee/caniverse/issues

## References


https://github.com/dschanoeh/Kayak