from sqlalchemy import create_engine
from utilities.database_utilities import USER, PASSWORD, HOST, PORT, DATABASE

def get_connection():
    engine = create_engine("postgresql://{0}:{1}@{2}:{3}/{4}".format(
        USER, PASSWORD, HOST, PORT, DATABASE))
    
    return engine