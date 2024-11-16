# bugsocial

## How to run the project:
1. Clone the repository
2. cd `bugsocial`
3. Install necessary dependencies via `python -m pip install -r requirements.txt`
4. Configure the required environment variables:
    - Add a new `.env` file at the root of the repository.
    - Declare the following environment variables:
        ```bash
        GOOGLE_OAUTH2_KEY=YOUR GOOGLE auth key
        GOOGLE_OAUTH2_SECRET=Your secret key
    Get these credentials from [Google's developer console](https://console.developers.google.com/apis/credentials).
5. To run the application, you'll need to update your hosts file to use `mysite.com` instead of the default localhost. On Mac, update your `/etc/hosts` file to point `127.0.0.1` to `mysite.com` like so:
    ```bash
    127.0.0.1	mysite.com
6. Finally, run the application:
    ```bash
    python manage.py runserver_plus --cert-file cert.crt