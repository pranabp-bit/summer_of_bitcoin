#!/usr/bin/env python
# coding: utf-8

# In[34]:


class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee =(fee) 
        self.weight=(weight)
        self.parents=parents


# In[35]:


def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open('mempool.csv') as f:
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])


# In[36]:


Transactions=parse_mempool_csv()


# In[37]:


Transactions.pop(0)


# In[38]:


sum=0
m=0
for x in Transactions:
    m=max(m,len(x.parents)) 
print(m) 
orig_Transactions=Transactions[:]


# In[39]:


vis = {Transactions[0]:0}
idx = {Transactions[0]:0}
trans={}


# In[40]:


n=len(Transactions)
print(n)


# In[41]:


curr_idx=0;
for x in Transactions:
    trans[x.txid]=x
    vis[x.txid]=0
    idx[x.txid]=curr_idx
    curr_idx+=1
    x.fee =int(x.fee) 
    x.weight=int(x.weight)
    x.parents=x.parents.split(';')
    


# In[42]:


#Naive solution constructing a valid block
ans=[]
wt=0
for x in Transactions:
    if(vis[x.txid]==0):
        stack=[]
        stack.append(x)
        flag=0;
        while(len(stack)!=0):
            
            curr_trans=stack[-1]
            
            if(len(curr_trans.parents[0])==0):
                if(wt+curr_trans.weight<=4000000):
                    wt+=curr_trans.weight
                    vis[curr_trans.txid]=1
                    ans.append(curr_trans)
                    stack.pop()
                else:
                    flag=1
                    break
                continue    
                    
            all_parents_visited=1
            for p in curr_trans.parents:
                if(vis[p]==0):
                    all_parents_visited=0
                    stack.append(trans[p])
                    
            if(all_parents_visited==1):
                if(wt+curr_trans.weight<=4000000):
                    wt+=curr_trans.weight
                    vis[curr_trans.txid]=1
                    ans.append(curr_trans)
                    stack.pop()
                else:
                    flag=1
                    break


# In[43]:


print(len(ans))


# In[44]:


for x in Transactions:
    vis[x.txid]=0


# In[45]:


for x in ans:
    vis[x.txid]=1
    for parent in x.parents:
        if(len(parent)==0):
            break
        if(vis[parent]==0):
            print(x.txid)


# In[46]:


fee=0
wt=0
for t in ans:
    fee+=t.fee
    wt+=t.weight
print(fee)  
print(wt)


# In[47]:


cum_wt={}
cum_fee={}
for x in Transactions:
    for y in Transactions:
        vis[y.txid]=0
    wts=0
    fees=0
    stack=[]    
    stack.append(x)
    flag=0;
    while(len(stack)!=0):

        curr_trans=stack[-1]

        if(len(curr_trans.parents[0])==0):
            wts+=curr_trans.weight
            fees+=curr_trans.fee
            vis[curr_trans.txid]=1
            stack.pop()
            continue    

        all_parents_visited=1
        for p in curr_trans.parents:
            if(vis[p]==0):
                all_parents_visited=0
                stack.append(trans[p])

        if(all_parents_visited==1):
            wts+=curr_trans.weight
            fees+=curr_trans.fee
            vis[curr_trans.txid]=1
            stack.pop()
            continue
    cum_wt[x]=wts
    cum_fee[x]=fees
    
    


# In[48]:


density={}
for x in Transactions:
    density[x]=cum_fee[x]/cum_wt[x]


# In[49]:


Keymax = max(density, key=density.get)
print(Keymax.txid)


# In[ ]:


visited={}

for x in Transactions:
    visited[x.txid]=0
    
