from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(app)
#MUST CREATE DATABASE ON FIRST RUN. REMOVE THE LINE AFTER
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)
    
    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

names = {"Camille":{"Q":"Precision Protocol","W":"Tactical Sweep","E":"Hookshot","R":"Hextech Ultimatum"},
         "Irelia":{"Q":"Bladesurge","W":"Defiant Dance","E":"Flawless Duet","R":"Vanguard's Edge"}}
         
video_put_args = reqparse.RequestParser()#CReate Parser to handle arguments being Sent     
video_put_args.add_argument("name",type=str, help="Name of Video (str)",required =True) #Each represents an argument and definitions to parse. Add requireed=True.
video_put_args.add_argument("views",type=int, help="Views of Video (int)")  
video_put_args.add_argument("likes",type=int, help="Likes of Video (int)")  

resource_fields = {
    'id' :fields.Integer,
    'name': fields.String,
    'views':fields.Integer,
    'likes':fields.Integer

}

#Define Resource, override methods
class HelloWorld(Resource): 
#HelloWorld inherits resource to return what we want.Allows override of methods (GET,PUT,DELETE, ETC..)
    def get(self,name):
        return names[name]#need to make sure data returned is serializable. (inside python dictionary to represent JSON format, architecture constraint)


class Video(Resource):
        @marshal_with(resource_fields)
        def get(self,video_id):
            result = VideoModel.query.filter_by(id=video_id).first()
            if not result:
                abort(404,message ="Could not find..")
            return result
            
        @marshal_with(resource_fields)
        def put(self,video_id):
            args = video_put_args.parse_args()
            result = VideoModel.query.filter_by(id=video_id).first()
            if result:
                abort(409, message = "ID Taken...")
            video = VideoModel(id=video_id, name = args['name'], views = args['views'], likes = args['likes'])
            db.session.add(video)
            db.session.commit()
            return video, 201#201 stands for created. There are default sends, 200 by defualt (nothing broke)
            
        def delete(self,video_id):
            abort_if_video_id_doesnt_exist(video_id)
            del videos [video_id]
            return'',204
            
api.add_resource(HelloWorld, "/helloworld/<string:name>") #'/' stands for default URL. use target request in key parameter. Want user to type some string after hellowrold, will be name.
api.add_resource(Video, "/video/<int:video_id>")
if __name__ == "__main__":
    app.run(debug=True)
    