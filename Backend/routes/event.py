from fastapi import APIRouter,HTTPException
from config.db import conn
from model.event import *
from schemas.event import serializeDict,serializeList
from bson import ObjectId
import re


event = APIRouter()

@event.get("/")
async def home():
    return {"message": "Welcome to the home page"}

# Routes For Admin ------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>

# Get all Organization
@event.get("/getallorganization")
async def find_all_organization():
    return serializeList(conn.event.organization.find())

# Get one Organization by ID
@event.get("/organization/{id}")
async def find_one_organizaton(id):
    return serializeDict(conn.event.organization.find_one({"_id":ObjectId(id)}))



# Routes for Organization ------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>

# Get all Members of Organization by Clubname
@event.post("/organizationmember/")
async def organization_member(data : dict):
    org = conn.event.organization.find({"clubname" : data["clubname"]})
    if org:
        data_dict = serializeList(org)[0]["members"]
        for i in data_dict:
            i["expiry_date"] = i["expiry_date"].strftime("%Y-%m-%d")
            i["start_date"] = i["start_date"].strftime("%Y-%m-%d")
        return data_dict
    else:
        return {"error":"Member doesn't Exist","success":False}

# Signup for Organizaton
@event.post("/organisationsignup/")
async def create_organization(organization:Organization):
    conn.event.organization.insert_one(dict(organization))
    return dict(organization)

# Login for Organization
@event.post("/organisationlogin/")
async def organization_login(data : dict):
    d1 = conn.event.organization.find_one({"username":data["username"]})
    if d1 and d1["pwd"] == data["pwd"]:
        return serializeDict(d1)
    else:
        return {"error":"Invalid Username and Password","success":False}

# Get all Membership Type (Only Type Name) by Clubname
@event.post("/getmemtype/")
async def get_memtype(data:dict):
    type = []
    cursor = conn.event.organization.find({"clubname":data["clubname"]}, {"memtype": 1, "_id": 0})
    # print(serializeList(cursor))
    d1 = serializeList(cursor)
    # print(d1[0]["memtype"])
    for i in d1[0]["memtype"]:
        type.append(i["type"])
    return type

# Sorting of Member list by Parameters
@event.post("/membersorting")
async def member_sorting(data:dict):
    org = conn.event.organization.find_one({"clubname" : data["clubname"]})
    if org:
        org1 =  serializeDict(org)["members"]
        if len(org1) != 0:
        # print(org1)
            if data["value"]:
                sorted_list = sorted(org1, key=lambda x: x[data["col"]])
                for i in sorted_list:
                    i["expiry_date"] = i["expiry_date"].strftime("%Y-%m-%d")
                    i["start_date"] = i["start_date"].strftime("%Y-%m-%d")
                return sorted_list
            else:
                sorted_list = sorted(org1, key=lambda x: x[data["col"]], reverse=True)
                for i in sorted_list:
                    i["expiry_date"] = i["expiry_date"].strftime("%Y-%m-%d")
                    i["start_date"] = i["start_date"].strftime("%Y-%m-%d")
                return sorted_list

    else:
        return {"error":"Organization not Found","success":False}

# Add Member in Organization
@event.put("/addorganizationmember/{id}")
async def add_member(id:str,member:User):
    data_dict = dict(member)
    org = conn.event.organization.find({"_id":ObjectId(id)})
    if org:
        data_dict1 = serializeList(org)[0]["members"]
        for i in data_dict1:
            if (i["username"] == data_dict["username"]):
                return {"data":"Username already Exists","success":False}
            if (i["memberid"] == data_dict["memberid"]):
                return {"data":"Member ID already Exists","success":False}
    if data_dict["membertype"] == '':
        return {"data":"Select Membership Type","success":False}
    del data_dict["clubname"]
    data_dict["expiry_date"] = data_dict["expiry_date"].strftime("%Y-%m-%d")
    data_dict["expiry_date"] = datetime.strptime(data_dict["expiry_date"], "%Y-%m-%d")
    data_dict["start_date"] = data_dict["start_date"].strftime("%Y-%m-%d")
    data_dict["start_date"] = datetime.strptime(data_dict["start_date"], "%Y-%m-%d")
    d1 = conn.event.organization.find_one({"_id":ObjectId(id)})
    if d1:
        # serializeDict(d1)["members"].append(data_dict)
        org1 = serializeDict(d1)
        org1["members"].append(data_dict)
        conn.event.organization.find_one_and_update({"_id":ObjectId(id)},{"$set": {"members":org1["members"]}})
        return {"data":"Member Added Successfully","success":True}
    else:
        return {"error":"Invalid Input","success":False}

