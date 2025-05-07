
# """
# إعدادات Django لمشروع Nursery_project.
# تم إنشاؤه بواسطة 'django-admin startproject' باستخدام Django 5.2.
# """

# from pathlib import Path
# from datetime import timedelta

# # مسار المشروع
# BASE_DIR = Path(__file__).resolve().parent.parent

# # إعدادات أساسية
# SECRET_KEY = 'your-new-secure-secret-key-here'  # تأكد إنك تستخدم مفتاح قوي وفريد (غيّره)
# DEBUG = False  # خلّيه False للإنتاج على Render

# # المضيفين المسموح بيهم
# ALLOWED_HOSTS = ['nursery-api-zzo0.onrender.com', '.onrender.com']

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
#     'corsheaders',  # أضف corsheaders
# ]

# # الـ Middleware
# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',  # أضف في الأول
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
#         'DIRS': [],
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

# # التحقق من كلمات السر
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # اللغة والتوقيت
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # الملفات الثابتة
# STATIC_URL = '/static/'
# STATICFILES_DIRS = []
# STATIC_ROOT = BASE_DIR / "staticfiles"

# # ملفات الوسائط (لصور الحضانات)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# # نوع المفتاح الأساسي الافتراضي
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # نموذج المستخدم المخصص
# AUTH_USER_MODEL = 'App.User'

# # إعدادات CORS للسماح لـ Flutter بالاتصال
# CORS_ALLOW_ALL_ORIGINS = False  # False للإنتاج
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:52897",  # للتطوير لو هتحتاجه
#     "https://your-flutter-app-domain.com",  # أضف نطاق Flutter لو عندك واحد
# ]
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
# CORS_ALLOW_HEADERS = [
#     'content-type',
#     'authorization',
#     'X-CSRFToken',
# ]

# # إعدادات CSRF للإنتاج
# CSRF_TRUSTED_ORIGINS = [
#     'https://nursery-api-zzo0.onrender.com',
# ]
# CSRF_COOKIE_SECURE = True  # True للإنتاج (HTTPS)
# SESSION_COOKIE_SECURE = True  # True للإنتاج (HTTPS)

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
#     'UPDATE_LAST_LOGIN': False,
#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': SECRET_KEY,
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
# }

# # إعدادات تسجيل الأخطاء للتصحيح
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
#             'level': 'INFO',  # INFO للإنتاج
#         },
#     },
# }

"""
إعدادات Django لمشروع Nursery_project.
تم إنشاؤه بواسطة 'django-admin startproject' باستخدام Django 5.2.
"""

from pathlib import Path
from datetime import timedelta
import os

# مسار المشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# إعدادات أساسية
SECRET_KEY = 'django-insecure-@k3x7v!p#q9w^r2m&y5n(h8l)z0c$v4b*t1u+j6e-o5i8g'  # مفتاح آمن جديد (غيّريه لو عايزة)
DEBUG = False  # خلّيه False للإنتاج على Render

# المضيفين المسموح بيهم
ALLOWED_HOSTS = ['nursery-api-zzo0.onrender.com', '.onrender.com']

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
    'corsheaders',  # أضف corsheaders
]

# الـ Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # أضف في الأول
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # أضف WhiteNoise لخدمة الملفات الثابتة
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
        'DIRS': [],
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
# استخدم PostgreSQL بدلاً من SQLite للإنتاج على Render
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'nursery_db'),
        'USER': os.getenv('DB_USER', 'nursery_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'your_db_password'),
        'HOST': os.getenv('DB_HOST', 'your_render_postgres_host'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# التحقق من كلمات السر
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# اللغة والتوقيت
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# الملفات الثابتة
STATIC_URL = '/static/'
STATICFILES_DIRS = []
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # لخدمة الملفات الثابتة في الإنتاج

# ملفات الوسائط (لصور الحضانات)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# نوع المفتاح الأساسي الافتراضي
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# نموذج المستخدم المخصص
AUTH_USER_MODEL = 'App.User'

# إعدادات CORS للسماح لـ Flutter بالاتصال
CORS_ALLOW_ALL_ORIGINS = False  # False للإنتاج
CORS_ALLOWED_ORIGINS = [
    "http://localhost:52897",  # للتطوير على المحاكي
    "http://10.0.2.2:52897",   # للمحاكي على Android
    "http://localhost",        # للتطوير المحلي
    "https://nursery-api-zzo0.onrender.com",  # للسيرفر نفسه
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'X-CSRFToken',
]

# إعدادات CSRF للإنتاج
CSRF_TRUSTED_ORIGINS = [
    'https://nursery-api-zzo0.onrender.com',
]
CSRF_COOKIE_SECURE = True  # True للإنتاج (HTTPS)
SESSION_COOKIE_SECURE = True  # True للإنتاج (HTTPS)

# إعدادات REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# إعدادات Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# إعدادات تسجيل الأخطاء للتصحيح
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
            'level': 'INFO',  # INFO للإنتاج
        },
    },
}