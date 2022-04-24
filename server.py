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
    try:
        count=conn.execute("""Insert ignore into coders(id,username,mail,password) Values(NULL,%s,%s,sha2(%s,256))""",[request.form.get("username"),request.form.get("mail"),request.form.get("password")])
        myconn.commit()
        print(count)
        if(count==0):
            return "duplicate"
        result={}
        val=hashlib.sha256(request.form.get("mail").encode())
        result["id"]= val.hexdigest()
        return json.dumps(result)
    except Exception as e:
        print(e)
        return "error"

# ! Signup for buyers
@app.route("/buyerRegister", methods=['POST'])
def buyerRegister():
    try:
        count=conn.execute("""Insert ignore into buyers(id,username,mail,password,company) Values(NULL,%s,%s,sha2(%s,256),%s)""",[request.form.get("username"),request.form.get("mail"),request.form.get("password"),request.form.get("company")])
        myconn.commit()
        print(count)
        if(count==0):
            return "duplicate"
        result={}
        val=hashlib.sha256(request.form.get("mail").encode())
        result["id"]= val.hexdigest()
        return json.dumps(result)
    except Exception as e:
        print(e)
        return "error"

# ! Login for coders
@app.route("/coderValidate", methods=['POST'])
def coderValidate():
    try:
        conn.execute("""Select SHA2(mail,256) as id from coders where mail=%s and password=SHA2(%s,256)""",[request.form.get("mail"),request.form.get("password")])
        result=conn.fetchall()
        print(result)
        if(len(result)==0):
            return "wrong"
        return json.dumps(result[0])
    except Exception as e:
        print(e)
        return "error"

# ! Login for buyers
@app.route("/buyerValidate", methods=['POST'])
def buyerValidate():
    try:
        conn.execute("""Select SHA2(mail,256) as id from buyers where mail=%s and password=SHA2(%s,256)""",[request.form.get("mail"),request.form.get("password")])
        result=conn.fetchall()
        print(result)
        if(len(result)==0):
            return "wrong"
        return json.dumps(result[0])
    except Exception as e:
            print(e)
            return "error"

# ! buyer verification
@app.route("/buyerVerification", methods=['POST'])
def buyerVerification():
    try:
        conn.execute("""Select 'verified' from buyers where sha2(mail,256)=%s""",[request.form.get("id")])
        result=conn.fetchall()
        print(result)
        if(len(result)==0):
            return "error"
        return "done"
    except Exception as e:
        print(e)
        return "error"

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
    try:
        conn.execute("""Select sha2(id,256) as id, technology from technology""")
        result=conn.fetchall()
        print(result)
        return json.dumps(result)
    except Exception as e:
        print(e)
        return "error"

# ! add coder projects
@app.route("/addCoderProject", methods=['POST'])
def addCoderProject():
    try:
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
    except Exception as e:
        print(e)
        return "error"

# ! add buyer request
@app.route("/addBuyerRequest", methods=['POST'])
def addBuyerRequest():
    try:

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
        print(request.form)
        count=conn.execute("""Insert into requests(id,name,cost,description,technology,buyerId) Values(NULL,%s,%s,%s,%s,(Select id from buyers where sha2(mail,256)=%s))""",[request.form.get("name"),request.form.get("cost"),request.form.get("description"),json.dumps(tech),request.form.get("id")])
        myconn.commit()
        print(count)
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
    except Exception as e:
        print(e)
        return "error"

# ! buyers request list
@app.route('/listBuyersRequests', methods=['POST'])
def listBuyersRequests():
    try:
        conn.execute("""SELECT sha2(r.id,256) as id,r.name,Coalesce((Select min(amount) from responses where requestId=r.id),0) as lowestBid,r.finalCost,r.description,r.cost,r.technology,b.username,sha2(b.mail,256) as buyerId FROM requests r inner join buyers b on r.buyerId=b.id where coderId is null and finalCost is null;""")
        result=conn.fetchall()
        print(result)
        return json.dumps(result)
    except Exception as e:
        print(e)
        return "error"



# ! coder dashboard
@app.route('/coderDashboard', methods=['POST'])
def coderDashboard():
    try:
        conn.execute("""Select username,mail, 
                            (Select count(id) from projects where coderId=(Select id from coders where sha2(mail,256)=%s) and buyerId is not NULL) as completedProjects,
                            (Select count(distinct buyerId) from projects where coderId=(Select id from coders where sha2(mail,256)=%s) and buyerId is not NULL) as uniqueBuyers,
                            coalesce((Select sum(amount)*0.98 from payments where receiverId=(Select id from coders where sha2(mail,256)=%s)),0) as earned
                        from coders where sha2(mail,256)=%s""",
            [request.form.get("id"),request.form.get("id"),request.form.get("id"),request.form.get("id")]
        )
        result=conn.fetchall()
        print(result)
        return json.dumps(result)
    except Exception as e:
        print(e)
        return "error"