# Update Member Details in Organization
@event.put("/organizationupdatememberdetails/")   
async def update_member_details(data: dict):
    organisation = conn.event.organization.find_one({"clubname": data["clubname"]})
    if organisation:   
        
        org1 = serializeDict(organisation)
        # formdata = data["formData"]
        
        data["formData"]["expiry_date"] = datetime.strptime(data["formData"]["expiry_date"], "%Y-%m-%d")
        data["formData"]["start_date"] = datetime.strptime(data["formData"]["start_date"], "%Y-%m-%d")
        # member_id = data["memberId"]
        # print(member_id)
        for memberdict in org1["members"]:
            # print(memberdict["memberid"])
            if memberdict["memberid"] == data["memberId"]:
                memberdict.update(data["formData"])
                # print(org1["members"])
                conn.event.organization.find_one_and_update({"_id":ObjectId(org1["_id"])},{"$set": {"members":org1["members"]}})
                # print(org1["members"])
                return True
    else:
        return {"error":"Organisation not found","success": False}

# Delete Member from Organization
@event.put("/deletemember")
async def delete_member(data : dict):
    org = conn.event.organization.find_one({"_id":ObjectId(data['orgid'])})
    if org:
        org1 = serializeDict(org)
        clubname = org1["clubname"]
        org1 = serializeDict(org)["members"]
        for i in org1:
            if i["memberid"] == data["memberid"]:
                i["clubname"] = clubname
                conn.event.deletemember.insert_one(i)
        updated_members = [i for i in org1 if i["memberid"] != data["memberid"]]
        # print("Updated Member list",updated_members)
        conn.event.organization.find_one_and_update({"_id":ObjectId(data["orgid"])},{"$set": {"members":updated_members}})
        return {"data":"Member deleted Successfully","success":True}
    else:
        return {"error":"Invalid Input","success":False}

# Get all Membership of Organization by Clubname
@event.post("/getallmembership")
async def get_all_membership(data : dict):
    membership = conn.event.organization.find_one({"clubname":data["clubname"]}, {"memtype": 1, "_id": 0})
    if membership:
        memtype = serializeDict(membership)["memtype"]
        if len(memtype) !=0:
            return memtype
        else:
            return {"error":"No Membership Type Available","success":False}
    else:
        return {"error":"Organization Not Found","success":False}

# Add New Membership in Organization
@event.put("/addmembership/{clubname}")
async def add_membership(clubname : str,data : dict):
    membership = conn.event.organization.find_one({"clubname":clubname}, {"memtype": 1, "_id": 0})
    if membership:
        memtype = serializeDict(membership)["memtype"]
        memtype.append(data)
        conn.event.organization.find_one_and_update({"clubname":clubname},{"$set": {"memtype":memtype}})
        return {"data":"Membership Added Successfully","success":True}
    else :
        return {"error":"Organization Not Found","success":False}
        
# organisation's member table filters
@event.post("/organisationmembertablefilters")
async def membertable_filtering(filters:dict):
    data = filters["data"]
    orgid = filters["orgid"]
    
    filtered_data = {}
    for key, value in data.items():
        if (value != '' or value != ""):
            filtered_data[key] = re.escape(value)
    print(filtered_data)
    content = []
    if (len(filtered_data) != 0):
        regex_patterns = {}
        for key, value in data.items():
            if value:
                regex_patterns[key] = re.compile(f'^{re.escape(value)}', re.IGNORECASE)

        print (regex_patterns)
        organisation = conn.event.organization.find_one({"_id":ObjectId(orgid)})
        if organisation:
            org1 = serializeDict(organisation)
            membersList = org1["members"]
            if (membersList != []):
                for memberdict in membersList:

                    # match = all(regex.match(str(memberdict.get(key, ''))) for key, regex in regex_patterns.items())
                    match = all(regex.match(str(memberdict.get(key, ''))) for key, regex in regex_patterns.items())
                    if match:
                        print("Match found:", memberdict)
                        content.append(memberdict)

                if content:
                    return content
                else:
                    return {"error":"Members not found","success":False}
            else:
                return {"error":"No Members","success":False}
        else:
            return {"error":"Organisation not found","success":False}
    else:
        
        return {"error":"Please enter data in filter input","success":False,"data_dict":"empty"}

#searching a member by name
@event.post("/orgmemberfilterbyname")
async def fetch_details_byname(data:dict):
    organisation = conn.event.organization.find_one({"_id":ObjectId(data["cid"])})
    result = []
    if organisation:
        org1 = serializeDict(organisation)
        partial_name = data["membername"]
        regex_pattern = re.compile(f".{re.escape(partial_name)}.", re.IGNORECASE)
        # print(org1)
        # member_name = data["membername"]
        # print(member_name)
        for memberdict in org1["members"]:
            print(memberdict["name"])
            if "name" in memberdict and re.match(regex_pattern, memberdict["name"]):
                result.append(memberdict)
        # print(d1)
        print(result)
        if (result != []):
          print(result)
          return result
        else:
            return {"error":"Member Not Found","success":False}
    else:
        return {"error":"Organisation Not Found","success":False}

# Routes for Post ------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>

