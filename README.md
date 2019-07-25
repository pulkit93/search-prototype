# search-prototype
prototype app for searching using elasticsearch

# Running the app

- with Docker:

 `docker-compose up -d --build`

- without Docker:

 `gunicorn --workers=2 --bind=0.0.0.0:3000 server.app:app`
 
 Go to `localhost:3000/search?term=<your-search-term>&offset=<optional-offset>` to hit the api
 or `localhost:8080` to see the UI 
 
# Load data
 
Download data using,
 
`wget -w 2 -m -H "http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en"`

Extract these files into a `books/` directory in your project.

Load data to ES index using,

`docker exec gs-api python server/load_data.py`
 
