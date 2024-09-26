import warnings
from asyncio import run
from puresnmp import Client, V2C, PyWrapper
from puresnmp import ObjectIdentifier as OID
from puresnmp.exc import NoSuchOID
from collections import defaultdict 
from x690.types import *
from typing import Literal
from puresnmp_olt.tools import ascii_to_hex
# from tools import ascii_to_hex


#Get data
def Get(host: str, community: str, oid: str):
    try:
        warnings.simplefilter("ignore")
        client = PyWrapper(Client(host, V2C(community)))
        value = client.get(oid)
        response = run(value)

        return oid,response
    except:
        print({"Cod":NoSuchOID.DEFAULT_MESSAGE})
        return {
                "Cod":404,
                "Message":NoSuchOID.DEFAULT_MESSAGE
            }
    
#Get data in async
async def Get_async(host: str, community: str, oid: str):
    try:
        warnings.simplefilter("ignore")
        client = PyWrapper(Client(host, V2C(community)))
        value = await client.get(oid)

        return oid,value
    except:
        print({"Cod":NoSuchOID.DEFAULT_MESSAGE})
        return {
                "Cod":404,
                "Message":NoSuchOID.DEFAULT_MESSAGE
            }
    
#Get data next
def GetNext(host: str, community: str, oid: str):
    try:
        warnings.simplefilter("ignore")
        client = PyWrapper(Client(host, V2C(community)))
        value = client.getnext(oid)
        response = run(value)

        return oid,response[1]
    except:
        print({"Cod":NoSuchOID.DEFAULT_MESSAGE})
        return {
                "Cod":404,
                "Message":NoSuchOID.DEFAULT_MESSAGE
            }
    
#Get data next
async def GetNext_async(host: str, community: str, oid: str):
    try:
        warnings.simplefilter("ignore")
        client = PyWrapper(Client(host, V2C(community)))
        value = await client.getnext(oid)

        return value[0],value[1]
    except:
        print({"Cod":NoSuchOID.DEFAULT_MESSAGE})
        return {
                "Cod":404,
                "Message":NoSuchOID.DEFAULT_MESSAGE
            }

#MultiGet data
def MultiGet(host: str, community: str, oid: list[str]):
    data = []
    try:
        warnings.simplefilter("ignore")
        client = PyWrapper(Client(host, V2C(community)))
        value = client.multiget(oid)
        response = run(value)
        if response is not None:
            for x in range(len(oid)):
                data.append({"oid":oid[x],
                        "value":response[x]})
        return data
    except:
        print({"Cod":NoSuchOID.DEFAULT_MESSAGE})
        return {
                "Cod":404,
                "Message":NoSuchOID.DEFAULT_MESSAGE
            }
    
#MULTIWALK is necesary execute with run of "from asyncio import run" examp = run(MultiTask(...)) 
async def MultiWalk_async(host: str, community: str, oid: list[str],only_final_id=False,decode_ascii=False):
    try:
        data = []
        warnings.simplefilter("ignore")
        client = PyWrapper(Client(host, V2C(community)))
        async for row in client.multiwalk(oid):
            if decode_ascii:
                decode = ascii_to_hex(row[1])
            else:
                decode = row[1]

            if only_final_id:
                data.append({"oid": row[0].split(".")[-1], "value": decode})  
            else:
                data.append({"oid": row[0], "value": decode}) 
        return data
    except:
        print({"Error":NoSuchOID.DEFAULT_MESSAGE})
        return {
                "Cod":404,
                "Message":NoSuchOID.DEFAULT_MESSAGE
            }
    
#MULTIWALK is necesary execute with run of "from asyncio import run" examp = run(Walk_async(...)) 
async def Walk_async(host: str, community: str, oid: str,only_final_id=False,decode_ascii=False):
    try:
        data = []
        warnings.simplefilter("ignore")
        client = PyWrapper(Client(host, V2C(community)))
        async for row in client.walk(oid):
            if decode_ascii:
                decode = ascii_to_hex(row[1])
            else:
                decode = row[1]

            if only_final_id:
                data.append({"oid": row[0].split(".")[-1], "value": decode})  
            else:
                data.append({"oid": row[0], "value": decode}) 
        return data
    except:
        print({"Error":NoSuchOID.DEFAULT_MESSAGE})
        return {
                "Cod":404,
                "Message":NoSuchOID.DEFAULT_MESSAGE
            }
    
# #MULTIWALK is necesary execute with run of "from asyncio import run" examp = run(MultiTask(...)) 
# def MultiWalk(host: str, community: str, oid: list[str],only_final_id=False,decode_ascii=False):
#     try:
#         data = []
#         warnings.simplefilter("ignore")
#         client = PyWrapper(Client(host, V2C(community)))
        
#         value = client.multiwalk(oid)
#         print(value)
#         response = run(value)
#         return data
#     except:
#         print({"Error":NoSuchOID.DEFAULT_MESSAGE})
#         return {
#                 "Cod":404,
#                 "Message":NoSuchOID.DEFAULT_MESSAGE
#             }

#Set data in snmp 
def Set(host: str, community: str, oid: str,new_value,_type: Literal["int", "Oct"] = "int"):
        types = {
            "int":Integer,
            "Oct":OctetString
        }
        try:
            warnings.simplefilter("ignore")
            client = Client(host, V2C(community))
            value = client.set(OID(oid),types[_type](new_value))
            response = run(value)
            return{
                "Cod":200,
                "Message":f"Change to {new_value}"
            }
        except:
            return {
                "Cod":404,
                "Message":NoSuchOID.DEFAULT_MESSAGE
            }

#Set data in async
async def Set_async(host: str, community: str, oid: str,new_value,_type: Literal["int", "Oct"] = "int"):
    types = {
            "int":Integer,
            "Oct":OctetString
        }
    try:
        warnings.simplefilter("ignore")
        client = PyWrapper(Client(host, V2C(community)))
        value = await client.set(oid,types[_type](new_value))

        return{
                "Cod":200,
                "Message":f"{value}"
            }
    except:
        print({"Error":NoSuchOID.DEFAULT_MESSAGE})
        return {
                "Cod":404,
                "Message":NoSuchOID.DEFAULT_MESSAGE
            }
    

###In working ################################
#MultiSet data in snmp 
def MultiSet(host: str, community: str, oid: str,new_value,_type: Literal["int", "Oct"] = "int"):
        types = {
            "int":Integer,
            "Oct":OctetString
        }
        try:
            warnings.simplefilter("ignore")
            client = Client(host, V2C(community))
            value = client.set(OID(oid),types[_type](new_value))
            response = run(value)

            return ({"Change to":new_value})
        except:
            print({"Cod":NoSuchOID.DEFAULT_MESSAGE})
            return {
                "Cod":404,
                "Message":NoSuchOID.DEFAULT_MESSAGE
            }






# def Table(host: str, community: str, oid: str):
#     data = []
    
#     warnings.simplefilter("ignore")
#     client = PyWrapper(Client(host, V2C(community)))
#     value = client.table(oid)
#     response = run(value)
#     if response is not None:
#         for x in range(len(response)):
#             for id,value in response[x]:
#                 print(value)
#     return "ff"
