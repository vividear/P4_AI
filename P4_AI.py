import numpy as np
import tensorflow as tf
import math
import cPickle
import graph
import RLAgent
import httpConec as hC
import matplotlib.pyplot as plt
import geneTopo

topo,hosts,nodes,links=geneTopo.getDCtopo()
ag=RLAgent.PGNAgent(links,nodes*2+1)
atest=graph.graf(nodes,links,initopo=topo,inihost=hosts)
atest.initial()
atest.printTopo() 
ini_path=atest.getpath()
print ini_path
batch_size=32
batch_number=0
total_episodes=6400
episode_number=0
valid_action=0
xs,ys,rs=[],[],[]

epslon=0.9
plt_x=range(total_episodes/batch_size)
plt_y=[]
r_batch=[]

gradBuffer=ag.sess.run(ag.tvars)

rsp=hC.sendTopo(atest.E,atest.host)
env=hC.sendact(False,ini_path)

while episode_number<total_episodes:
    episode_number+=1
    batch_number+=1
    done=0
    obs=np.reshape(atest.linkFilter(env),[1,ag.nx])
    while done==0:
        #obs=np.reshape(atest.linkFilter(env),[1,ag.nx])
        xs.append(obs)
        pre_val=atest.eval_Ques(obs)
        act=ag.rollaction(obs)[0][0]
        act=act if np.random.uniform()<float(episode_number)/total_episodes else np.random.randint(0,ag.ny-1)
        
        ys.append(act)
        act-=nodes
        action_type,imm_reward=atest.pre_eval_action(act)
        #print action_type
        if action_type=='A':
            atest.action(act)
            if atest.check_connect():
                valid_action+=1
                #take action and update env
                paths=atest.getpath()  # send action to p4 platform
                print("send action and path to p4:",act,paths)
                env=hC.sendact(act,paths) 
                obs=np.reshape(atest.linkFilter(env),[1,ag.nx])  # update enviroment(observation)
                print("get observation f:",obs)
                reward=atest.eval_Ques(obs)-pre_val
                rs.append(reward)

            else:
                atest.action(-act)
                reward=-5
                rs.append(reward)
                done=1
                
                rsp=hC.resetTopo()
                paths=atest.getpath()
                env=hC.sendact(False, paths)
        else:
            done=1
            rs.append(imm_reward)
    
    epx = np.vstack(xs)
    epy = np.vstack(ys)
    epr = np.vstack(rs)
    r_batch.append(np.mean(epr))
    
    xs,ys,rs=[],[],[]
    tgrad=ag.calGrad(epx, epy, epr)  
    for ix,grad in enumerate(tgrad):
        gradBuffer[ix] += grad  
    if batch_number==batch_size:
        batch_number=0
        plt_y.append(np.mean(r_batch))
        r_batch=[]
        ag.applyGrad(gradBuffer)
        for ix,grad in enumerate(gradBuffer):
            gradBuffer[ix] = grad * 0
plt.figure(figsize=(8,4))
plt.plot(plt_x,plt_y)
plt.show()
print "valid action num:",valid_action        