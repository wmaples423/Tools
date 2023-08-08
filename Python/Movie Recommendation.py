import rottentomatoes as rt
# from plexapi.myplex import MyPlexAccount
# account = MyPlexAccount('<USERNAME>', '<PASSWORD>')
# plex = account.resource('<SERVERNAME>').connect()

movie = rt.Movie(input("Enter a movie: "))
print(movie)

