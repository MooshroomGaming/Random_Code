import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from kasa import SmartPlug

# Spotify API Credentials
SPOTIFY_CLIENT_ID = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

# Kasa Plug IP Address (Change to match your device's IP)
PLUG_IP = "192.168.x.x"

# Setup Spotify API
scope = "user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope=scope))

# Setup Kasa Smart Plug
plug = SmartPlug(PLUG_IP)

async def flash_plug(duration):
    """Flashes the smart plug on and off for the given duration."""
    await plug.update()
    await plug.turn_on()
    time.sleep(duration)
    await plug.turn_off()
    time.sleep(duration)

def get_current_track_tempo():
    """Gets the current track tempo (BPM) from Spotify."""
    playback = sp.current_playback()
    if playback and playback["is_playing"]:
        track_id = playback["item"]["id"]
        features = sp.audio_features(track_id)[0]
        bpm = features["tempo"]
        return 60 / bpm  # Convert BPM to beat duration (seconds per beat)
    return None

def main():
    """Main loop to sync plug flashing with Spotify playback."""
    print("Starting synchronization with Spotify...")
    try:
        while True:
            beat_duration = get_current_track_tempo()
            if beat_duration:
                print(f"Flashing with a beat duration of {beat_duration:.2f} seconds...")
                plug.loop.run_until_complete(flash_plug(beat_duration / 2))
            else:
                print("No playback detected. Retrying in 5 seconds...")
                time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        plug.loop.run_until_complete(plug.turn_off())

if __name__ == "__main__":
    main()
