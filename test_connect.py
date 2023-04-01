from configuration import env
import psycopg2


def postgres_test():
    try:
        conn = psycopg2.connect(f"dbname={env('DB_NAME')} "
                                f"user={env('DB_USER')} "
                                f"host={env('DB_HOST')} "
                                f"password={env('DB_PASSWORD')} "
                                f"connect_timeout=1 ")
        conn.close()
        return True
    except:
        return False
