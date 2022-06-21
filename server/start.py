import os

from panel import app, db
from panel import config


if __name__ == '__main__':
    if not 'steal.db' in str(os.listdir(os.getcwd())):
        try:
            db.create_all()
            print('Database was created')
        except:
            print('Database create Error')
    else:
        print('Database was finded')
    app.run(host=config.server_host, port=config.server_port, debug=True)
