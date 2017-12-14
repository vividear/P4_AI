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
#atest.printTopo()
batch_size=16
batch_number=0
total_episodes=640
episode_number=0
valid_action=0
invalid_action=0
xs,ys,rs=[],[],[]

epslon=0.9
plt_x=range(total_episodes/batch_size)
plt_y=[]
r_batch=[]

valid_action_combo=0
gradBuffer=ag.sess.run(ag.tvars)

total_ac=0
env=atest.Q
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
        total_ac+=1
        act=act if np.random.uniform()<float(episode_number)/total_episodes else np.random.randint(0,ag.ny-1)
        #act=act if np.random.uniform()<epslon else np.random.randint(0,ag.ny-1)
        ys.append(act)
        act-=nodes
        action_type,imm_reward=atest.pre_eval_action(act)
        #print action_type
        #if float(episode_number)/total_episodes>0.8:
            #print"episode:",episode_number,"action:",act,imm_reward
        if action_type=='A':
            invalid_action=0
            atest.action(act)
            if atest.check_connect():
                valid_action+=1
                #take action and update env
                env=atest.Q
                obs=np.reshape(atest.linkFilter(env),[1,ag.nx])
                reward=atest.eval_Ques(obs)-pre_val
                #if reward>0:
                    #print"episode:",episode_number,"action:",act,reward
                rs.append(reward)
            else:
                atest.action(-act)
                reward=-5
                rs.append(reward)
                done=1
                atest.initial()
                env=atest.Q
                r_batch.append(np.mean(rs))
        else:
            invalid_action+=1
            rs.append(imm_reward)
            if invalid_action>10:
                atest.initial()
                env=atest.Q
                r_batch.append(np.mean(rs))
                done=1
    
    valid_action_combo=valid_action_combo if valid_action_combo>len(xs) else len(xs)
    epx = np.vstack(xs)
    epy = np.vstack(ys)
    epr = np.vstack(rs)
    #plt_y.append(np.mean(epr))
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
print "ttacs:",total_ac
print "valid action num:",valid_action
print "max action combo",valid_action_combo  
plt.figure(figsize=(8,4))
plt.plot(plt_x,plt_y)
plt.show()       
      
        
        
