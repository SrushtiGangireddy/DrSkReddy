import os
import psycopg2
import urlparse

DATABASE_URL='postgres://wiadnhuyckvaxo:da9e87326d11b82333e784095a16ef285b0e9450275e7ce405412dcb0dc0c567@ec2-50-19-218-160.compute-1.amazonaws.com:5432/d8pi92het8nh2b'
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
)
