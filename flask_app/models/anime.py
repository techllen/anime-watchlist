from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, redirect

class Anime:
    db = "group-project"
    
    def __init__(self, data):
        self.user_id = data['user_id']
        self.id = data['id']
        self.title = data['title']
        self.episodeNum = data['episodeNum'] or 1
        self.seasons = data['seasons'] or 1
        self.statusDone = data['statusDone'] or 'inProgress'
        self.startedAt = data['startedAt'] 
        self.genre = data['genre']
        self.coverImg = data['coverImg']

    @classmethod
    def getAllAnimes(cls):
        query = "SELECT * FROM animes"
        results = connectToMySQL(cls.db).query_db(query)
        animes = []
        print(results)
        for anime in results:
            animes.append(cls(anime))
        return animes

    @classmethod
    def save(cls, data):
        query = "insert into animes (user_id, title, episodeNum, seasons, statusDone, startedAt, genre, coverImg) value (%(user_id)s, %(title)s, %(episodeNum)s, %(seasons)s, %(statusDone)s, %(startedAt)s, %(genre)s, %(coverImg)s);"
        return connectToMySQL(cls.db).query_db(query,data)
        

    @classmethod
    def getAnime(cls, data):
        query = "SELECT * FROM animes Where animes.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print("----------------", results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def abandon(cls, data):
        query = "UPDATE animes SET statusDone='abandoned' WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def complete(cls, data):
        query = "UPDATE animes SET statusDone='completed' WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getByGenre(cls, data):
        query = "SELECT * FROM animes where genre=%(genre)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        animesInGenre = []
        for anime in results:
            animesInGenre.append(cls(anime))
        return animesInGenre

    @classmethod
    def update(cls, data):
        print (data)
        query = "UPDATE animes SET title = %(title)s, episodeNum = %(episodeNum)s, seasons = %(seasons)s, statusDone = %(statusDone)s, startedAt = %(startedAt)s, genre = %(genre)s, coverImg = %(coverImg)s WHERE animes.id = %(id)s;"
        print(query)
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results

    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM animes WHERE id = %(id)s;"
        print(query)
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def animeValidation(anime):
        isValid = True
        try:
            ep = int(anime['episodeNum'])
            se = int(anime['seasons'])

            if len(anime['title']) < 3:
                flash("Please provide a title of at least 3 characters", 'anime-error')
                isValid= False
            if not anime['episodeNum']:
                flash("Please provide an episode", 'anime-error')
                isValid= False
            if ep <= 0:
                flash("Please provide a episode number of at least 1", 'anime-error')
                isValid= False
            if not anime['seasons']:
                flash("Please provide a season", 'anime-error')
                isValid= False
            if se <= 0:
                flash("Please provide a season number of at least 1", 'anime-error')
                isValid= False
            if not anime['startedAt']:
                flash("Please provide a date started", 'anime-error')
                isValid= False
        except:
            flash("Invalid inputs, 'anime-error")
            return redirect("/dashboard")
        return isValid


