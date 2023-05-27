class DevelopmentConfig():
    DEBUG = True

    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'janeiro'
    MYSQL_PASSWORD = 'admin'
    MYSQL_DB = 'jornada_almuerzo_gratis'


config = {
    'development':DevelopmentConfig
}