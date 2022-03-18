from flask import Flask, render_template,request,jsonify,make_response,redirect
from flask_socketio import SocketIO
import pymysql
import json
from datetime import datetime
import hashlib
import util
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


result = hashlib.sha256("hello@gmail.com".encode())
adminHash=result.hexdigest()





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
    result={}
    val=hashlib.sha256(request.form.get("mail").encode())
    result["id"]= val.hexdigest()
    return json.dumps(result)

# ! Signup for buyers
@app.route("/buyerRegister", methods=['POST'])
def buyerRegister():
    count=conn.execute("""Insert into buyers(id,username,mail,password,company) Values(NULL,%s,%s,sha2(%s,256),%s)""",[request.form.get("username"),request.form.get("mail"),request.form.get("password"),request.form.get("company")])
    myconn.commit()
    print(count)
    if(count==0):
        return "error"
    result={}
    val=hashlib.sha256(request.form.get("mail").encode())
    result["id"]= val.hexdigest()
    return json.dumps(result)

# ! Login for coders
@app.route("/coderValidate", methods=['POST'])
def coderValidate():
    conn.execute("""Select SHA2(mail,256) as id from coders where mail=%s and password=SHA2(%s,256)""",[request.form.get("mail"),request.form.get("password")])
    result=conn.fetchall()
    print(result)
    if(len(result)==0):
        return "error"
    return json.dumps(result[0])

# ! Login for buyers
@app.route("/buyerValidate", methods=['POST'])
def buyerValidate():
    conn.execute("""Select SHA2(mail,256) as id from buyers where mail=%s and password=SHA2(%s,256)""",[request.form.get("mail"),request.form.get("password")])
    result=conn.fetchall()
    print(result)
    if(len(result)==0):
        return "error"
    return json.dumps(result[0])

# ! buyer verification
@app.route("/buyerVerification", methods=['POST'])
def buyerVerification():
    conn.execute("""Select 'verified' from buyers where sha2(mail,256)=%s""",[request.form.get("id")])
    result=conn.fetchall()
    print(result)
    if(len(result)==0):
        return "error"
    return "done"

# ! add technology to coders
"""
@app.route("/addCoderTechnology", methods=['POST'])
def addCoderTechnology():

    # check if tachnology is valid
    # conn.execute(""Select id from technology where technology=%s"",[request.form.get("technology")])
    result=conn.fetchall()

    if(len(result)==0):
        return "error"
    
    conn.execute(""Select technology from coders where sha2(mail,256)=%s"",[request.form.get("id")])
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
    count=conn.execute(""Update coders set technology=%s  where sha2(mail,256)=%s"",[json.dumps(tech),request.form.get("id")])
    myconn.commit()
    if(count==0):
        return "error"
    else:
        return "done"
"""

# ! get coder technology list
@app.route('/getCoderTechnologyList', methods=['POST'])
def getCoderTechnologyList():
    conn.execute("""Select sha2(id,256) as id, technology from technology""")
    result=conn.fetchall()
    print(result)
    return json.dumps(result)

# ! add coder projects
@app.route("/addCoderProject", methods=['POST'])
def addCoderProject():
    print("add project")
    # check if technolgies are valid and added to coders
    conn.execute("""Select technology from coders where sha2(mail,256)=%s""",[request.form.get("id")])
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
    count=conn.execute("""Insert into projects(id,name,description,technology,cost,coderId) Values(NULL,%s,%s,%s,%s,(Select id from coders where sha2(mail,256)=%s))""",[request.form.get("name"),request.form.get("description"),json.dumps(tech),request.form.get("cost"),request.form.get("id")])
    myconn.commit()
    if(count==0):
        return "error"
    return "done"

# ! add buyer request
@app.route("/addBuyerRequest", methods=['POST'])
def addBuyerRequest():

    # check if buyer is valid
    conn.execute("""Select verified,username from buyers where sha2(mail,256)=%s""",[request.form.get("id")])
    resultV=conn.fetchall()

    if(len(resultV)==0 or resultV[0]["verified"]=="no"):
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
    count=conn.execute("""Insert into requests(id,name,description,technology,buyerId) Values(NULL,%s,%s,%s,(Select id from buyers where sha2(mail,256)=%s))""",[request.form.get("name"),request.form.get("description"),json.dumps(tech),request.form.get("id")])
    myconn.commit()
    if(count==0):
        return "error"
    
    ids=util.kNN(myconn,json.loads(request.form.get("technology")))
    print(ids)

    header = {"Content-Type": "application/json; charset=utf-8","Authorization": "Basic MmVkNjBmYzctMWM1Mi00NDQwLTgzYWQtODdkOTA4YTk3ZDAw"}

    payload = {"app_id": "94000518-7da5-44a5-a338-7efd79d09099",
            "include_external_user_ids": ids,
            "channel_for_external_user_ids": "push",
            "headings":{"en":"New Buyer Request"},
            "contents": {"en": request.form.get("name")}}
    
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
    print(req.status_code, req.reason)
    return "done"


