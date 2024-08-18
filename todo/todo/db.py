
from sqlmodel import SQLModel , create_engine , Session
from todo import setting


    
#5: create the engin : engine is one for whole application   
connection_string : str = str(setting.DATABASE_URL).replace("postgresql","postgresql+psycopg")
engine = create_engine(connection_string, connect_args={"sslmode":"require"},pool_recycle=300,echo=True)

#6: create the table
def create_tables():
    SQLModel.metadata.create_all(engine)


#7: session: seperate session for each functionality/transactio
def get_session(): # create function as dependence 
    with Session(engine) as session:  # create session like session= Session(engine)
        yield session # generated function that return the session