from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Anime:
    db_name = "group-project"
    
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
        results = connectToMySQL(cls.db_name).query_db(query)
        animes = []
        print(results)
        for anime in results:
            animes.append(cls(anime))
        return animes

    @classmethod
    def save(cls, data):
        query = "insert into animes (user_id, title, episodeNum, seasons, statusDone, startedAt, genre, coverImg) value (%(user_id)s, %(title)s, %(episodeNum)s, %(seasons)s, %(statusDone)s, %(startedAt)s, %(genre)s, %(coverImg)s);"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @classmethod
    def getAnime(cls, data):
        query = "SELECT * FROM animes Where animes.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print("----------------", results)
        anime = cls(results[0])
        return anime

    @classmethod
    def update(cls, data):
        print (data)
        query = "UPDATE animes SET title = %(title)s, episodeNum = %(episodeNum)s, seasons = %(seasons)s, statusDone = %(statusDone)s, startedAt = %(startedAt)s, genre = %(genre)s, coverImg = %(coverImg)s WHERE id = %(id)s;"
        print(query)
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        return results

    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM animes WHERE id = %(id)s;"
        print(query)
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def animeValidation(input):
        isValid = True
        if len(input['title']) < 3:
            flash("Please provide a title of at least 3 characters")
            isValid= False
        if input['episodeNum'] < 0:
            flash("Please provide a episode number of at least 1")
            isValid= False
        if input['seasons'] < 0:
            flash("Please provide a number of seasons of at least 1")
            isValid= False
        if len(input['startedAt']) < 1:
            flash("Please provide a platform to watch on")
            isValid= False
        if len(input['genre']) < 1:
            flash("Please seclect a genre")
            isValid= False
        return isValid