# ! buyers request list
@app.route('/listBuyersRequests', methods=['POST'])
def listBuyersRequests():
    conn.execute("""SELECT r.id,r.name,r.description,r.technology,b.username,sha2(b.mail,256) as buyerId FROM requests r inner join buyers b on r.buyerId=b.id where TIMESTAMPDIFF(MINUTE,r.adddatetime,now())/60<24;""")
    result=conn.fetchall()
    print(result)
    return json.dumps(result)



# ! coder dashboard
@app.route('/coderDashboard', methods=['POST'])
def coderDashboard():
    conn.execute("""Select username,mail, 
                        (Select count(id) from projects where coderId=(Select id from coders where sha2(mail,256)=%s) and buyerId is not NULL) as completedProjects,
                        (Select count(distinct buyerId) from projects where coderId=(Select id from coders where sha2(mail,256)=%s) and buyerId is not NULL) as uniqueBuyers,
                        coalesce((Select sum(finalCost) from projects where coderId=(Select id from coders where sha2(mail,256)=%s) and buyerId is not NULL),0) as earned
                    from coders where sha2(mail,256)=%s""",
        [request.form.get("id"),request.form.get("id"),request.form.get("id"),request.form.get("id")]
    )
    result=conn.fetchall()
    print(result)
    return json.dumps(result)

# ! buyer dashboard
@app.route('/buyerDashboard', methods=['POST'])
def buyerDashboard():
    conn.execute("""Select
                        (Select count(id) from projects where buyerId=(Select id from buyers where sha2(mail,256)=%s)) as bids,
                        (Select count(id) from requests where buyerId=(Select id from buyers where sha2(mail,256)=%s)) as requests,
                        coalesce((Select sum(amount) from payments where senderId=(Select id from buyers where sha2(mail,256)=%s)),0) as spent""",
        [request.form.get("id"),request.form.get("id"),request.form.get("id")]
    )
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)

# ! buyer profile
@app.route('/buyerProfile', methods=['POST'])
def buyerProfile():
    conn.execute("""Select SHA2(id,256) as id,username,mail,company from buyers where SHA2(mail,256)=%s""",[request.form.get("id")])
    result=conn.fetchall()
    if(len(result)==0):
        return "error"
    return json.dumps(result[0])

# ! coder profile
@app.route('/coderProfile', methods=['POST'])
def coderProfile():
    conn.execute("""Select id,username,mail,technology from (Select sha2(id,256) as id,username,mail from coders where sha2(mail,256)=%s) T1, (SELECT sha2(coderId,256) as coderId,COALESCE(concat('[',GROUP_CONCAT((Select concat('"',technology,'"') from technology where id=technologyId)),']'),'[]') as technology FROM score where coderId=(select id from coders where sha2(mail,256)=%s)) T2;""",[request.form.get("id"),request.form.get("id")])
    result=conn.fetchall()
    print(result)
    if(len(result)==0):
        return "error"
    return json.dumps(result[0])

# ! edit coder profile
@app.route('/editCoderProfile', methods=['POST'])
def editCoderProfile():
    count=conn.execute("""Update coders set username=%s where sha2(mail,256)=%s""",[request.form.get("username"),request.form.get("id")])
    myconn.commit()
    print(conn._last_executed)
    if(count==0):
        return "error"
    return "done"

# ! edit buyer profile
@app.route('/editBuyerProfile', methods=['POST'])
def editBuyerProfile():
    count=conn.execute("""Update buyers set username=%s,company=%s where sha2(mail,256)=%s""",[request.form.get("username"),request.form.get("company"),request.form.get("id")])
    myconn.commit()
    print(count)
    if(count==0):
        return "error"
    return "done"