# ! buyer dashboard
@app.route('/buyerDashboard', methods=['POST'])
def buyerDashboard():
    try:
        conn.execute("""Select username, mail, 
                            (Select count(id) from projects where buyerId=(Select id from buyers where sha2(mail,256)=%s)) as bids,
                            (Select count(id) from requests where buyerId=(Select id from buyers where sha2(mail,256)=%s)) as requests,
                            coalesce((Select sum(amount) from payments where senderId=(Select id from buyers where sha2(mail,256)=%s)),0) as spent from buyers where sha2(mail,256)=%s""",
            [request.form.get("id"),request.form.get("id"),request.form.get("id"),request.form.get("id")]
        )
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! buyer profile
@app.route('/buyerProfile', methods=['POST'])
def buyerProfile():
    try:
        conn.execute("""Select SHA2(id,256) as id,username,mail,company,verified from buyers where SHA2(mail,256)=%s""",[request.form.get("id")])
        result=conn.fetchall()
        if(len(result)==0):
            return "error"
        return json.dumps(result[0])
    except Exception as e:
        print(e)
        return "error"

# ! coder profile
@app.route('/coderProfile', methods=['POST'])
def coderProfile():
    try:
        conn.execute("""Select id,username,mail,technology from (Select sha2(id,256) as id,username,mail from coders where sha2(mail,256)=%s) T1, (SELECT sha2(coderId,256) as coderId,COALESCE(concat('[',GROUP_CONCAT((Select concat('"',technology,'"') from technology where id=technologyId)),']'),'[]') as technology FROM score where coderId=(select id from coders where sha2(mail,256)=%s)) T2;""",[request.form.get("id"),request.form.get("id")])
        result=conn.fetchall()
        print(result)
        if(len(result)==0):
            return "error"
        return json.dumps(result[0])
    except Exception as e:
        print(e)
        return "error"

# ! edit coder profile
@app.route('/editCoderProfile', methods=['POST'])
def editCoderProfile():
    try:
        count=conn.execute("""Update coders set username=%s where sha2(mail,256)=%s""",[request.form.get("username"),request.form.get("id")])
        myconn.commit()
        print(conn._last_executed)
        if(count==0):
            return "error"
        return "done"
    except Exception as e:
        print(e)
        return "error"

# ! edit buyer profile
@app.route('/editBuyerProfile', methods=['POST'])
def editBuyerProfile():
    try:
        count=conn.execute("""Update buyers set username=%s,company=%s where sha2(mail,256)=%s""",[request.form.get("username"),request.form.get("company"),request.form.get("id")])
        myconn.commit()
        print(count)
        if(count==0):
            return "error"
        return "done"
    except Exception as e:
        print(e)
        return "error"

# ! buyer request history
@app.route('/buyerRequestHistory', methods=['POST'])
def buyerRequestHistory():
    try:
        conn.execute("""Select sha2(t1.id,256) as id,Coalesce((Select 'On Bid' where t1.finalCost is null),'Completed') as status,t1.completeDate,t1.finalCost,t1.adddatetime,t1.name,t1.cost,t1.technology,COALESCE(t2.count,0) as responses from requests t1 left JOIN (Select count(*) as count,requestId from responses group by requestId) t2 on t1.id=t2.requestId where buyerId=(Select id from buyers where SHA2(mail,256)=%s);""",[request.form.get("id")])
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! buyer pay
@app.route('/buyerPay', methods=['POST'])
def buyerPay():
    try:
        print(request.form)
        count=conn.execute("""Insert into payments(id,amount,senderId,receiverId,description) Values(null,%s,(Select id from buyers where sha2(mail,256)=%s),(Select id from coders where sha2(id,256)=%s),%s)""",[request.form.get("amount"),request.form.get("senderId"),request.form.get("receiverId"),request.form.get("description")])
        myconn.commit()
        print(conn._last_executed)
        if(count==0):
            return "error"
        try:
            conn.execute("""Select (Select mail from coders where sha2(id,256)=%s) as mail, (Select username from buyers where sha2(mail,256)=%s) as name""",
                    [request.form.get("receiverId"),request.form.get("senderId")])
            result=conn.fetchone()
            header = {"Content-Type": "application/json; charset=utf-8","Authorization": "Basic MmVkNjBmYzctMWM1Mi00NDQwLTgzYWQtODdkOTA4YTk3ZDAw"}
            payload = {"app_id": "94000518-7da5-44a5-a338-7efd79d09099",
                    "include_external_user_ids": [result["mail"]],
                    "channel_for_external_user_ids": "push",
                    "headings":{"en":"Payment Alert!!!!"},
                    "contents": {"en": "You received a payment of Rs. "+str(float(request.form.get("amount"))*0.98)+" from "+result['name']}}
            
            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
            print(req.status_code, req.reason)
        except Exception as e:
            print(e)
            pass
        return "done"
    except Exception as e:
        print(e)
        return "error"