Final_ans=[]
wght=0
feez=0
i=0
cum_wt={}
cum_fee={}
cur_density={}
while(len(Transactions)!=0):
    i+=1
    print(i)

    for x in Transactions:
        for y in Transactions:
            if(visited[y.txid]==1):
                vis[y.txid]=1
            else:
                vis[y.txid]=0
        wts=0
        fees=0
        stack=[]    
        stack.append(x)
        flag=0;
        while(len(stack)!=0):

            curr_trans=stack[-1]

            if(len(curr_trans.parents[0])==0):
                wts+=curr_trans.weight
                fees+=curr_trans.fee
                vis[curr_trans.txid]=1
                stack.pop()
                continue    

            all_parents_visited=1
            for p in curr_trans.parents:
                if(vis[p]==0):
                    all_parents_visited=0
                    stack.append(trans[p])

            if(all_parents_visited==1):
                wts+=curr_trans.weight
                fees+=curr_trans.fee
                vis[curr_trans.txid]=1
                stack.pop()
                continue
        cum_wt[x]=wts
        cum_fee[x]=fees
        cur_density[x]=cum_fee[x]/cum_wt[x]
    
    while(len(cur_density)!=0):
        Keymax = max(cur_density, key=cur_density.get)
        if(cum_wt[Keymax]+wght<=4000000):
            
            stack=[]
            stack.append(Keymax)
            flag=0;
            while(len(stack)!=0):

                curr_trans=stack[-1]

                if(len(curr_trans.parents[0])==0):
                    wght+=curr_trans.weight
                    feez+=curr_trans.fee
                    ans.append(curr_trans)
                    print(ans[-1].txid)
                    print(wght)
                    print(feez)
                    visited[curr_trans.txid]=1
                    Transactions.remove(curr_trans)
                    stack.pop()
                    continue    

                all_parents_visited=1
                for p in curr_trans.parents:
                    if(visited[p]==0):
                        all_parents_visited=0
                        stack.append(trans[p])

                if(all_parents_visited==1):
                    wght+=curr_trans.weight
                    feez+=curr_trans.fee
                    visited[curr_trans.txid]=1
                    ans.append(curr_trans)
                    print(ans[-1].txid)
                    print(wght)
                    print(feez)
                    Transactions.remove(curr_trans)
                    stack.pop()
            
            break
        else:
            Transactions.remove(Keymax)
            cur_density.pop(Keymax)
    if(len(cur_density)==0):
        break
    cum_wt.clear()
    cum_fee.clear()
    cur_density.clear()


# In[ ]:





# In[ ]:





# In[ ]:


# does NOT work  
#     if(vis[x.txid]==0):
#         if(len(x.parents[0])==0):
#             if(wt+x.weight<=4000000):
#                 vis[x.txid]=1
#                 ans.append(x)
               
#         else:
#             stack=[]
#             stack.append(x)
#             while(len(stack)!=0):
#                 curr_trans=stack.top()
#                 flag=0
#                 for curr_parent in curr_trans.parents:
#                     if(vis[curr_parent]==0):
#                         if(len(trans[curr_parent].parents[0])==0):
#                             if(wt+trans[curr_parent].weight<=4000000):
#                                 vis[curr_parent]=1
#                                 ans.append(trans[curr_parent])
#                             else:
#                                 flag=1
#                                 break
#                         else:
#                             stack.append(trans[curr_parent])
#                 if(flag==0):
#                     stack.pop()
#                     if(wt+curr_trans.weight<=4000000):
#                         vis[curr_trans.txid]=1
#                         ans.append(curr_trans)
                   


# In[ ]:





# In[ ]:


# i=0
# while(1):
#     #print(j)
#     j+=1
#     if(vis[Transactions[i].txid]==0):
#         flag=0
#         for parent in Transactions[i].parents:
#             if(len(parent)==0):
#                 break

#             if(vis[parent]==0):
#                 flag=1
#                 temp=Transactions[i]
#                 dk=idx[parent]
#                 Transactions[i]=Transactions[idx[parent]]
#                 Transactions[idx[parent]]=temp
#                 idx[parent]=i
#                 idx[Transactions[dk].txid]=dk
#                 break;
#         if(flag==0):
#             vis[Transactions[i].txid]=1
#             i+=1
#     if(i>=n):
#         break  


# In[ ]:


# k=0;
# for x in Transactions:
#     vis[x.txid]=0
# for i in range (0,n):
#     vis[Transactions[i].txid]=1
#     for parent in Transactions[i].parents:
#         if(len(parent)==0):
#             break
#         if(vis[parent]==0):
#             print("Problem")
            


# In[ ]:


# #Naive solution constructing a valid block
# ans=[]
# wt=0
# index=0
# while(1):
#     wt+=Transactions[index].weight
#     if(wt>4000000):
#         break
#     ans.append(Transactions[index])    
#     index+=1
    


# In[ ]:


# fee=0
# for t in ans:
#     fee+=t.fee
# print(fee)    


# In[ ]:


# print(len(ans))


# In[ ]:





# In[ ]:




