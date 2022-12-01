# PerformanceDB
 Fill and read data from a database about performance statistics


## Requirements

- Docker
- Python3
- [`pip install -r requirements.txt`](requirements.txt)

## Testing it out

Start up the mondodb server.
```
./startMongo.sh
```

Fill the database with fake data.
```
./FillMongo.py
```

Start jupyer notebook.
```
jupyter notebook
```

and open [ReadMongoDB](ReadMongoDB.ipynb) to access and see data in the database.