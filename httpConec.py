import requests
import json
ipp="10.112.228.66"
def sendact(action,paths):
    #paths=[[2,6,2]]
    if action==False:
        print"sending initial action=false,path= ",paths
    url="http://"+ipp+":80/update"
    payload={
        'action':action,
        'traversePath':paths
        }
    payloadJson = json.dumps(payload)
    headers = {
    'content-type': "application/json"
    }
    response = requests.request("POST", url,data=payloadJson,headers=headers)
    #print response
    rspobj=json.loads(response.content)['rewardMatrix']
    print"ques from p4 platform:"
    print rspobj
    return rspobj
    
def sendTopo(topo,host):
    url="http://"+ipp+":80/init"
    payload={
        'graph':topo,
        'hosts':host
        }
    headers = {
    'content-type': "application/json"
    }
    pldJson=json.dumps(payload)
    rsp=requests.request("POST",url,data=pldJson,headers=headers)
    print"p4 platform in readiness."
    return rsp
def resetTopo():
    url="http://"+ipp+":80/reset"
    rsp=requests.request("GET",url)
    return rsp