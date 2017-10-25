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
#MONGODB_URI = 'mongodb://heroku_3gr09dlh:ohb0regig4p4bsphgktn25llge@ds113063.mlab.com:13063/heroku_3gr09dlh'
MONGODB_URI = 'mongodb://localhost:27017/test'

# record number displayed in single page
PAGESIZE = 20

##########################################
# Task config
##########################################

# rabbit mq url
RABBITMQ_URL = 'amqp://1G8enNXO:Nf_uWwcyHBs-jg3UhAkRskXZSLwh7ppq@sad-nelthilta-30.bigwig.lshift.net:11020/hOM1ppDgFf6w'

PING_URL = 'https://wavemonitor.herokuapp.com/ping'

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
