from flask import Flask, render_template,request,jsonify
from flask_socketio import SocketIO
import pymysql
import json
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)








#client array
users={}


#db connect
hostname = 'localhost'
username = 'root'
password = ''
database = 'mingleBox'
myconn = pymysql.connect( host=hostname, user=username, passwd=password, db=database ,cursorclass=pymysql.cursors.DictCursor)
conn = myconn.cursor()


@app.route('/')
def sessions():
    return "hello"

# ! Signup for coder  
@app.route("/coderRegister", methods=['POST'])
def coderRegister():
    count=conn.execute("""Insert into coders(id,username,mail,password) Values(NULL,%s,%s,sha2(%s,256))""",[request.form.get("username"),request.form.get("mail"),request.form.get("password")])
    myconn.commit()
    print(count)
    if(count==0):
        return "error"
    return "done"

# ! Signup for buyers
@app.route("/buyerRegister", methods=['POST'])
def buyerRegister():
    count=conn.execute("""Insert into buyers(id,username,mail,password,company) Values(NULL,%s,%s,sha2(%s,256),%s)""",[request.form.get("username"),request.form.get("mail"),request.form.get("password"),request.form.get("company")])
    myconn.commit()
    print(count)
    if(count==0):
        return "error"
    return "done"

# ! Login for coders
@app.route("/coderValidate", methods=['POST'])
def coderValidate():
    conn.execute("""Select SHA2(id,256) from coders where mail=%s and password=%s""",[request.form.get("mail"),request.form.get("password")])
    result=conn.fetchall()
    print(result)
    if(len(result)==0):
        return "error"
    return "done"

# ! Login for buyers
@app.route("/buyerValidate", methods=['POST'])
def buyerValidate():
    conn.execute("""Select SHA2(id,256) from buyers where mail=%s and password=%s""",[request.form.get("mail"),request.form.get("password")])
    result=conn.fetchall()
    print(result)
    if(len(result)==0):
        return "error"
    return json.dumps(result)

# ! buyer verification
@app.route("/buyerVerification", methods=['POST'])
def buyerVerification():
    conn.execute("""Select 'verified' from buyers where sha2(mail,256)=%s""",[request.form.get("mail")])
    result=conn.fetchall()
    print(result)
    if(len(result)==0):
        return "error"
    return "done"

# ! add technology to coders
@app.route("/addCoderTechnology", methods=['POST'])
def addCoderTechnology():

    # check if tachnology is valid
    conn.execute("""Select id from technology where technology=%s""",[request.form.get("technology")])
    result=conn.fetchall()

    if(len(result)==0):
        return "error"
    
    conn.execute("""Select technology from coders where sha2(mail,256)=%s""",[request.form.get("mail")])
    result=conn.fetchall()

    if(len(result)==0):
        return "error"
    
    tech=[]

    try:
        tech=json.loads(result[0]["technology"])
    except:
        pass

    if(request.form.get("technology") in tech):
        return "done"

    tech.append(request.form.get("technology"))

    # update
    count=conn.execute("""Update coders set technology=%s  where sha2(mail,256)=%s""",[json.dumps(tech),request.form.get("mail")])
    myconn.commit()
    if(count==0):
        return "error"
    else:
        return "done"

# ! add coder projects
@app.route("/addCoderProject", methods=['POST'])
def addCoderProject():

    # check if technolgies are valid and added to coders
    conn.execute("""Select technology from coders where sha2(mail,256)=%s""",[request.form.get("mail")])
    result=conn.fetchall()

    if(result[0]["technology"]==None):
        return "error"
    
    try:
    
        addedTech=json.loads(result[0]["technology"])
        tech=json.loads(request.form.get("technology"))
        print(addedTech,tech)
        if(not set(tech).issubset(addedTech)):
            return "error"

    except:
        return "error"

    # insert
    count=conn.execute("""Insert into projects(id,name,description,technology,cost,coderId) Values(NULL,%s,%s,%s,%s,(Select id from coders where sha2(mail,256)=%s))""",[request.form.get("name"),request.form.get("description"),json.dumps(tech),request.form.get("cost"),request.form.get("mail")])
    myconn.commit()
    if(count==0):
        return "error"
    return "done"

# ! add buyer request
@app.route("/addBuyerRequest", methods=['POST'])
def addBuyerRequest():

    # check if buyer is valid
    conn.execute("""Select verified from buyers where sha2(mail,256)=%s""",[request.form.get("mail")])
    result=conn.fetchall()

    if(len(result)==0 or result[0]["verified"]=="no"):
        return "error"
    
    # check if tehcnologies are valid
    conn.execute("""Select technology from technology """)
    result=conn.fetchall()

    technologies=[]
    for i in result:
        technologies.append(i["technology"])

    try:
        tech=json.loads(request.form.get("technology"))
        print(technologies,tech)
        if(not set(tech).issubset(technologies)):
            return "error"

    except:
        return "error"

    # insert
    count=conn.execute("""Insert into requests(id,name,description,technology,buyerId) Values(NULL,%s,%s,%s,(Select id from buyers where sha2(mail,256)=%s))""",[request.form.get("name"),request.form.get("description"),json.dumps(tech),request.form.get("mail")])
    myconn.commit()
    if(count==0):
        return "error"
    return "done"


