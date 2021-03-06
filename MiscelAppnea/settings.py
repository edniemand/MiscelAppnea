"""
Django settings for MiscelAppnea project.

Generated by 'django-admin startproject' using Django 2.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MISCELAPPNEA
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR,'static')

# USUARIOS
TEMPLATE_USUARIOS_DIR = os.path.join(BASE_DIR,'usuarios_app/templates/usuarios_app')

# NOMINAS
TEMPLATE_NOMINAS_DIR = os.path.join(BASE_DIR,'nominas_app/templates/nominas_app')

# COMEDOR
TEMPLATE_COMEDOR_DIR = os.path.join(BASE_DIR,'comedor_app/templates/comedor_app')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3e7eeg+tnb7oaid=4-ymyqfk33*^2o0tt-4j@02+5^f!r#ih3+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios_app',
    'nominas_app',
    'comedor_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MiscelAppnea.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,TEMPLATE_USUARIOS_DIR,TEMPLATE_NOMINAS_DIR,TEMPLATE_COMEDOR_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MiscelAppnea.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # PARA SU FICIONAMIENTO EN WINDOWS
    'comedorTrabis': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': 'SERVERNOMINA\COMPAC',
        'USER': 'sa',
        'PASSWORD': 'compac',
        'NAME': 'ComedorTrabis',
        'OPTIONS': {
            #'host_is_server': True,
            'driver': "ODBC Driver 13 for SQL Server"
            },
    },
    'tempoControl': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': 'SERVERNOMINA\COMPAC',
        'USER': 'sa',
        'PASSWORD': 'compac',
        'NAME': 'dbTempoControl',
        'OPTIONS': {
            #'host_is_server': True,
            'driver': "ODBC Driver 13 for SQL Server"
            },
    },
    'nominasPrestadora': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': 'SERVERNOMINA\COMPAC',
        'USER': 'sa',
        'PASSWORD': 'compac',
        'NAME': 'ctPRESTADORA_DE_S',
        'OPTIONS': {
            #'host_is_server': True,
            'driver': "ODBC Driver 13 for SQL Server"
            },
    },
    'nominasPresol': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': 'SERVERNOMINA\COMPAC',
        'USER': 'sa',
        'PASSWORD': 'compac',
        'NAME': 'ctPRESOL_HERMOSIL',
        'OPTIONS': {
            #'host_is_server': True,
            'driver': "ODBC Driver 13 for SQL Server"
            },
    },
    'nominasInnova': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': 'SERVERNOMINA\COMPAC',
        'USER': 'sa',
        'PASSWORD': 'compac',
        'NAME': 'ctINNOVACIONES_CO',
        'OPTIONS': {
            #'host_is_server': True,
            'driver': "ODBC Driver 13 for SQL Server"
            },
    },
    'nominasSERA': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': 'SERVERNOMINA\COMPAC',
        'USER': 'sa',
        'PASSWORD': 'compac',
        'NAME': 'ctSERVICIOS_RELAC',
        'OPTIONS': {
            #'host_is_server': True,
            'driver': "ODBC Driver 13 for SQL Server"
            },
    },
    'nominasComplem': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': 'SERVERNOMINA\COMPAC',
        'USER': 'sa',
        'PASSWORD': 'compac',
        'NAME': 'ctCOMPLEMENTO_DE',
        'OPTIONS': {
            #'host_is_server': True,
            'driver': "ODBC Driver 13 for SQL Server"
            },
    },

    # # PARA SU FUNCIONAMIENTO EN MACOSX
    # 'comedorTrabis': {
    #     'ENGINE': 'sql_server.pyodbc',
    #     'HOST': '192.168.0.17',
    #     'INSTANCE': 'COMPAC',
    #     'PORT': '9612',
    #     'NAME': 'ComedorTrabis',
    #     'USER': 'sa',
    #     'PASSWORD': 'compac',
    #     'AUTOCOMMIT': True,
    #     'OPTIONS': {
    #         'driver': 'FreeTDS',
    #         'unicode_results': True,
    #         'host_is_server': True,
    #         'extra_params': 'tds_version=7.4;',
    #     },
    # },
    # 'nominasPrestadora': {
    #     'ENGINE': 'sql_server.pyodbc',
    #     'HOST': '192.168.0.17',
    #     'INSTANCE': 'COMPAC',
    #     'PORT': '9612',
    #     'NAME': 'ctPRESTADORA_DE_S',
    #     'USER': 'sa',
    #     'PASSWORD': 'compac',
    #     'AUTOCOMMIT': True,
    #     'OPTIONS': {
    #         'driver': 'FreeTDS',
    #         'unicode_results': True,
    #         'host_is_server': True,
    #         'extra_params': 'tds_version=7.4;',
    #     },
    # },
    # 'nominasPresol': {
    #     'ENGINE': 'sql_server.pyodbc',
    #     'HOST': '192.168.0.17',
    #     'INSTANCE': 'COMPAC',
    #     'PORT': '9612',
    #     'NAME': 'ctPRESOL_HERMOSIL',
    #     'USER': 'sa',
    #     'PASSWORD': 'compac',
    #     'AUTOCOMMIT': True,
    #     'OPTIONS': {
    #         'driver': 'FreeTDS',
    #         'unicode_results': True,
    #         'host_is_server': True,
    #         'extra_params': 'tds_version=7.4;',
    #     },
    # },
    # 'nominasInnova': {
    #     'ENGINE': 'sql_server.pyodbc',
    #     'HOST': '192.168.0.17',
    #     'INSTANCE': 'COMPAC',
    #     'PORT': '9612',
    #     'NAME': 'ctINNOVACIONES_CO',
    #     'USER': 'sa',
    #     'PASSWORD': 'compac',
    #     'AUTOCOMMIT': True,
    #     'OPTIONS': {
    #     'driver': 'FreeTDS',
    #         'unicode_results': True,
    #         'host_is_server': True,
    #         'extra_params': 'tds_version=7.4;',
    #     },
    # },
    # 'nominasSERA': {
    #     'ENGINE': 'sql_server.pyodbc',
    #     'HOST': '192.168.0.17',
    #     'INSTANCE': 'COMPAC',
    #     'PORT': '9612',
    #     'NAME': 'ctSERVICIOS_RELAC',
    #     'USER': 'sa',
    #     'PASSWORD': 'compac',
    #     'AUTOCOMMIT': True,
    #     'OPTIONS': {
    #         'driver': 'FreeTDS',
    #         'unicode_results': True,
    #         'host_is_server': True,
    #         'extra_params': 'tds_version=7.4;',
    #     },
    # },
    # 'nominasComplem': {
    #     'ENGINE': 'sql_server.pyodbc',
    #     'HOST': '192.168.0.17',
    #     'INSTANCE': 'COMPAC',
    #     'PORT': '9612',
    #     'NAME': 'ctCOMPLEMENTO_DE',
    #     'USER': 'sa',
    #     'PASSWORD': 'compac',
    #     'AUTOCOMMIT': True,
    #     'OPTIONS': {
    #         'driver': 'FreeTDS',
    #         'unicode_results': True,
    #         'host_is_server': True,
    #         'extra_params': 'tds_version=7.4;',
    #     },
    # },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR]

LOGIN_REDIRECT_URL = '/'