# ! buyer payment history list
@app.route('/buyerPaymentHistory', methods=['POST'])
def buyerPaymentHistory():
    try:
        conn.execute("""Select t1.id,t1.amount,(Select username from coders where id=t1.receiverId) as coder,t1.datetime,t1.description from payments t1 where senderId=(Select id from buyers where SHA2(mail,256)=%s) order by datetime desc""",[request.form.get("id")])
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! coder payment history list
@app.route('/coderPaymentHistory', methods=['POST'])
def coderPaymentHistory():
    try:
        conn.execute("""Select p.id as id,p.amount*0.98 as amount,p.description as description,p.datetime as datetime,b.username as sender from payments p inner join buyers b on p.senderId=b.id where p.receiverId = (Select id from coders where sha2(mail,256)=%s) order by datetime desc""",[request.form.get("id")])
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! coder chat lists
@app.route('/coderChatList', methods=['POST'])
def coderChatList():
    try:
        conn.execute("""select id,concat(if(strcmp(senderType,"coder")=0,"You: ",""),message) as message, datetime,if(strcmp(senderType,"coder")=0,(Select sha2(mail,256) from buyers where id= receiver),(Select sha2(mail,256) from buyers where id= sender)) as chatWithId, if(strcmp(senderType,"coder")=0,(Select username from buyers where id= receiver),(Select username from buyers where id= sender)) as chatWith from chat where id in (select id from (Select max(id) as id,if(strcmp(senderType,"coder")=0,receiver,sender) as chatWithId from chat where (sender=(select id from coders where sha2(mail,256)=%s) and senderType="coder") or (receiver=(select id from coders where sha2(mail,256)=%s) and receiverType="coder") group by chatWithId) t1) order by datetime desc;""",[request.form.get("id"),request.form.get("id")])
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! buyer chat lists
@app.route('/buyerChatList', methods=['POST'])
def buyerChatList():
    try:
        conn.execute("""select id,concat(if(strcmp(senderType,"buyer")=0,"You: ",""),message) as message, datetime,if(strcmp(senderType,"buyer")=0,(Select sha2(mail,256) from coders where id= receiver),(Select sha2(mail,256) from coders where id= sender)) as chatWithId, if(strcmp(senderType,"buyer")=0,(Select username from coders where id= receiver),(Select username from coders where id= sender)) as chatWith from chat where id in (select id from (Select max(id) as id,if(strcmp(senderType,"buyer")=0,receiver,sender) as chatWithId from chat where (sender=(select id from buyers where sha2(mail,256)=%s) and senderType="buyer") or (receiver=(select id from buyers where sha2(mail,256)=%s) and receiverType="buyer") group by chatWithId) t1) order by datetime desc;""",[request.form.get("id"),request.form.get("id")])
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! add question 
@app.route('/addQuestion', methods=['POST'])
def addQuestion():
    try:
        if(str(adminHash)!=request.form.get("mail")):
            return "error"
        options=[(obj["question"],json.dumps(obj["options"]),obj["answer"],obj["technology"]) for obj in json.loads(request.form.get("questions"))]
        print(options)
        count=conn.executemany("""Insert into questions(id,question,options,answer,technologyId) Values(NULL,%s,%s,%s,(Select id from technology where technology=%s))""",options)
        myconn.commit()
        if(count==0):
            return "error"
        return "done"
    except Exception as e:
        print(e)
        return "error"

# ! coder exam 
@app.route('/coderExam', methods=['POST'])
def coderExam():
    try:
        conn.execute("""Select sha2(id,256) as id, question, optionList from questions q inner join (Select questionId,concat('[',GROUP_CONCAT(concat('"',optionText,'"')),']') as optionList from options group by questionId) o on q.id=o.questionId where sha2(technologyId,256)=%s;""",[request.form.get("technologyId")])
        result=conn.fetchall()
        print(result)
        return json.dumps(result)
    except Exception as e:
        print(e)
        return "error"

# ! coder exam submit
@app.route('/coderExamSubmit', methods=['POST'])
def coderExamSubmit():
    try:
        conn.execute("""Select sha2(id,256) as questionId,(Select optionText from options where options.id= questions.answer) as answer from questions where sha2(technologyId,256)=%s;""",[request.form.get("technologyId")])
        result=conn.fetchall()
        print(result,"hello")
        exam=json.loads(request.form.get("answers"))
        mark=0
        for options in exam:
            try:
                if options in result:
                    mark+=1
            except Exception as e:
                print(e)
        print(exam)
        score=mark/len(exam)*100
        if(score>=60):
            count=conn.execute("""Insert into score(id,technologyId,score,coderId) values(null,(Select id from technology where sha2(id,256)=%s),%s,(Select id from coders where sha2(mail,256)=%s)) On duplicate key Update score=%s""",[request.form.get("technologyId"),score,request.form.get("id"),score])
            myconn.commit()
            if(count==0):
                return "error"
            conn.execute("""Select c.technology as technology,t.technology as name from coders c,technology t where sha2(c.mail,256)=%s and sha2(t.id,256)=%s""",[request.form.get("id"),request.form.get("technologyId")])
            result=conn.fetchone()
            result["technology"]=json.loads(result["technology"])
            print(result)
            if(result["name"] in result["technology"]):
                return json.dumps({"score":mark/len(exam)*100})
            result["technology"].append(result["name"])
            print(result["technology"])
            count=conn.execute("""Update coders set technology=%s where sha2(mail,256)=%s""",[json.dumps(result["technology"]),request.form.get("id")])
            myconn.commit()
            return json.dumps({"score":mark/len(exam)*100})
        else:
            return json.dumps({"score":mark/len(exam)*100})
    except Exception as e:
        print(e)
        return "error"


# ! coder result 
@app.route('/coderResult', methods=['POST'])
def coderResult():
    try:
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
    except Exception as e:
        print(e)
        return "error"