# ! coder dashboard
@app.route('/coderDashboard', methods=['POST'])
def coderDashboard():
    conn.execute("""Select
                        (Select count(id) from projects where coderId=(Select id from coders where sha2(mail,256)=%s) and buyerId is not NULL) as completedProjects,
                        (Select count(distinct buyerId) from projects where coderId=(Select id from coders where sha2(mail,256)=%s) and buyerId is not NULL) as uniqueBuyers,
                        coalesce((Select sum(finalCost) from projects where coderId=(Select id from coders where sha2(mail,256)=%s) and buyerId is not NULL),0) as earned,
                    from coders where sha2(mail,256)=%s""",
        [request.form.get("mail"),request.form.get("mail"),request.form.get("mail"),request.form.get("mail")]
    )
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)

# ! buyer dashboard
@app.route('/buyerDashboard', methods=['POST'])
def buyerDashboard():
    conn.execute("""Select
                        (Select count(id) from projects where buyerId=(Select id from buyers where sha2(mail,256)=%s)) as bids,
                        (Select count(id) from requests where buyerId=(Select id from buyers where sha2(mail,256)=%s)) as requests,
                        coalesce((Select sum(finalCost) from projects where buyerId=(Select id from buyers where sha2(mail,256)=%s)),0) as spent""",
        [request.form.get("mail"),request.form.get("mail"),request.form.get("mail")]
    )
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)

# ! edit coder profile
@app.route('/editCoderProfile', methods=['POST'])
def editCoderProfile():
    count=conn.execute("""Update coders set username=%s where sha2(mail,256)=%s""",[request.form.get("username"),request.form.get("mail")])
    if(count==0):
        return "error"
    return "done"

# ! edit buyer profile
@app.route('/editCoderProfile', methods=['POST'])
def editCoderProfile():
    count=conn.execute("""Update buyers set username=%s,company=%s where sha2(mail,256)=%s""",[request.form.get("username"),request.form.get("company"),request.form.get("mail")])
    if(count==0):
        return "error"
    return "done"


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('connect')
def connect():
    users[request.cookies.get('phone')]=request.sid
    print(users)
    print("user connected : "+request.sid)


@socketio.on('disconnect')
def connect():
    users.pop(request.cookies.get('phone'))
    print("user disconnected")


@socketio.on('send_message')
def send(json, methods=['GET','POST']):
    today = datetime.now()
    if(json['receiver'] in users):
        socketid=users[json['receiver']]
    else:
        socketid=''
    conn.execute("INSERT INTO chat (sname, sender, rname, receiver, message, date, time) VALUES ((SELECT name FROM user WHERE phone='"+json['sender']+"'), '" + json['sender'] + "', (SELECT name FROM user WHERE phone='"+json['receiver']+"'),'" + json['receiver'] + "', '" + json['message'] + "','"+today.strftime("%d/%m/%Y")+"', '"+today.strftime('%I:%M %p')+"')")
    myconn.commit()
    json['date']=today.strftime("%d/%m/%Y")
    json['time']=today.strftime("%I:%M %p")
    print(json)
    socketio.emit('new_message',json,room=socketid)




@socketio.on('user_connected')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('user connected ' + str(json))
    # users[str(json)]=request.sid
    # print(users)
    socketio.emit('user_connected', str(json), callback=messageReceived)

@app.route('/all_users', methods=['POST'])
def postJsonHandler():
    if request.method=="POST":
        phone=request.form.get('phone')
        # print(phone)
        conn.execute("SELECT id,name,phone From user WHERE NOT phone='"+phone+"' ORDER BY name ASC")
        result=conn.fetchall()
        print(json.dumps(result))
    return json.dumps(result)


@app.route('/get_name', methods=['POST'])
def get_name():
    if request.method=="POST":
        phone=request.form.get('phone')
        # print(phone)
        conn.execute("SELECT name From user WHERE phone="+phone)
        result=conn.fetchall()
        print(json.dumps(result))
    return json.dumps(result)


@app.route('/chat_history', methods=['POST'])
def chat_history():
    if request.method=="POST":
        conn.execute("SELECT id,name,phone,(select message from chat WHERE (receiver='"+request.form.get('phone')+"' and sender=user.phone) or (sender='"+request.form.get('phone')+"' and receiver=user.phone) order by id desc limit 1) as message,(select id from chat WHERE (receiver='"+request.form.get('phone')+"' and sender=user.phone) or (sender='"+request.form.get('phone')+"' and receiver=user.phone) order by id desc limit 1) as messageid, (select date from chat WHERE (receiver='"+request.form.get('phone')+"' and sender=user.phone) or (sender='"+request.form.get('phone')+"' and receiver=user.phone) order by id desc limit 1) as date, (select time from chat WHERE (receiver='"+request.form.get('phone')+"' and sender=user.phone) or (sender='"+request.form.get('phone')+"' and receiver=user.phone) order by id desc limit 1) as time from user WHERE phone in (SELECT receiver from chat where sender='"+request.form.get('phone')+"') OR phone in (SELECT sender from chat where receiver='"+request.form.get('phone')+"') ORDER BY messageid DESC")
        result=conn.fetchall()
        print(json.dumps(result))
    return json.dumps(result)


@app.route('/get_messages', methods=['POST'])
def get_messages():
    if request.method=="POST":
        conn.execute("SELECT * FROM chat WHERE (sender = '" + request.form.get('sender') + "' AND receiver = '" + request.form.get('receiver') + "') OR (sender = '" + request.form.get('receiver') + "' AND receiver = '" + request.form.get('sender') + "')")
        result=conn.fetchall()
        print(json.dumps(result))
    return json.dumps(result)




if __name__ == '__main__':
    socketio.run(app, debug=True,host="192.168.18.2",port=3000)