# Django Simple Blog

![image](https://raw.githubusercontent.com/mohamedayman28/simple_blog/master/github_simple_blog.jpg)

The blog contains all the writing essentials from a WYSIWYG editor to a full authentication system, along with RESTFul API.

## Setting up locally

To set the site up locally, you'll need to have Python 3.6 or higher version installed on your local machine. Once that is done and ready, proceed to download the repository with the next steps.

### 1. Make the directory for development:
```bash
mkdir simple_blog
cd simple_blog
```

### 2. Create virtualenv:

**Note:** You may want to change the Python version, I'm also using Linux Ubuntu-based OS, so depending on your OS you may use different commands for creating a python virtual environment.

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
git clone https://github.com/mohamedayman28/django_simple_blog
```

### 4. After, successfully, activating the virtualenv and download the repository, install required packages:
```bash
cd django_simple_blog
pip install -r requirements.txt
```

### 5 Migrate
```bash
python manage.py makemigrations
python manage.py migrate
```
If the migrations doesn't apply to all apps, you may need to migrate each app individually
```bash
python manage.py makemigrations posts
python manage.py migrate posts
```

### 6. Create Super User
Only authors allowed to write posts, for that, you first need to access the admin panel and create an author, thus need to be a super-user:
```bash
python manage.py createsuperuser
```

### 7. Run the app:
```bash
python manage.py runserver
```

## Handle FileBrowser error
You may encounter this log error while using filebrowser
```
Error finding Upload-Folder (site.storage.location + site.directory). Maybe it does not exist?
```
If that the case, create folder in the app root directory named as the name set in the settings.MEDIA_ROOT

## Using the API
It's advisable to have an overview of how Django REST handles authentication before using the blog API.
* Overview of how default [DRF authentication](https://www.django-rest-framework.org/api-guide/authentication/) works.
* I use the dj-rest-auth for API authentication, read more about it [here](https://dj-rest-auth.readthedocs.io/en/latest/index.html).