# ! buyer bid 
@app.route('/buyerBid', methods=['POST'])
def buyerBid():
    try:
        count=conn.execute("""
            Insert into bids(id,projectId,buyerId,datetime,amount) Values(NULL,(select id from projects where sha2(id,256)=%s),(Select id from buyers where sha2(mail,256)=%s and verified='yes'),now(),%s)
            On duplicate key Update amount=%s, datetime=now()""",
                [request.form.get("projectId"),request.form.get("id"),request.form.get("amount"),request.form.get("amount")])
        myconn.commit()
        if(count==0):
            return "error"
        else:
            return "done"
    except Exception as e:
        print(e)
        return "error"

# ! list of projects for coders
@app.route('/coderProjectList', methods=['POST'])
def coderProjectList():
    try:
        conn.execute("""Select sha2(id,256) as id,name,description,technology,timestamp,completeDate,finalCost,cost,(Select username from buyers where id=buyerId) as buyer,COALESCE((Select max(amount) from bids b where b.projectId=projects.id),0) as largestBid from projects where coderId=(Select id from coders where sha2(mail,256)=%s)""",
                [request.form.get("id")])
        result=conn.fetchall()
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! list of project bidders for coders
@app.route('/coderProjectBidders', methods=['POST'])
def coderProjectBidders():
    try:
        print("bidder")
        conn.execute("""select datetime,amount,(Select username from buyers where id=buyerId) as bidder,( Select sha2(mail,256) from buyers where id=buyerId) as bidderId from bids where sha2(projectId,256)=%s""",
                [request.form.get("id")])
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! list of request bidders for buyers
@app.route('/buyerRequestBidders', methods=['POST'])
def buyerRequestBidders():
    try:
        print("bidder")
        conn.execute("""select datetime,amount,(Select username from coders where id=coderId) as bidder,( Select sha2(mail,256) from coders where id=coderId) as bidderId from responses where sha2(requestId,256)=%s""",
                [request.form.get("id")])
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"


# ! list of coders
@app.route('/codersList', methods=['POST'])
def codersList():
    try:
        print(request.form.get("query"))
        conn.execute("""Select sha2(mail,256) as id,username from coders where technology like %s or username like %s""",
                ["%"+request.form.get("query")+"%","%"+request.form.get("query")+"%"])
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"


# ! list of projects for buyers
@app.route('/projectList', methods=['POST'])
def projectList():
    try:
        conn.execute("""Select sha2(p.id,256) as id,p.name,p.cost,(select username from coders where coders.id=p.coderId) as coder,coalesce((Select max(amount) from bids where bids.projectId=p.id),0) as highestBid,p.technology,p.description,p.timestamp from projects p where buyerId is NULL""",
                )
        result=conn.fetchall()
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! buyers bid history
@app.route('/buyerBidHistory', methods=['POST'])
def buyerBidHistory():
    try:
        conn.execute("""Select sha2(id,256) as id,sha2(projectId,256) as projectId,(Select name from projects where projects.id=projectId) as name,(Select completeDate from projects where projects.id=projectId) as completeDate,(Select username from coders where id=(Select coderId from projects where projects.id=projectId)) as coder,(Select sha2(id,256) from coders where id=(Select coderId from projects where projects.id=projectId)) as coderId,amount,Date(datetime) as datetime,coalesce((Select 'Won' from projects where projects.buyerId=buyerId and projects.id=projectId),(Select 'Pending' from projects where buyerId is NULL and projects.id=projectId),'Lost') as status from bids where buyerId=(Select id from buyers where sha2(mail,256)=%s);""",
                [request.form.get("id")])
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! coder response history
@app.route('/coderResponseHistory', methods=['POST'])
def coderResponseHistory():
    try:
        conn.execute("""Select sha2(id,256) as id,sha2(requestId,256) as requestId,(Select name from requests where requests.id=requestId) as name,(Select completeDate from requests where requests.id=requestId) as completeDate,(Select username from buyers where id=(Select buyerId from requests where requests.id=requestId)) as buyer,(Select sha2(coderId,256) from requests where requests.id=requestId) as buyerId,amount,Date(datetime) as datetime,coalesce((Select 'Won' from requests where requests.coderId=coderId and requests.id=requestId),(Select 'Pending' from requests where coderId is NULL and requests.id=requestId),'Lost') as status from responses where coderId=(Select id from coders where sha2(mail,256)=%s);""",
                [request.form.get("id")])
        result=conn.fetchall()
        print(result)
        print(conn._last_executed)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        print(conn._last_executed)
        return "error"

# ! respond to buyer request
@app.route('/coderRespond', methods=['POST'])
def coderRespond():
    print(request.form)
    try:
        conn.execute("""Select technology,(select technology from requests where sha2(id,256)=%s) as techRequired from coders where sha2(mail,256)=%s""",[request.form.get("requestId"),request.form.get("coderId")])
        result=conn.fetchone()
        tech=json.loads(result["technology"])
        techRequired = json.loads(result["techRequired"])

        if(not set(techRequired).issubset(tech)):
            print("hello")
            return "error"

        count=conn.execute("""Insert into responses(id,requestId,coderId,amount) Values(NULL,(select id from requests where sha2(id,256)=%s),(Select id from coders where sha2(mail,256)=%s),%s)
            On duplicate key Update amount=%s, datetime=now()""",[request.form.get("requestId"),request.form.get("coderId"),request.form.get("amount"),request.form.get("amount")])
        myconn.commit()
        print(conn._last_executed)
        if(count==0):
            return "error"
        return "done"
    except Exception as e:
        print(e)
        return "error"

