# # from pathlib import Path
# # from datetime import timedelta

# # BASE_DIR = Path(__file__).resolve().parent.parent

# # # إعدادات أساسية بسيطة
# # SECRET_KEY = 'simple-key-for-testing'  # مفتاح بسيط للتجربة
# # DEBUG = True  # مفعل للتجربة
# # ALLOWED_HOSTS = ['*']  # السماح لجميع المضيفين

# # # التطبيقات المثبتة (مع إضافة staticfiles)
# # INSTALLED_APPS = [
# #     'django.contrib.admin',
# #     'django.contrib.auth',
# #     'django.contrib.contenttypes',
# #     'django.contrib.sessions',
# #     'django.contrib.messages',
# #     'django.contrib.staticfiles',  # أضفنا ده
# #     'App',
# #     'rest_framework',
# #     'rest_framework_simplejwt',
# #     'corsheaders',
# # ]

# # # الـ Middleware
# # MIDDLEWARE = [
# #     'corsheaders.middleware.CorsMiddleware',
# #     'django.middleware.security.SecurityMiddleware',
# #     'django.contrib.sessions.middleware.SessionMiddleware',
# #     'django.middleware.common.CommonMiddleware',
# #     'django.middleware.csrf.CsrfViewMiddleware',
# #     'django.contrib.auth.middleware.AuthenticationMiddleware',
# #     'django.contrib.messages.middleware.MessageMiddleware',
# #     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# # ]

# # ROOT_URLCONF = 'Nursery_project.urls'

# # # إعدادات القوالب
# # TEMPLATES = [
# #     {
# #         'BACKEND': 'django.template.backends.django.DjangoTemplates',
# #         'DIRS': [BASE_DIR / 'templates'],
# #         'APP_DIRS': True,
# #         'OPTIONS': {
# #             'context_processors': [
# #                 'django.template.context_processors.request',
# #                 'django.contrib.auth.context_processors.auth',
# #                 'django.contrib.messages.context_processors.messages',
# #             ],
# #         },
# #     },
# # ]

# # WSGI_APPLICATION = 'Nursery_project.wsgi.application'

# # # قاعدة البيانات
# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.sqlite3',
# #         'NAME': BASE_DIR / 'db.sqlite3',
# #     }
# # }

# # # التحقق من كلمات السر (معطل مؤقتًا)
# # AUTH_PASSWORD_VALIDATORS = []

# # # اللغة والتوقيت
# # LANGUAGE_CODE = 'en-us'
# # TIME_ZONE = 'Africa/Cairo'
# # USE_I18N = True
# # USE_TZ = True


# # MEDIA_URL = '/media/'
# # MEDIA_ROOT = BASE_DIR / 'media'


# # STATIC_URL = '/static/'
# # STATIC_ROOT = BASE_DIR / 'staticfiles'

# # DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# # AUTH_USER_MODEL = 'App.User'


# # CSRF_COOKIE_SECURE = False
# # SESSION_COOKIE_SECURE = False
# # CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']


# # CORS_ALLOWED_ORIGINS = ['http://*', 'https://*']
# # CORS_ALLOW_CREDENTIALS = True
# # CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
# # CORS_ALLOW_HEADERS = [
# #     'content-type',
# #     'authorization',
# #     'x-csrftoken',
# #     'accept',
# #     'origin',
# # ]


# # REST_FRAMEWORK = {
# #     'DEFAULT_AUTHENTICATION_CLASSES': [],
# #     'DEFAULT_PERMISSION_CLASSES': [],
# # }


# # SIMPLE_JWT = {
# #     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
# #     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
# #     'ALGORITHM': 'HS256',
# #     'SIGNING_KEY': 'simple-key-for-testing',
# #     'AUTH_HEADER_TYPES': ('Bearer',),
# # }


# # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# # LOGGING = {
# #     'version': 1,
# #     'disable_existing_loggers': False,
# #     'handlers': {
# #         'console': {
# #             'class': 'logging.StreamHandler',
# #         },
# #     },
# #     'loggers': {
# #         'django': {
# #             'handlers': ['console'],
# #             'level': 'INFO',
# #             'propagate': True,
# #         },
# #     },
# # }



# from pathlib import Path
# from datetime import timedelta

# BASE_DIR = Path(__file__).resolve().parent.parent

# # إعدادات أساسية بسيطة
# SECRET_KEY = 'simple-key-for-testing'  # مفتاح بسيط للتجربة
# DEBUG = True  # مفعل للتجربة
# ALLOWED_HOSTS = ['192.168.135.14', 'localhost', '127.0.0.1']  # تحديد المضيفين المحليين

# # التطبيقات المثبتة
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'App',
#     'rest_framework',
#     'rest_framework_simplejwt',
#     'corsheaders',
# ]

# # الـ Middleware
# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'Nursery_project.urls'

# # إعدادات القوالب
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'Nursery_project.wsgi.application'

# # قاعدة البيانات
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# # التحقق من كلمات السر (معطل مؤقتًا)
# AUTH_PASSWORD_VALIDATORS = []

# # اللغة والتوقيت
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Africa/Cairo'
# USE_I18N = True
# USE_TZ = True

# # إعدادات الـ Media و Static Files
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH_USER_MODEL = 'App.User'

# # إعدادات CSRF
# CSRF_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = False
# CSRF_TRUSTED_ORIGINS = ['http://192.168.135.14:8000', 'http://localhost:8000']

# # إعدادات CORS
# CORS_ALLOWED_ORIGINS = [
#     'http://192.168.135.14:8000',
#     'http://localhost:8000',
#     'http://192.168.135.14',
#     'http://localhost',
# ]
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
# CORS_ALLOW_HEADERS = [
#     'content-type',
#     'authorization',
#     'x-csrftoken',
#     'accept',
#     'origin',
# ]

# # إعدادات REST Framework
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
# }

# # إعدادات Simple JWT
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': 'simple-key-for-testing',
#     'AUTH_HEADER_TYPES': ('Bearer',),
# }

# # إعدادات الإيميل
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# # إعدادات الـ Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }

from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# إعدادات أساسية بسيطة
SECRET_KEY = 'simple-key-for-testing'  # مفتاح بسيط للتجربة (غيّره في الإنتاج)
DEBUG = True  # مفعل للتجربة
ALLOWED_HOSTS = ['nursery-api-zzo0.onrender.com']  # السيرفر الخارجي

# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

# الـ Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Nursery_project.urls'

# إعدادات القوالب
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Nursery_project.wsgi.application'

# قاعدة البيانات
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# التحقق من كلمات السر (معطل مؤقتًا)
AUTH_PASSWORD_VALIDATORS = []

# اللغة والتوقيت
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True

# إعدادات الـ Media و Static Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'App.User'

# إعدادات CSRF
CSRF_COOKIE_SECURE = True  # مفعل لأن السيرفر الخارجي هيستخدم HTTPS
SESSION_COOKIE_SECURE = True  # مفعل لأن السيرفر الخارجي هيستخدم HTTPS
CSRF_TRUSTED_ORIGINS = ['https://nursery-api-zzo0.onrender.com']

# إعدادات CORS
CORS_ALLOWED_ORIGINS = [
    'https://nursery-api-zzo0.onrender.com',
    'http://localhost:8000',  # للتجربة المحلية لو لزم
    'http://127.0.0.1:8000',  # للتجربة المحلية لو لزم
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
    'accept',
    'origin',
]

# إعدادات REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# إعدادات Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'simple-key-for-testing',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# إعدادات الإيميل
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# إعدادات الـ Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}