import psycopg2
from postgis.psycopg import register
import codecs
def create_tables():

	conn_string = "host='localhost' dbname='postgres' user='postgres' password='postgres'"
	conn = psycopg2.connect(conn_string)
	conn.set_isolation_level('ISOLATION_LEVEL_AUTOCOMMIT')
	cursor = conn.cursor()
	register(conn)

	#creando la tabla
	drop_table="""DROP TABLE IF EXISTS Restaurants"""
	create_table = """  CREATE TABLE Restaurants
                        (
                             
								id TEXT PRIMARY KEY,
								rating INTEGER,
								name TEXT,
								site TEXT,
								email TEXT,
								phone TEXT,
								street TEXT,
								city TEXT,
								state TEXT,
								lat FLOAT,
								lng FLOAT,
								geom geometry(POINT,4326)
                        );
                        """

	update_table="""UPDATE restaurants SET geom = ST_SetSRID(ST_Point(lng,lat),4326)::geometry;"""
	cursor.execute(drop_table)
	cursor.execute(create_table)
	


	#cargando los datos
	with codecs.open('restaurantes.csv', 'r',encoding='utf-8',errors='ignore') as f:
		next(f) 
		copy = "COPY Restaurants(id,rating,name,site,email,phone,street,city,state,lat,lng) FROM STDIN  with csv"
		cursor.copy_expert(sql=copy, file=f)


	cursor.execute(update_table)
	cursor.close()
	conn.commit()

if __name__ == '__main__':
    create_tables()