# ! buyer request history
@app.route('/buyerRequestHistory', methods=['POST'])
def buyerRequestHistory():
    conn.execute("""Select t1.id,t1.name,t1.technology,COALESCE(t2.count,0) as responses from requests t1 left JOIN (Select count(*) as count,requestId from responses group by requestId) t2 on t1.id=t2.requestId where buyerId=(Select id from buyers where SHA2(mail,256)=%s);""",[request.form.get("id")])
    result=conn.fetchall()
    print(result)
    return json.dumps(result)

# ! buyer pay
@app.route('/buyerPay', methods=['POST'])
def buyerPay():
    print("buyerpay")
    count=conn.execute("""Insert into payments(id,amount,senderId,receiverId,description) Values(null,%s,(Select id from buyers where sha2(mail,256)=%s),(Select id from coders where sha2(id,256)=%s),%s)""",[request.form.get("amount"),request.form.get("senderId"),request.form.get("receiverId"),request.form.get("description")])
    myconn.commit()
    print(count)
    if(count==0):
        return "error"
    return "done"

# ! buyer payment history list
@app.route('/buyerPaymentHistory', methods=['POST'])
def buyerPaymentHistory():
    conn.execute("""Select id,amount,(Select username from coders where id=receiverId) as coder,datetime,description from payments where senderId=(Select id from buyers where SHA2(mail,256)=%s) order by datetime desc""",[request.form.get("id")])
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)

# ! coder payment history list
@app.route('/coderPaymentHistory', methods=['POST'])
def coderPaymentHistory():
    conn.execute("""Select p.id as id,p.amount as amount,p.description as description,p.datetime as datetime,b.username as sender from payments p inner join buyers b on p.senderId=b.id where p.receiverId = (Select id from coders where sha2(mail,256)=%s)""",[request.form.get("id")])
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)

# ! coder chat lists
@app.route('/coderChatList', methods=['POST'])
def coderChatList():
    conn.execute("""Select id,(Select concat(COALESCE((Select "You: " from chat where id=T.id and senderType="coder"),''),message) from chat c where id= T.id) as message,(Select datetime from chat c where id= T.id) as datetime,chatWith,chatWithId from (Select max(id) as id,if(strcmp(senderType,"coder")=0,(Select username from buyers where id= receiver),(Select username from buyers where id= sender)) as chatWith,if(strcmp(senderType,"coder")=0,(select sha2(mail,256) from buyers where id=receiver),(select sha2(mail,256) from buyers where id=sender)) as chatWithId from chat where (sender=(Select id from coders where sha2(mail,256)=%s) and senderType="coder") or (receiver=(Select id from coders where sha2(mail,256)=%s) and receiverType="coder")) T group by chatWithId;""",[request.form.get("id"),request.form.get("id")])
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)

# ! buyer chat lists
@app.route('/buyerChatList', methods=['POST'])
def buyerChatList():
    conn.execute("""Select id,(Select concat(COALESCE((Select "You: " from chat where id=T.id and senderType="buyer"),''),message) from chat c where id= T.id) as message,(Select datetime from chat c where id= T.id) as datetime,chatWith,chatWithId from (Select max(id) as id,if(strcmp(senderType,"buyer")=0,(Select username from coders where id= receiver),(Select username from coders where id= sender)) as chatWith,if(strcmp(senderType,"buyer")=0,(select sha2(mail,256) from coders where id=receiver),(select sha2(mail,256) from coders where id=sender)) as chatWithId from chat where (sender=(Select id from buyers where sha2(mail,256)=%s) and senderType="buyer") or (receiver=(Select id from buyers where sha2(mail,256)=%s) and receiverType="buyer")) T group by chatWithId;""",[request.form.get("id"),request.form.get("id")])
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)

# ! add question 
@app.route('/addQuestion', methods=['POST'])
def addQuestion():
    if(str(adminHash)!=request.form.get("mail")):
        return "error"
    options=[(obj["question"],json.dumps(obj["options"]),obj["answer"],obj["technology"]) for obj in json.loads(request.form.get("questions"))]
    print(options)
    count=conn.executemany("""Insert into questions(id,question,options,answer,technologyId) Values(NULL,%s,%s,%s,(Select id from technology where technology=%s))""",options)
    myconn.commit()
    if(count==0):
        return "error"
    return "done"

