# -*- coding: utf-8 -*-
##########################################
# General config
##########################################

# Determine system whether start with debug mode
DEBUG = True

# Cookie security key
SECRET_KEY = 'AIzaSyAlpjgnmPOM99xvTK_KzGCvVWLMXC_MaA0'

##########################################
# Database config
##########################################

# db connection string
SQLALCHEMY_DATABASE_URI = 'sqlite:///projdb.sqlite'

# mongodb connection string
MONGODB_URI = 'mongodb://heroku_58kf4fqc:m1j3udgpd72eoab5radq1g2bho@ds231205.mlab.com:31205/heroku_58kf4fqc'
# MONGODB_URI = 'mongodb://localhost:27017/test'

# record number displayed in single page
PAGESIZE = 40

##########################################
# Task config
##########################################

# rabbit mq url
RABBITMQ_URL = 'amqp://NZ97ia81:-mYjIbOC34zOavnNXl1ndZd2Nb8rtoVa@happy-threar-806.bigwig.lshift.net:10264/286AM56zKV0R'

PING_URL = 'https://cxonlineshop1.herokuapp.com/ping'

##########################################
# Email config
##########################################

# the flag whether open email notification
ENABLE_MAIL_NOTICE = False

# the host of mail server
SMTP_HOST = 'smtp.163.com'

# default sender
EMAIL_SENDER = 'zhanglei520vip@163.com'

# the password of default sender
SENDER_PASS = '1qaz2wsx'

#dropzone setting
DROPZONE_UPLOAD_MULTIPLE = True