# ! coder chat history
@app.route('/coderChatHistory', methods=['POST'])
def coderChatHistory():
    try:
        conn.execute("""Select if(strcmp(senderType,"coder")=0,"You",(Select sha2(mail,256) from buyers where buyers.id=sender)) as sender,message,datetime as dateTime from chat where (sender=(Select id from coders where sha2(mail,256)=%s) and receiver=(Select id from buyers where sha2(mail,256)=%s)) or (sender = (Select id from buyers where sha2(mail,256)=%s) and receiver = (Select id from coders where sha2(mail,256)=%s));""",
                [request.form.get("id"),request.form.get("chatWithId"),request.form.get("chatWithId"),request.form.get("id")])
        result=conn.fetchall()
        print(result)
        if(len(result)==0):
            return "error"
        else:
            return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! buyer chat history
@app.route('/buyerChatHistory', methods=['POST'])
def buyerChatHistory():
    try:
        conn.execute("""Select if(strcmp(senderType,"buyer")=0,"You",(Select sha2(mail,256) from coders where coders.id=sender)) as sender,message,datetime as dateTime from chat where (sender=(Select id from buyers where sha2(mail,256)=%s) and receiver=(Select id from coders where sha2(mail,256)=%s)) or (sender = (Select id from coders where sha2(mail,256)=%s) and receiver = (Select id from buyers where sha2(mail,256)=%s));""",
                [request.form.get("id"),request.form.get("chatWithId"),request.form.get("chatWithId"),request.form.get("id")])
        result=conn.fetchall()
        if(len(result)==0):
            return "error"
        else:
            return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! coder select bidder
@app.route('/coderSelectBidder', methods=['POST'])
def coderSelectBidder():
    try:
        count=conn.execute("""Update projects set finalCost=%s, buyerId=(Select id from buyers where sha2(mail,256)=%s), completeDate=now() where sha2(id,256)=%s and coderId=(Select id from coders where sha2(mail,256)=%s)""",[request.form.get("finalCost"),request.form.get("buyerId"),request.form.get("projectId"),request.form.get("id")])
        myconn.commit()
        print(conn._last_executed)
        if(count==0):
            return "error"
        try:
            conn.execute("""Select mail,(Select name from projects where sha2(id,256)=%s) as project from buyers where sha2(mail,256)=%s""",
                    [request.form.get("projectId"),request.form.get("buyerId")])
            result=conn.fetchone()
            header = {"Content-Type": "application/json; charset=utf-8","Authorization": "Basic MmVkNjBmYzctMWM1Mi00NDQwLTgzYWQtODdkOTA4YTk3ZDAw"}

            payload = {"app_id": "94000518-7da5-44a5-a338-7efd79d09099",
                    "include_external_user_ids": [result["mail"]],
                    "channel_for_external_user_ids": "push",
                    "headings":{"en":"Congratulations"},
                    "contents": {"en": "You won a Bid!!"}}
            
            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
            print(req.status_code, req.reason)

            # send message to buyer
            today = datetime.now()
            print(today)
            chatMessage={"receiver":request.form.get("buyerId"),
                    "sender":request.form.get("id"),
                    "message":"You won the bid for "+result["project"],
                    "senderType":"coder",
                    "receiverType":"buyer"}
            if(chatMessage['receiver'] in users):
                socketid=users[chatMessage['receiver']]
            else:
                socketid=''
            print(chatMessage["receiver"])
            count=conn.execute("""INSERT INTO chat(id,message,sender,senderType,receiver,receiverType) values(null,%s,if(strcmp(%s,'coder')=0,(Select id from coders where sha2(mail,256)=%s),(Select id from buyers where sha2(mail,256)=%s)),%s,if(strcmp(%s,'coder')=0,(Select id from coders where sha2(mail,256)=%s),(Select id from buyers where sha2(mail,256)=%s)),%s)""",[chatMessage["message"],chatMessage["senderType"],chatMessage["sender"],chatMessage["sender"],chatMessage["senderType"],chatMessage["receiverType"],chatMessage["receiver"],chatMessage["receiver"],chatMessage["receiverType"]])
            myconn.commit()
            print(conn._last_executed)
            chatMessage["dateTime"]=str(today)
            conn.execute("""Select if(strcmp(%s,'coder')=0,(Select username from coders where sha2(mail,256)=%s),(Select username from buyers where sha2(mail,256)=%s)) as chatWith""",
                    [chatMessage["senderType"],chatMessage["sender"],chatMessage["sender"]])
            result=conn.fetchone()
            print(result)
            chatMessage["chatWith"]=result["chatWith"]
            socketio.emit('newMessage',chatMessage,room=socketid)

        except Exception as e:
            print(e)
            pass
    except Exception as e:
        print(e)
        return "error"

    return "done"