# ! coder exam 
@app.route('/coderExam', methods=['POST'])
def coderExam():
    conn.execute("""Select sha2(id,256) as id, question, optionList from questions q inner join (Select questionId,concat('[',GROUP_CONCAT(concat('"',optionText,'"')),']') as optionList from options group by questionId) o on q.id=o.questionId where sha2(technologyId,256)=%s;""",[request.form.get("technologyId")])
    result=conn.fetchall()
    print(result)
    return json.dumps(result)

# ! coder exam submit
@app.route('/coderExamSubmit', methods=['POST'])
def coderExamSubmit():
    conn.execute("""Select sha2(id,256) as questionId,(Select optionText from options where id= answer) as answer from questions where sha2(technologyId,256)=%s;""",[request.form.get("technologyId")])
    result=conn.fetchall()
    print(result)
    exam=json.loads(request.form.get("answers"))
    mark=0
    for options in exam:
        if options in result:
            mark+=1
    print(exam)
    score=mark/len(exam)*100
    if(score>=60):
        count=conn.execute("""Insert into score(id,technologyId,score,coderId) values(null,(Select id from technology where sha2(id,256)=%s),%s,(Select id from coders where sha2(mail,256)=%s))""",[request.form.get("technologyId"),score,request.form.get("id")])
        myconn.commit()
        if(count==0):
            return "error"
        conn.execute("""Select c.technology as technology,t.technology as name from coders c,technology t where sha2(c.mail,256)=%s and sha2(t.id,256)=%s""",[request.form.get("id"),request.form.get("technologyId")])
        result=conn.fetchone()
        result["technology"]=json.loads(result["technology"])
        print(result)
        result["technology"].append(result["name"])
        print(result["technology"])
        count=conn.execute("""Update coders set technology=%s where sha2(mail,256)=%s""",[json.dumps(result["technology"]),request.form.get("id")])
        myconn.commit()
        return json.dumps({"score":mark/len(exam)*100})


# ! coder result 
@app.route('/coderResult', methods=['POST'])
def coderResult():
    conn.execute("""Select id, answer, options from questions where technologyId=(Select id from technology where technology=%s) and exists(Select id from coders where sha2(mail,256)=%s)""",[request.form.get("technology"),request.form.get("id")])
    result=conn.fetchall()
    if(len(result)==0):
        return "error"
    options=json.loads(request.form.get("options"))
    score=0
    for obj in result:
        print(options[str(obj["id"])],(obj["answer"]))
        if(options[str(obj["id"])]==(obj["answer"])):
            score+=1
    count=conn.execute("""Insert into score(id,score,technologyId,coderId) Values(NULL,%s,(Select id from technology where technology=%s),(Select id from coders where sha2(mail,256)=%s))""",[score,request.form.get("technology"),request.form.get("id")])
    myconn.commit()
    if(count==0):
        return "error"
    if(score>=0.9*len(result)):
        return json.dumps({"remarks":"pass","score":score})
    
    return json.dumps({"remarks":"fail","score":score})

# ! buyer bid 
@app.route('/buyerBid', methods=['POST'])
def buyerBid():
    count=conn.execute("""
        Insert into bids(id,projectId,buyerId,datetime,amount) Values(NULL,(select id from projects where sha2(id,256)=%s),(Select id from buyers where sha2(mail,256)=%s),now(),%s)
        On duplicate key Update amount=%s, datetime=now()""",
            [request.form.get("projectId"),request.form.get("id"),request.form.get("amount"),request.form.get("amount")])
    myconn.commit()
    if(count==0):
        return "error"
    else:
        return "done"

# ! list of projects for coders
@app.route('/coderProjectList', methods=['POST'])
def coderProjectList():
    conn.execute("""Select sha2(id,256) as id,name,description,technology,timestamp,finalCost,cost,(Select username from buyers where id=buyerId) as buyer,COALESCE((Select max(amount) from bids b where b.projectId=projects.id),0) as largestBid from projects where coderId=(Select id from coders where sha2(mail,256)=%s)""",
            [request.form.get("id")])
    result=conn.fetchall()
    return json.dumps(result,default=str)

# ! list of project bidders for coders
@app.route('/coderProjectBidders', methods=['POST'])
def coderProjectBidders():
    print("bidder")
    conn.execute("""select datetime,amount,(Select username from buyers where id=buyerId) as bidder,( Select sha2(mail,256) from buyers where id=buyerId) as bidderId from bids where sha2(projectId,256)=%s""",
            [request.form.get("id")])
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)


# ! list of coders
@app.route('/codersList', methods=['POST'])
def codersList():
    print(request.form.get("query"))
    conn.execute("""Select sha2(mail,256) as id,username from coders where technology like %s or username like %s""",
            ["%"+request.form.get("query")+"%","%"+request.form.get("query")+"%"])
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)


# ! list of projects for buyers
@app.route('/projectList', methods=['POST'])
def projectList():
    conn.execute("""Select sha2(p.id,256) as id,p.name,p.cost,(select username from coders where coders.id=p.coderId) as coder,coalesce((Select max(amount) from bids where bids.projectId=p.id),0) as highestBid,p.technology,p.description,p.timestamp from projects p where buyerId is NULL""",
            )
    result=conn.fetchall()
    if(len(result)==0):
        return "error"
    else:
        return json.dumps(result,default=str)

# ! buyers bid history
@app.route('/buyerBidHistory', methods=['POST'])
def buyerBidHistory():
    conn.execute("""Select sha2(id,256) as id,sha2(projectId,256) as projectId,(Select name from projects where projects.id=projectId) as name,(Select username from coders where id=(Select coderId from projects where projects.id=projectId)) as coder,amount,Date(datetime) as datetime,coalesce((Select 'Won' from projects where projects.buyerId=buyerId and projects.id=projectId),(Select 'Pending' from projects where buyerId is NULL and projects.id=projectId),'Lost') as status from bids where buyerId=(Select id from buyers where sha2(mail,256)=%s);""",
            [request.form.get("id")])
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)

# ! respond to buyer request
@app.route('/coderRespond', methods=['POST'])
def coderRespond():
    count=conn.execute("""Insert into responses(id,coderId,requestId) values(null,(Select id from coders where sha2(mail,256)=%s),%s)""",[request.form.get("coderId"),request.form.get("requestId")])
    myconn.commit()
    print(conn._last_executed)
    if(count==0):
        return "error"
    return "done"

# ! coder chat history
@app.route('/coderChatHistory', methods=['POST'])
def coderChatHistory():
    conn.execute("""Select if(strcmp(senderType,"coder")=0,"You",(Select sha2(mail,256) from buyers where buyers.id=sender)) as sender,message,datetime as dateTime from chat where (sender=(Select id from coders where sha2(mail,256)=%s) and receiver=(Select id from buyers where sha2(mail,256)=%s)) or (sender = (Select id from buyers where sha2(mail,256)=%s) and receiver = (Select id from coders where sha2(mail,256)=%s));""",
            [request.form.get("id"),request.form.get("chatWithId"),request.form.get("chatWithId"),request.form.get("id")])
    result=conn.fetchall()
    print(result)
    if(len(result)==0):
        return "error"
    else:
        return json.dumps(result,default=str)

# ! buyer chat history
@app.route('/buyerChatHistory', methods=['POST'])
def buyerChatHistory():
    conn.execute("""Select if(strcmp(senderType,"buyer")=0,"You",(Select sha2(mail,256) from coders where coders.id=sender)) as sender,message,datetime as dateTime from chat where (sender=(Select id from buyers where sha2(mail,256)=%s) and receiver=(Select id from coders where sha2(mail,256)=%s)) or (sender = (Select id from coders where sha2(mail,256)=%s) and receiver = (Select id from buyers where sha2(mail,256)=%s));""",
            [request.form.get("id"),request.form.get("chatWithId"),request.form.get("chatWithId"),request.form.get("id")])
    result=conn.fetchall()
    print(result)
    if(len(result)==0):
        return "error"
    else:
        return json.dumps(result,default=str)

# ! coder select bidder
@app.route('/coderSelectBidder', methods=['POST'])
def coderSelectBidder():
    count=conn.execute("""Update projects set finalCost=%s, buyerId=(Select id from buyers where sha2(mail,256)=%s) where sha2(id,256)=%s and coderId=(Select id from coders where sha2(mail,256)=%s)""",[request.form.get("finalCost"),request.form.get("buyerId"),request.form.get("projectId"),request.form.get("id")])
    myconn.commit()
    print(conn._last_executed)
    if(count==0):
        return "error"
    return "done"

# ! buyer request responders
@app.route('/buyerRequestResponders', methods=['POST'])
def buyerRequestResponders():
    conn.execute("""Select (Select username from coders where coders.id=coderId) as username, (Select mail from coders where coders.id=coderId) as mail from responses where requestId=%s""",
            [request.form.get("requestId")])
    result=conn.fetchall()
    return json.dumps(result,default=str)



