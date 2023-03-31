from environs import Env

env = Env()
env.read_env()

DB_HOST = env('DB_HOST')
DB_PORT = env('DB_PORT')
DB_DIALECT = env('DB_DIALECT')
DB_DRIVER = env('DB_DRIVER')
DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')
DB_NAME = env('DB_NAME')
SECRET_KEY = env('SECRET_KEY')