# ! buyer select bidder
@app.route('/buyerSelectBidder', methods=['POST'])
def buyerSelectBidder():
    try:
        count=conn.execute("""Update requests set finalCost=%s, coderId=(Select id from coders where sha2(mail,256)=%s), completeDate=now() where sha2(id,256)=%s and buyerId=(Select id from buyers where sha2(mail,256)=%s)""",[request.form.get("finalCost"),request.form.get("coderId"),request.form.get("requestId"),request.form.get("id")])
        myconn.commit()
        print(conn._last_executed)
        if(count==0):
            return "error"
        try:
            conn.execute("""Select mail,(Select name from requests where sha2(id,256)=%s) as request from coders where sha2(mail,256)=%s""",
                    [request.form.get("requestId"),request.form.get("coderId")])
            result=conn.fetchone()
            header = {"Content-Type": "application/json; charset=utf-8","Authorization": "Basic MmVkNjBmYzctMWM1Mi00NDQwLTgzYWQtODdkOTA4YTk3ZDAw"}

            payload = {"app_id": "94000518-7da5-44a5-a338-7efd79d09099",
                    "include_external_user_ids": [result["mail"]],
                    "channel_for_external_user_ids": "push",
                    "headings":{"en":"Congratulations"},
                    "contents": {"en": "You won a Bid!!"}}
            
            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
            print(req.status_code, req.reason)

            # send message to buyer
            today = datetime.now()
            print(today)
            chatMessage={"receiver":request.form.get("coderId"),
                    "sender":request.form.get("id"),
                    "message":"You won the bid for "+result["request"],
                    "senderType":"buyer",
                    "receiverType":"coder"}
            if(chatMessage['receiver'] in users):
                socketid=users[chatMessage['receiver']]
            else:
                socketid=''
            print(chatMessage["receiver"])
            count=conn.execute("""INSERT INTO chat(id,message,sender,senderType,receiver,receiverType) values(null,%s,if(strcmp(%s,'coder')=0,(Select id from coders where sha2(mail,256)=%s),(Select id from buyers where sha2(mail,256)=%s)),%s,if(strcmp(%s,'coder')=0,(Select id from coders where sha2(mail,256)=%s),(Select id from buyers where sha2(mail,256)=%s)),%s)""",[chatMessage["message"],chatMessage["senderType"],chatMessage["sender"],chatMessage["sender"],chatMessage["senderType"],chatMessage["receiverType"],chatMessage["receiver"],chatMessage["receiver"],chatMessage["receiverType"]])
            myconn.commit()
            print(conn._last_executed)
            chatMessage["dateTime"]=str(today)
            conn.execute("""Select if(strcmp(%s,'coder')=0,(Select username from coders where sha2(mail,256)=%s),(Select username from buyers where sha2(mail,256)=%s)) as chatWith""",
                    [chatMessage["senderType"],chatMessage["sender"],chatMessage["sender"]])
            result=conn.fetchone()
            print(result)
            chatMessage["chatWith"]=result["chatWith"]
            socketio.emit('newMessage',chatMessage,room=socketid)

        except Exception as e:
            print(e)
            pass
    except Exception as e:
        print(e)
        return "error"

    return "done"

# ! buyer request responders
@app.route('/buyerRequestResponders', methods=['POST'])
def buyerRequestResponders():
    try:
        conn.execute("""Select (Select username from coders where coders.id=coderId) as username, (Select mail from coders where coders.id=coderId) as mail from responses where requestId=%s""",
                [request.form.get("requestId")])
        result=conn.fetchall()
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! coder tech info
@app.route('/coderTechInfo', methods=['POST'])
def coderTechInfo():
    try:
        conn.execute("""Select sha2(id,256) as id, Coalesce((Select score from score where score.coderId=(select id from coders where sha2(mail,256)=%s) and score.technologyId=technology.id),0) as score from technology where technology=%s""",
                [request.form.get("id"),request.form.get("technology")])
        result=conn.fetchone()
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! buyer view coder profile
@app.route('/viewCoderProfile', methods=['POST'])
def viewCoderProfile():
    try:
        conn.execute("""Select sha2(id,256) as id, username,mail,technology, coalesce((select count(id) from projects where not finalCost is null and projects.coderId=coders.id),0) as completed,Coalesce((select count(id) from projects where projects.coderId=coders.id),0) as projects from coders where sha2(mail,256)=%s""",
                [request.form.get("id")])
        result=conn.fetchone()
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! buyer reset password
@app.route('/buyerPasswordReset', methods=['POST'])
def buyerPasswordReset():
    try:
        count=conn.execute("""Update buyers set `password`=sha2(%s,256) where sha2(mail,256)=%s and sha2(%s,256)=password""",[request.form.get("newPassword"),request.form.get("id"),request.form.get("password")])
        myconn.commit()
        print(conn._last_executed)
        if(count==0):
            return "error"
        return "done"
    except Exception as e:
        print(e)
        return "error"

# ! coder reset password
@app.route('/coderPasswordReset', methods=['POST'])
def coderPasswordReset():
    try:
        count=conn.execute("""Update coders set `password`=sha2(%s,256) where sha2(mail,256)=%s and sha2(%s,256)=password""",[request.form.get("newPassword"),request.form.get("id"),request.form.get("password")])
        myconn.commit()
        print(conn._last_executed)
        if(count==0):
            return "error"
        return "done"
    except Exception as e:
        print(e)
        return "error"