# Insert Event Post
@event.post("/eventpost/")
async def event_post(data : EventPost):
    try:
        data_dict = dict(data)
        if data_dict["type"] == '':
            return {"error":"Select Membership Type","success":False}
        data_dict["event_start_date"] = data_dict["event_start_date"].strftime("%Y-%m-%d")
        data_dict["event_end_date"] = data_dict["event_end_date"].strftime("%Y-%m-%d")
        data_dict["event_start_date"] = datetime.strptime(data_dict["event_start_date"], "%Y-%m-%d")
        data_dict["event_end_date"] = datetime.strptime(data_dict["event_end_date"], "%Y-%m-%d")
        conn.event.post.insert_one(data_dict)
        return {"data": "Event data successfully submitted"}
    except ValueError:
        return {"error":"ValueError","success":False}
    
# Get Event Post by Clubname
@event.post("/geteventposts")
async def get_event_posts(data : dict):
    response = conn.event.post.find({"clubname":data["clubname"]})
    if response:
        lis = []
        d1= {}
        for singleDict in response:
            d1 = singleDict
            d1["event_start_date"] = d1["event_start_date"].strftime("%d-%m-%Y")
            d1["event_end_date"] = d1["event_end_date"].strftime("%d-%m-%Y")
            lis.append(serializeDict(d1))
        return serializeList(lis)
    else:
        return {"error":"no post found","success":False}

# Event Post filter by parameters
@event.post("/postfilters")   
async def org_filters(filtereddata: dict):
    query = {}

    for field, value in filtereddata.items():

        if field in ["event_start_date", "event_end_date"] and value != "":
            value = datetime.strptime(value, "%Y-%m-%d")
            print(value)
            if field == "event_start_date":
                query["event_start_date"] = {"$gte": value}
                print(query)
            if field == "event_end_date":
                query["event_start_date"] = {"$lte": value}
                print(query)

        if field in ["minprice", "maxprice"] and value != "":
            if field == "minprice":
                # Convert minprice to float and construct the query
                query["ticket_price"] = {"$gte": float(value)}
                print(query)
            if field == "maxprice":
                # Convert maxprice to float and construct the query
                query["ticket_price"] = {"$lte": float(value)}
                print(query)

        if field == "venue_city" and value != "":
            # Construct a case-insensitive regex pattern for venue_city
            regex_pattern = re.compile(f"^{re.escape(value)}", re.IGNORECASE)
            query[field] = {"$regex": regex_pattern}

    # Find posts based on the query
    result = conn.event.post.find(query)

    # Iterate over the result and print each post
    response_list = serializeList(result)
    if response_list:
        lis = []
        d1= {}
        for singleDict in response_list:
            d1 = singleDict
            d1["event_start_date"] = d1["event_start_date"].strftime("%d-%m-%Y")
            d1["event_end_date"] = d1["event_end_date"].strftime("%d-%m-%Y")
            lis.append(serializeDict(d1))
        return serializeList(lis)
    else:
        return {"error": "Error, please fill the form again", "success": False}
    

    
# Delete Event Post
@event.delete("/deleteeventposts/{id}")
async def delete_user(id):
    #fetch the details using id
    # if details found execute the delete query
    #always test in swagger first
    #then bind with UI
    response = serializeDict(conn.event.post.find_one_and_delete({"_id":ObjectId(id)}))
    if response:
        return True
    else:
        return {"error":"no post found","success":False}


# Routes For User ------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>
    
# Signup for User
@event.post("/usersignup/")
async def create_user(user:User):
    d1 = dict(user)
    uname = conn.event.user.find_one({"$and": 
        [
            {"clubname": None},
            {"username": d1["username"]}
        ]
        },{"username":1,"_id":0})
    if uname:
        return {"error":"Username already exists","success":False}
    else:
        conn.event.user .insert_one(dict(user))
        return dict(user)

# Login for User
@event.post("/userlogin/")
async def check_user(data:dict):
    if data["clubname"] == "None" or data["clubname"] == "":
        data["clubname"] = None
    flag=0
    d1= {}
    u1 = conn.event.user.find_one({"$and": [{"username":data["username"]},{"pwd":data["pwd"]},{"clubname":data["clubname"]}]})
    u3 = conn.event.organization.find_one({"clubname":data["clubname"]})
    if u1:
        return serializeDict(u1)
    elif u3:
        user3 = serializeDict(u3)
        membersList =  user3["members"]
        for singleDict in membersList:
            if (singleDict["username"] == data["username"]) and (singleDict["pwd"] == data["pwd"]):
                flag =1
                d1 = singleDict
                d1["clubname"] = data["clubname"]
                conn.event.user.insert_one(d1)
                return serializeDict(d1)
        if flag == 0:
            return {"error":"Invalid Username , Password and Clubname","success":False}
    else : 
        return {"error":"Invalid Username , Password and Clubname","success":False}


# General Routes ---------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Get all the Clubnames
@event.get("/clubnames/")
async def get_clubnames():
    clubname = ["None"]
    cursor = conn.event.organization.find({}, {"clubname": 1, "_id": 0})
    for i in serializeList(cursor):
        clubname.append(i["clubname"])
    return clubname