from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Thought:
    db = "group-project"
    
    def __init__(self, data):
        self.id = data['id']
        self.anime_id = data['anime_id']
        self.thoughts = data['thoughts']
        self.episodeNum = data['episodeNum']
        self.seasonNum = data['seasonNum']

    @classmethod
    def getAllThoughts(cls, data):
        query = "SELECT * FROM thoughts where anime_id = %(anime_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM thoughts Where id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print("----------------", results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        print (data)
        query = "UPDATE thoughts SET thoughts = %(thoughts)s WHERE id = %(id)s;"
        print(query)
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results

    @classmethod 
    def save(cls, data):
        query = "insert into thoughts (anime_id, episodeNum, seasonNum, thoughts) value ( %(anime_id)s, %(episodeNum)s, %(seasonNum)s, %(thoughts)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results


    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM thoughts WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def thoughtValidation(thought):
        isValid = True
        if len(thought['thoughts']) < 10:
            flash("please provide thoughts of at least 10 characters.")
            isValid = False
        if int(thought['episodeNum']) < 1:
            flash("Please provide a episode number of at least 1.")
            isValid = False
        if int(thought['episodeNum']) < 1:
            flash("Please choose a season number of at least 1.")
            isValid = False
        return isValid