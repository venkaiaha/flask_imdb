from flask import Flask,json,jsonify,json_available
from flask_restplus import Resource,Api,fields
from flask_pymongo import PyMongo
from collections import defaultdict
from bson.json_util import dumps
from flask_cors import CORS
from flask_restplus import cors

app=Flask(__name__)
api=Api(app)
cors=CORS(app)
app.config["MONGO_URI"]='mongodb://localhost:27017/imdb'
mongo=PyMongo(app)
imdb_model=api.model('imdb',{'name':fields.String,'99popularity':fields.String,'director':fields.String,'imdb_score':fields.String,'genre':fields.String})
obj=mongo.db.movies

@api.route("/all")
class AllMovies(Resource):
    # @cors.crossdomain(origin='*')
    def get(self):
        l=[]
        r= obj.find()
        for i in r:
            print(i)
            dic={'name':i['name'],"popularity":i["99popularity"],'director':i['director'],'imdb_score':i['imdb_score'],'genre':i['genre']}
            l.append(dic)
        return jsonify(l)

@api.route("/limit")
class LimitedMovies(Resource):
    # @cors.crossdomain(origin='*')
    def post(self):
        data=api.payload
        lim= data['limit']
        ski = data['skip']
        l=[]
        r= obj.find().skip(ski).limit(lim)
        cnt=obj.find().count()
        for i in r:
            print(i)
            dic={'name':i['name'],"popularity":i["99popularity"],'director':i['director'],'imdb_score':i['imdb_score'],'genre':i['genre']}
            l.append(dic)
        return jsonify({"data":l,"count":cnt})


@api.route("/1")
class TopDirector(Resource):
    # @cors.crossdomain(origin='*')
    def get(self):
        d1=obj.find()
        hsc=defaultdict(list)
        for i in d1:
            hsc[i['director']].append(i['name'])
        d,m=max(hsc.items(),key=lambda x:len(x[1]))
        return jsonify({'td':d,"cnt":len(m),"ml":m})
# @api.route("/3")
# class TopTenMovies(Resource):
#     # @cors.crossdomain(origin='*')
#     def get(self):
#         d1=obj.find()
#         hsc=defaultdict(list)
#         for i in d1:
#             hsc[i['name']].append(i['imdb_score'])
#         s=sorted(hsc.items(),key=lambda x:x[1],reverse=True)
#         return jsonify({"top10":s[:10]})
# @api.route("/4")
# class TopTenMovies(Resource):
#     def get(self):
#         d1=obj.find()
#         hsc=defaultdict(list)
#         for i in d1:
#             hsc[i['name']].append(i['imdb_score'])
#         s=sorted(hsc.items(),key=lambda x:x[1],reverse=True)
#         return {"Least Wached Movie :":s[-1]}

# @api.route("/2")
# class PopularGenere(Resource):
#     # @cors.crossdomain(origin='*')
#     def get(self):
#         d1=obj.find()
#         hsc=defaultdict(list)
#         for i in d1:
#             hsc[i['99popularity']].append(i['genre'])
#         p,g=max(hsc.items(),key=lambda x:x[0])
#         return jsonify({"BG":g,"popularity":p})
@api.route("/5")
class BestMovieDirec(Resource):
    # @cors.crossdomain(origin='*')
    def get(self):
        d1=obj.find()
        hsc=defaultdict(list)
        for i in d1[0:100]:
                hsc[i['director']].append(i['99popularity'])
        s=sorted(hsc.items(),key=lambda x:max(x[1]),reverse=True)
        r=s[0]
        return jsonify({"BD":r})
@api.route("/new")
class PostMethod(Resource):
    # @cors.crossdomain(origin='*',headers=['Content-Type', 'application/json'])
    @api.expect(imdb_model)
    def post(self):
        '''
        This method allows you to post a DB entry.
        '''
        data = api.payload
        obj.insert(data)
        data.pop('_id')
        return jsonify(data)

if __name__ == "__main__":
    app.run()