# ! technology List
@app.route('/getTechnologyList', methods=['POST'])
def getTechnologyList():
    try:
        conn.execute("""Select technology from technology""")
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

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
    try:
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
    except Exception as e:
        print(e)
        return "error"


@app.route('/all_users', methods=['POST'])
def postJsonHandler():
    try:
        if request.method=="POST":
            phone=request.form.get('phone')
            # print(phone)
            conn.execute("SELECT id,name,phone From user WHERE NOT phone='"+phone+"' ORDER BY name ASC")
            result=conn.fetchall()
            print(json.dumps(result))
        return json.dumps(result)
    except Exception as e:
        print(e)
        return "error"


@app.route('/get_name', methods=['POST'])
def get_name():
    try:
        if request.method=="POST":
            phone=request.form.get('phone')
            # print(phone)
            conn.execute("SELECT name From user WHERE phone="+phone)
            result=conn.fetchall()
            print(json.dumps(result))
        return json.dumps(result)
    except Exception as e:
        print(e)
        return "error"


@app.route('/chat_history', methods=['POST'])
def chat_history():
    try:
        if request.method=="POST":
            conn.execute("SELECT id,name,phone,(select message from chat WHERE (receiver='"+request.form.get('phone')+"' and sender=user.phone) or (sender='"+request.form.get('phone')+"' and receiver=user.phone) order by id desc limit 1) as message,(select id from chat WHERE (receiver='"+request.form.get('phone')+"' and sender=user.phone) or (sender='"+request.form.get('phone')+"' and receiver=user.phone) order by id desc limit 1) as messageid, (select date from chat WHERE (receiver='"+request.form.get('phone')+"' and sender=user.phone) or (sender='"+request.form.get('phone')+"' and receiver=user.phone) order by id desc limit 1) as date, (select time from chat WHERE (receiver='"+request.form.get('phone')+"' and sender=user.phone) or (sender='"+request.form.get('phone')+"' and receiver=user.phone) order by id desc limit 1) as time from user WHERE phone in (SELECT receiver from chat where sender='"+request.form.get('phone')+"') OR phone in (SELECT sender from chat where receiver='"+request.form.get('phone')+"') ORDER BY messageid DESC")
            result=conn.fetchall()
            print(json.dumps(result))
        return json.dumps(result)
    except Exception as e:
        print(e)
        return "error"


@app.route('/get_messages', methods=['POST'])
def get_messages():
    try:
        if request.method=="POST":
            conn.execute("SELECT * FROM chat WHERE (sender = '" + request.form.get('sender') + "' AND receiver = '" + request.form.get('receiver') + "') OR (sender = '" + request.form.get('receiver') + "' AND receiver = '" + request.form.get('sender') + "')")
            result=conn.fetchall()
            print(json.dumps(result))
        return json.dumps(result)
    except Exception as e:
        print(e)
        return "error"

# ! admin dashboard
@app.route('/admin', methods=['GET'])
def admin():
    try:
        if(request.cookies.get("acc")):
            return render_template("index.html")
        return redirect("/adminLogin")
    except Exception as e:
        print(e)
        return "error"

# ! admin login
@app.route('/adminLogin', methods=['GET'])
def adminLogin():
    try:
        return render_template("login.html")
    except Exception as e:
        print(e)
        return "error"

# ! admin login validation
@app.route('/adminValidate', methods=['POST'])
def adminValidate():
    try:
        if(request.form.get("mail")=="123@gmail.com" and request.form.get("password")=="123"):
            response=make_response("done")
            response.set_cookie("acc",hashlib.sha1(request.form.get('mail').encode()).hexdigest())
            return response
        else:
            return "error"
    except Exception as e:
        print(e)
        return "error"

# ! admin home page info
@app.route('/adminHome', methods=['POST'])
def adminHome():
    try:
        conn.execute("""SELECT company,(Select count(id) from bids where buyerId in (Select b.id from buyers b where b.company = bc.company)) as bids,(Select count(id) from projects where buyerId in (Select b.id from buyers b where b.company = bc.company)) as bought FROM `buyers` bc group by company;""")
        result=conn.fetchall()
        print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! admin coders page
@app.route('/adminCoders', methods=['GET'])
def adminCoders():
    try:
        if(request.cookies.get("acc")):
            return render_template("coders.html")
        return redirect("/adminLogin")
    except Exception as e:
        print(e)
        return "error"

# ! admin buyers page
@app.route('/adminBuyers', methods=['GET'])
def adminBuyers():
    try:
        if(request.cookies.get("acc")):
            return render_template("buyers.html")
        return redirect("/adminLogin")
    except Exception as e:
        print(e)
        return "error"

# ! admin payment page
@app.route('/adminPayments', methods=['GET'])
def adminPayments():
    try:
        if(request.cookies.get("acc")):
            return render_template("payments.html")
        return redirect("/adminLogin")
    except Exception as e:
        print(e)
        return "error"

# ! admin technology page
@app.route('/adminTechnology', methods=['GET'])
def adminTechnology():
    try:
        if(request.cookies.get("acc")):
            return render_template("technology.html")
        return redirect("/adminLogin")
    except Exception as e:
        print(e)
        return "error"

