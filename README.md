# Django Simple Blog

![image](https://raw.githubusercontent.com/mohamedayman28/simple_blog/master/github_simple_blog.jpg)

Blog contains all the essentials from a WYSIWYG editor to a full authentication system, along with RESTFul API.

## Setting up locally

To set the site up locally, you'll need to have Python 3.6 or higher version installed on your local system. Once that is done and ready, proceed to download the repository with using the next steps.

### 1. Make the directory for development:
```bash
mkdir simple_blog
cd simple_blog
```

### 2. Create virtualenv:

**Note:** You may want to change the Python version.

```bash
sudo apt-get install python3-pip
sudo apt-get install python3.6-venv
python3.6 -m venv blog_env
```

### 3. Activate virtualenv:
```bash
source blog_env/bin/activate
```

### 4. Download the repository:
```bash
git init
git https://github.com/mohamedayman28/django_simple_blog
```

### 4. After, successfully, activate the virtualenv and download the repository, install required packages:
```bash
cd django_simple_blog
pip install -r requirements.txt
```

### 5. Now run the app with:
```bash
python manage.py runserver
```

To use the API provided, you may want to use a client app like [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/), and read through the next usage  pages:
* Overview of how default [DRF authentication](https://www.django-rest-framework.org/api-guide/authentication/) works.
* I use the dj-rest-auth for API authentication, read more about it [here](https://dj-rest-auth.readthedocs.io/en/latest/index.html).
