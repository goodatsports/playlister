import MySQLdb
import sys
import random

#   NOTES
# HIP HOP id_genre = 151
# SPECIALTY = 153
# row 1 = file path
# row 14 = track time
# row 20 = artist
# row 22 = song title
# row 23 = album


# genre of music which playlist is to be populated with
genre = sys.argv[1]

# counter for total length of playlist track times
totalLength = 0;

# Genres in RadioDJ are organized by an int value called id_genre, I have no idea what
# criteria is used to determine a genre's id
if genre.lower() == "hiphop":
    id_genre = 151
elif genre.lower() == "specialty":
    id_genre = 153
else:
    sys.exit("Invalid genre entered!")


# Connect to database
db = MySQLdb.connect(host="localhost",
                     user= "root",
                     passwd="******",
                     db="******")
# Create cursor object
cursor = db.cursor()

# Query database, grab a random assortment of songs within genre passed in sysarg
cursor.execute("SELECT * FROM songs WHERE id_genre = %s ORDER BY RAND() LIMIT 20" % id_genre )

# Save returned songs retrieved by cursor object
songPool = cursor.fetchall()

# Create empty .m3u file and write header
targetFile = open(genre+".m3u", 'w')
targetFile.write("#EXTM3U\n")

# Counter variable for running through randomized song pool
i = 0
# Keep adding tracks until the total length is roughly a full hour
while(totalLength + 120 < 3600):
    newSong = songPool[i]

    # These index values are based on how RadioDJ organizes its MySQL columns
    file_path = newSong[1]
    track_time = str(int(round(newSong[14])))
    artist = newSong[20]
    track_title = newSong[22]
    # Append this song to the playlist
    targetFile.write("#EXTINF:"+track_time +","+artist+ " - " +track_title+"\n")
    targetFile.write(file_path+"\n\n")

    # Update counters
    i += 1
    totalLength += int(track_time)

# Save file and close database connection
targetFile.close()
db.close()
