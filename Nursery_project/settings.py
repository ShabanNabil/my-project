
# from pathlib import Path
# from datetime import timedelta
# import os
# from decouple import config  


# BASE_DIR = Path(__file__).resolve().parent.parent


# # SECRET_KEY = config('SECRET_KEY', default='your-very-secure-secret-key-1234567890!@#$%^&*')  
# DEBUG = config('DEBUG', default=False, cast=bool)  
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,192.168.124.14,nursery-api-zzo0.onrender.com')
# ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS.split(',')]
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
# # بما إنك بتستخدم SQLite3
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# # التحقق من كلمات السر
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # اللغة والتوقيت
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Africa/Cairo'
# USE_I18N = True
# USE_TZ = True

# # الملفات الثابتة
# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# # ملفات الوسائط (لصور الحضانات)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# # نوع المفتاح الأساسي الافتراضي
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # نموذج المستخدم المخصص
# AUTH_USER_MODEL = 'App.User'

# # إعدادات CSRF
# CSRF_TRUSTED_ORIGINS = [
#     'http://localhost:8000',
#     'http://127.0.0.1:8000',
#     'http://192.168.124.14:8000',
#     'https://nursery-api-zzo0.onrender.com',  # للإنتاج
# ]
# CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)  # True في الإنتاج
# SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)  # True في الإنتاج

# # إعدادات CORS
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
#     'http://192.168.124.14:3000',
#     # لو عندك نطاق للواجهة الأمامية في الإنتاج، أضفه هنا
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
#         'rest_framework.authentication.SessionAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
# }

# # إعدادات Simple JWT
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': False,
#     'UPDATE_LAST_LOGIN': True,
#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': SECRET_KEY,
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
# }

# # إعدادات الإيميل
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='your-email@gmail.com')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='your-app-password')
# DEFAULT_FROM_EMAIL = 'Nursery App <your-email@gmail.com>'

# # إعدادات تسجيل الأخطاء
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#         'file': {
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'debug.log',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'App': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }


from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# إعدادات أساسية بسيطة
SECRET_KEY = 'simple-key-for-testing'  # مفتاح بسيط للتجربة
DEBUG = True  # مفعل للتجربة
ALLOWED_HOSTS = ['*']  # السماح لجميع المضيفين

# التطبيقات المثبتة (مع إضافة staticfiles)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # أضفنا ده
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

# ملفات الوسائط
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ملفات الـ static (أضفناها)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# نوع المفتاح الأساسي الافتراضي
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# نموذج المستخدم المخصص
AUTH_USER_MODEL = 'App.User'

# إعدادات CSRF
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']

# إعدادات CORS
CORS_ALLOWED_ORIGINS = ['http://*', 'https://*']
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
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
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

# إعدادات تسجيل الأخطاء
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