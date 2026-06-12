from app import app 
from app.services.SongPlayerService import SongPlayerService

sps = SongPlayerService()

if __name__ == "__main__":
    sps.start_background_scheduler()
    
    app.run(host="0.0.0.0", port=8000, debug=True)