def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('connect')
def connect():
    print("user connected : "+request.sid)

@socketio.on('userId')
def userId(data):
    users[data["userId"]]=request.sid
    print(users)
    print("userId updated")


@socketio.on('userDisconnection')
def userDisconnection(data):
    users.pop(data["userId"])
    print("user disconnection")


@socketio.on('disconnect')
def disconnect():
    print("user disconnected: "+request.sid)


@socketio.on('sendMessage')
def send(json, methods=['GET','POST']):
    today = datetime.now()
    print(today)
    if(json['receiver'] in users):
        socketid=users[json['receiver']]
    else:
        socketid=''
    print(json["receiver"])
    count=conn.execute("""INSERT INTO chat(id,message,sender,senderType,receiver,receiverType) values(null,%s,if(strcmp(%s,'coder')=0,(Select id from coders where sha2(mail,256)=%s),(Select id from buyers where sha2(mail,256)=%s)),%s,if(strcmp(%s,'coder')=0,(Select id from coders where sha2(mail,256)=%s),(Select id from buyers where sha2(mail,256)=%s)),%s)""",[json["message"],json["senderType"],json["sender"],json["sender"],json["senderType"],json["receiverType"],json["receiver"],json["receiver"],json["receiverType"]])
    myconn.commit()
    print(conn._last_executed)
    json["dateTime"]=str(today)
    conn.execute("""Select if(strcmp(%s,'coder')=0,(Select username from coders where sha2(mail,256)=%s),(Select username from buyers where sha2(mail,256)=%s)) as chatWith""",
            [json["senderType"],json["sender"],json["sender"]])
    result=conn.fetchone()
    print(result)
    json["chatWith"]=result["chatWith"]
    socketio.emit('newMessage',json,room=socketid)


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

@app.route('/admin', methods=['GET'])
def admin():
    if(request.cookies.get("acc")):
        return render_template("index.html")
    return redirect("/adminLogin")

@app.route('/adminLogin', methods=['GET'])
def adminLogin():
    return render_template("login.html")

@app.route('/adminValidate', methods=['POST'])
def adminValidate():
    if(request.form.get("mail")=="123@gmail.com" and request.form.get("password")=="123"):
        response=make_response("done")
        response.set_cookie("acc",hashlib.sha1(request.form.get('mail').encode()).hexdigest())
        return response
    else:
        return "error"


@app.route('/adminHome', methods=['POST'])
def adminHome():
    conn.execute("""SELECT company,(Select count(id) from bids where buyerId in (Select b.id from buyers b where b.company = bc.company)) as bids,(Select count(id) from projects where buyerId in (Select b.id from buyers b where b.company = bc.company)) as bought FROM `buyers` bc group by company;""")
    result=conn.fetchall()
    print(result)
    return json.dumps(result,default=str)


@app.route('/adminCoders', methods=['GET'])
def adminCoders():
    if(request.cookies.get("acc")):
        return render_template("coders.html")
    return redirect("/adminLogin")

@app.route('/adminBuyers', methods=['GET'])
def adminBuyers():
    if(request.cookies.get("acc")):
        return render_template("buyers.html")
    return redirect("/adminLogin")

@app.route('/adminCodersList', methods=['POST'])
def adminCodersList():
    if request.method=="POST":
        conn.execute("""Select username, mail, date, technology, (Select count(id) from projects where coderId=coders.id and not finalCost is NULL) as completedProjects, (Select count(id) from projects where coderId=coders.id) as projects from coders""")
        result=conn.fetchall()
        print(result)
    return json.dumps(result,default=str)

@app.route('/adminBuyersList', methods=['POST'])
def adminBuyersList():
    if request.method=="POST":
        conn.execute("""Select sha2(id,256) as id,username, mail, date, company, verified from buyers""")
        result=conn.fetchall()
        print(result)
    return json.dumps(result,default=str)

@app.route('/adminVerifyBuyer', methods=['POST'])
def adminVerifyBuyer():
    count=conn.execute("""Update buyers set verified='yes' where sha2(id,256)=%s""",[request.form.get("id")])
    myconn.commit()
    if(count==0):
        return "error"
    return "done"


if __name__ == '__main__':
    socketio.run(app, debug=True,host="192.168.18.2",port=3000)