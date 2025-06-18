

# from datetime import timedelta
# from pathlib import Path


# BASE_DIR = Path(__file__).resolve().parent.parent


# SECRET_KEY = 'simple-key-for-testing'  
# DEBUG = True  
# ALLOWED_HOSTS = [
#     'nursery-api-zzo0.onrender.com',
#     'localhost',
#     'http:// 192.168.135.14:8000',
#     '127.0.0.1',
#     '605b-154-236-147-226.ngrok-free.app',
#     '0f66-154-236-147-226.ngrok-free.app',  
      
# ]


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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# AUTH_PASSWORD_VALIDATORS = []


# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Africa/Cairo'
# USE_I18N = True
# USE_TZ = True


# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'


# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AUTH_USER_MODEL = 'App.User'


# CSRF_COOKIE_SECURE = True  
# SESSION_COOKIE_SECURE = True  
# CSRF_TRUSTED_ORIGINS = [
#     'https://nursery-api-zzo0.onrender.com',
#     'https://605b-154-236-147-226.ngrok-free.app',  
#     'http://localhost:8000',
#     'http://192.168.135.14:8000',
#     'http://127.0.0.1:8000'
# ]


# CORS_ALLOWED_ORIGINS = [
#     'https://nursery-api-zzo0.onrender.com',
#     'https://605b-154-236-147-226.ngrok-free.app',
#     'http://localhost:8000',
#     'http://192.168.135.14:8000',
#     'http://127.0.0.1:8000',
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

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.AllowAny',
#     ],
# }


# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': 'simple-key-for-testing',  
#     'AUTH_HEADER_TYPES': ('Bearer',),
# }


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


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
# AUTHENTICATION_BACKENDS = [
#     'App.authentication.EmailBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]




# from datetime import timedelta
# from pathlib import Path

# # تعريف المسار الأساسي للمشروع
# BASE_DIR = Path(__file__).resolve().parent.parent

# # إعدادات أساسية
# SECRET_KEY = 'simple-key-for-testing'  # تحذير: غيّر هذا المفتاح في الإنتاج إلى مفتاح قوي وفريد
# DEBUG = True  # مفعل للتطوير، قم بتعطيله (False) في الإنتاج
# ALLOWED_HOSTS = [
#     'nursery-api-zzo0.onrender.com',
#     'localhost',
#     'http:// 192.168.135.14:8000',
#     '127.0.0.1',
#     'https://610c-154-236-147-226.ngrok-free.app',
#     'c507-196-135-64-221.ngrok-free.app'  # الرابط الجديد
# ]

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
#     'corsheaders.middleware.CorsMiddleware',  # يجب أن يكون أولًا لمعالجة CORS
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# # إعدادات URL الرئيسية
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

# # تطبيق WSGI
# WSGI_APPLICATION = 'Nursery_project.wsgi.application'

# # قاعدة البيانات (SQLite للتطوير)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# # تعطيل التحقق من كلمات السر مؤقتًا (للتطوير فقط)
# AUTH_PASSWORD_VALIDATORS = []

# # إعدادات اللغة والتوقيت
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Africa/Cairo'
# USE_I18N = True
# USE_TZ = True

# # إعدادات الملفات الثابتة والوسائط
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# # نوع الحقل التلقائي الافتراضي
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # نموذج المستخدم المخصص
# AUTH_USER_MODEL = 'App.User'

# # إعدادات CSRF (مطابقة لـ HTTPS مع ngrok)
# CSRF_COOKIE_SECURE = True  # مفعل لأن ngrok يستخدم HTTPS
# SESSION_COOKIE_SECURE = True  # مفعل لأن ngrok يستخدم HTTPS
# CSRF_TRUSTED_ORIGINS = [
#     'https://nursery-api-zzo0.onrender.com',
#     'https://610c-154-236-147-226.ngrok-free.app',  # الرابط الجديد
#     'http://localhost:8000',
#     'http://192.168.135.14:8000',
#     'http://127.0.0.1:8000'
# ]

# # إعدادات CORS
# CORS_ALLOWED_ORIGINS = [
#     'https://nursery-api-zzo0.onrender.com',
#     'https://610c-154-236-147-226.ngrok-free.app',  # الرابط الجديد
#     'http://localhost:8000',
#     'http://192.168.135.14:8000',
#     'http://127.0.0.1:8000'
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

# # إعدادات Django REST Framework
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
#     'SIGNING_KEY': 'simple-key-for-testing',  # تحذير: غيّر هذا في الإنتاج
#     'AUTH_HEADER_TYPES': ('Bearer',),
# }

# # إعدادات الإيميل (للتطوير فقط)
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


from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# الإعدادات الأساسية
SECRET_KEY = 'simple-key-for-testing'  # تغيير هذا في الإنتاج!
DEBUG = True  # وضع التطوير (تعطيل في الإنتاج)
ALLOWED_HOSTS = [
    '*',  # للتنمية فقط
    'nursery-api-zzo0.onrender.com',  # ⬅️ رابط ngrok بدون https://
    'localhost',
    '127.0.0.1'
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # التطبيقات الخارجية
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # تطبيقاتي
    'App',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # يجب أن يكون أولًا
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Nursery_project.urls'

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

# قاعدة البيانات (SQLite للتطوير)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# تعطيل التحقق من كلمة السر (للتطوير فقط)
AUTH_PASSWORD_VALIDATORS = []

# اللغة والتوقيت
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True

# الملفات الثابتة
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# نموذج المستخدم المخصص
AUTH_USER_MODEL = 'App.User'

# إعدادات CORS
# CORS_ALLOW_ALL_ORIGINS = True  # للتنمية فقط
CORS_ALLOWED_ORIGINS = [
    'https://nursery-api-zzo0.onrender.com',  # ⬅️ رابط ngrok مع https://
    'http://localhost:8000',
    'http://127.0.0.1:8000'
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['*']
CORS_ALLOW_HEADERS = ['*']

# إعدادات CSRF
CSRF_COOKIE_SECURE = False  # تعطيل في التنمية
SESSION_COOKIE_SECURE = False  # تعطيل في التنمية
CSRF_TRUSTED_ORIGINS = [
    'https://nursery-api-zzo0.onrender.com',  # ⬅️ رابط ngrok مع https://
    'http://localhost:8000',
    'http://127.0.0.1:8000'
]

# إعدادات REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # للتنمية فقط
    ),
}

# إعدادات JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# إعدادات البريد الإلكتروني (للتطوير)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# إعدادات التسجيل
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}