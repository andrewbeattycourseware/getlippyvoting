from flask import Flask, jsonify, request, abort, redirect

app = Flask(__name__, static_url_path='', static_folder='.')

acts=[
    { "id": 1, "actname":"Angel Abbey", "totalVotes":0}, 
    { "id": 2, "actname":"Daniel & Shona", "totalVotes":0}, 
    { "id": 3, "actname":"Catherina Roynane", "totalVotes":0}, 
    { "id": 4, "actname":"Gary Tobin and Crew", "totalVotes":0}, 
    { "id": 5, "actname":"John Gately", "totalVotes":0}, 
    { "id": 6, "actname":"Kelsea & Siobhan", "totalVotes":0}, 
    { "id": 7, "actname":"Ladies GAA", "totalVotes":0}, 
    { "id": 8, "actname":"Nigel Jennings & Kelsea", "totalVotes":0}, 
    { "id": 9, "actname":"Teresa & Maura", "totalVotes":0}, 
    { "id": 10, "actname":"Year 3 Social Care", "totalVotes":0}, 
    { "id": 11, "actname":"1st Year Outdoor Shane Halley", "totalVotes":0}, 
]


nextId=3
#app = Flask(__name__)


@app.route('/')
def index():
    urlRoot=request.url_root
    
    return redirect(urlRoot+"vote.html", code=302)

#curl "http://127.0.0.1:5000/acts"
@app.route('/acts')
def getAll():
    return jsonify(acts)

#curl "http://127.0.0.1:5000/acts/2"
@app.route('/acts/<int:id>')
def findById(id):
    foundActs = list(filter(lambda t: t['id'] == id, acts))
    if len(foundActs) == 0:
        return jsonify ({}) , 204

    return jsonify(foundActs[0])

#
@app.route('/acts', methods=['POST'])
def create():
    global nextId
    if not request.json:
        abort(400)
    # other checking 
    act = {
        "id": nextId,
        "actname": request.json['actname'],
        "totalVotes":0
    }
    nextId += 1
    acts.append(act)
    return jsonify(act)

@app.route('/acts/<int:id>' , methods=['PUT'])
def update(id):
    foundActs = list(filter(lambda t: t['id']== id, acts))
    if (len(foundActs) == 0):
        abort(404)
    if not request.json:
        abort(400)
    reqJson = request.json
    foundAct = foundActs[0]
    
    if 'actname' in reqJson:
        foundAct['actname'] = reqJson['actname']

    if 'totalVotes' in reqJson and type(reqJson['totalVotes']) is not int:
        abort(401) 
    if 'totalVotes' in reqJson:
        foundAct['totalVotes'] = reqJson['totalVotes']
    return jsonify(foundAct)


    
    return jsonify({"done":True})




@app.route('/acts/<int:id>' , methods=['DELETE'])
def delete(id):
    foundActs = list(filter(lambda t: t['id']== id, acts))
    if (len(foundActs) == 0):
        abort(404)
    acts.remove(foundActs[0])
    return jsonify({"done":True})

@app.route('/votes/<int:actId>', methods = ['POST'])
def addVote(actId):
    foundActs=list(filter(lambda t : t['id']==actId, acts))
    if len(foundActs)== 0:
        abort(404)
    if not request.json:
        abort(400)
    if not 'votes' in request.json or type(request.json['votes']) is not int:
        abort(401)
    newVotes = request.json['votes']
    print(newVotes)

    foundActs[0]['totalVotes'] += newVotes


    return jsonify(foundActs[0])

@app.route('/votes/leaderboard')
def getleaderBoard():
#ut.sort(key=lambda x: x.count, reverse=True)
    acts.sort(key=lambda x: x['totalVotes'], reverse=True)

    return jsonify(acts)


if __name__ == '__main__' :
    app.run(debug= True)