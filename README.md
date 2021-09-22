# top_music_analysis

The pipeline for getting tracks features from the most popular Spotify playlists, cluster analysis, and visualization.

### Data description

Dataframe index - playlist name.

Columns:
- **name** - name of the song
- **artist** - name of the artist
- **popularity** - the popularity of the track. The value will be between 0 and 100, with 100 being the most popular
- **danceability** - this value describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity
- **energy** - energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity
- **key** -	the key the track is in. Integers map to pitches using standard Pitch Class notation. 
- **loudness** - the overall loudness of a track in decibels (dB)
- **mode** - mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived
- **speechiness** - this value detects the presence of spoken words in a track
- **acousticness** - a confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic
- **instrumentalness** - predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context
- **liveness** - detects the presence of an audience in the recording
- **valence**	- a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track
- **tempo**	- the overall estimated tempo of a track in beats per minute (BPM)
- **duration_ms** - the duration of the track in milliseconds

### Repository structure

```
|    ├── data
|       ├── clustered_data.csv -- Source data with labels after the clustering.
|       └── data.csv -- Source data obtained from the Spotify API.
|    ├── notebooks
|       ├── eda.ipynb -- Jupyter notebook with an exploration data analysis.
|       └── eda.pdf -- PDF-version of EDA notebook.
|    ├── clustering.py -- Script with clustering functions.
|    ├── config.py -- Settings and path configurations.
|    ├── pipeline.py -- Luigi pipeline to run tasks (getting the data, clustering).
│    └── spotify.py -- Script to get the songs data from the Spotify API.
```