# ! admin technology page
@app.route('/adminAddTechnology', methods=['GET'])
def adminAddTechnology():
    try:
        if(request.cookies.get("acc")):
            return render_template("addTechnology.html")
        return redirect("/adminLogin")
    except Exception as e:
        print(e)
        return "error"

# ! admin coders List
@app.route('/adminCodersList', methods=['POST'])
def adminCodersList():
    try:
        if request.method=="POST":
            conn.execute("""Select username, mail, date, technology, (Select count(id) from projects where coderId=coders.id and not finalCost is NULL) as completedProjects, (Select count(id) from projects where coderId=coders.id) as projects from coders""")
            result=conn.fetchall()
            print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! admin buyers list
@app.route('/adminBuyersList', methods=['POST'])
def adminBuyersList():
    try:
        if request.method=="POST":
            conn.execute("""Select sha2(id,256) as id,username, mail, date, company, verified from buyers""")
            result=conn.fetchall()
            print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! admin verify buyers
@app.route('/adminVerifyBuyer', methods=['POST'])
def adminVerifyBuyer():
    try:
        count=conn.execute("""Update buyers set verified='yes' where sha2(id,256)=%s""",[request.form.get("id")])
        myconn.commit()
        if(count==0):
            return "error"
        try:
            conn.execute("""Select mail from buyers where sha2(id,256)=%s""",
                    [request.form.get("id")])
            result=conn.fetchone()
            header = {"Content-Type": "application/json; charset=utf-8","Authorization": "Basic MmVkNjBmYzctMWM1Mi00NDQwLTgzYWQtODdkOTA4YTk3ZDAw"}

            payload = {"app_id": "94000518-7da5-44a5-a338-7efd79d09099",
                    "include_external_user_ids": [result["mail"]],
                    "channel_for_external_user_ids": "push",
                    "headings":{"en":"Congratulations"},
                    "contents": {"en": "You have been verified"}}
            
            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
            print(req.status_code, req.reason)
        except Exception as e:
            print(e)
        return "done"
    except Exception as e:
        print(e)
        return "error"

# ! admin buyers list
@app.route('/adminPaymentsList', methods=['POST'])
def adminPaymentsList():
    try:
        if request.method=="POST":
            conn.execute("""Select amount*0.02 as amount, (Select username from buyers where id=senderId) as 'from', (Select username from coders where id=receiverId) as 'to', DATE_FORMAT(datetime,'%c/%e/%Y') as date, DATE_FORMAT(datetime,'%r') as time, description from payments""")
            result=conn.fetchall()
            print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! admin technology list
@app.route('/adminTechnologyList', methods=['POST','GET'])
def adminTechnologyList():
    try:
        if request.method=="POST" or request.method=="GET":
            conn.execute("""Select sha2(id,256) as id, technology from technology""")
            result=conn.fetchall()
            print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! admin technology question
@app.route('/adminTechnologyQuestion', methods=['POST','GET'])
def adminTechnologyQuestion():
    try:
        if request.method=="POST" or request.method=="GET":
            conn.execute("""Select question, (select GROUP_CONCAT(optionText) from options where questionId=questions.id) as options, (select optionText from options where id=questions.answer) as answer from questions where sha2(technologyId,256)=%s""",[request.form.get("id")])
            result=conn.fetchall()
            print(result)
        return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# ! admin add technology question
@app.route('/adminAddNewTechnology', methods=['POST','GET'])
def adminAddNewTechnology():
    try:
        if request.method=="POST" or request.method=="GET":
            print(request.form)
            count=conn.execute("""Insert into technology(id,technology) values(null,%s)""",[request.form.get("technology")])
            techId=myconn.insert_id()
            print(techId)
            if count!=0:
                for i in range(5):
                    count1=conn.execute("""Insert into questions(id,question,answer,technologyId) values(null,%s,0,%s)""",[request.form.get("question"+str(i+1)),techId])
                    id=myconn.insert_id()
                    if(count1==0):
                        myconn.rollback()
                        return "error"
                    count1=conn.execute("""Insert into options(id,optionText,questionId) values(null,%s,%s), (null,%s,%s), (null,%s,%s) ,(null,%s,%s)""",[request.form.getlist("option"+str(i+1)+"[]")[0],id,request.form.getlist("option"+str(i+1)+"[]")[1],id,request.form.getlist("option"+str(i+1)+"[]")[2],id,request.form.getlist("option"+str(i+1)+"[]")[3],id])
                    myconn.commit()
                    if(count1==0):
                        myconn.rollback()
                        return "error"
                    count1=conn.execute("""Update questions set answer=(select id from options where optionText=%s and questionId=%s) where id=%s""",[request.form.getlist("option"+str(i+1)+"[]")[int(request.form.get("answer"+str(i+1)))],id,id])
                    if(count1==0):
                        myconn.rollback()
                        return "error"
                myconn.commit()
                return "done"
            else:
                myconn.rollback()
                return "error"
    except Exception as e:
        print(e)
        return "error"

if __name__ == '__main__':
    socketio.run(app, debug=True,host="192.168.18.46",port=3000)