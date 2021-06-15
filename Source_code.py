class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee =(fee) 
        self.weight=(weight)
        self.parents=parents

def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open('mempool.csv') as f:
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])

#store the list of MempoolTransactions in variable 'Transactions' 
Transactions=parse_mempool_csv()                            

#remove the first element of the list which contains headings of the columns(tx_id,fee,weight,parent)
Transactions.pop(0)

#maintain a copy of the list for future use
orig_Transactions=Transactions[:] 

#initialize a dictionary called 'vis' which indicates that while traversing over the transactions, has the particular transaction been visited(0 means "not visited", 1 means "visited")
vis = {Transactions[0]:0}

#initialize a dictionary 'trans' which maps string tx_id to MempoolTransactions
trans={}

n=len(Transactions)
#print(n)

for x in Transactions:
    # map all tx_id's to their corresponding MempoolTransactions
    trans[x.txid]=x
    
    #mark all tx_id's as "Not visited"
    vis[x.txid]=0
    
    # typecast fee and weight from string to int (for calculation)
    x.fee =int(x.fee) 
    x.weight=int(x.weight)
    
    #for each transaction, parents attribute will now store list of string
    x.parents=x.parents.split(';')
    
#initialize a dictionary 'visited' which indicates that while traversing over the transactions , has the particular transaction been visited(0 means "not visited", 1 means "visited")
visited={}

for x in Transactions:
    #mark all tx_id's as "Not visited"
    visited[x.txid]=0
    
# ordered list of MempoolTransactions
ans=[]

# keep a note of the the total weight of transactions which have been added to the block
wght=0
# keep a note of the the total fees of transactions which have been added to the block
feez=0

"""
This problem is similar to the knapsack problem, but with constrainsts which don't allow the use of the usual knapsack approach.
One solution to tackle this problem can be the use of the ratio of fee and weight. Since individual weights are much smaller than the maximum value allowed, 
this approach will bring us to a nearly perfect answer. For transactions which have parent tranactions, we can calculate the cumulative weight, and cumulative fees 
of the transactions and use their ratio to determine which transaction should be added next. This cumulative weight and cumulated fees will keep on changing 
after each addition to the block. So, we can calculate these after each addition to find the maximum possible fees within the given weight limit.
"""
# initialize dictionary for cumulative weight
cum_wt={}
# initialize dictionary for cumulative fees
cum_fee={}
# initialize dictionary to store the ratio of cum_fee and cum_wt
cur_density={}

# iterate over the transactions again and again till the list Transactions becomes empty.
# In each iteration keep removing the transactions which are being added to the ans and the transactions which CANNOT be added to the ans
while(len(Transactions)!=0):
    # First step is to calculate cum_wt, cum_fee, cur_density for each transaction
    for x in Transactions:
        # update the dictionary 'vis' for each transaction.
        for y in Transactions:
            if(visited[y.txid]==1):
                vis[y.txid]=1
            else:
                vis[y.txid]=0
        #store the cumulative weight for the current transaction in wts        
        wts=0
        #store the cumulative fee for the current transaction in fees
        fees=0
        stack=[] 
        # Stack is being used to execute something similar to a depth first search
        stack.append(x)
        flag=0;
        
        # Those elements are added to the stack which need to be traversed if transaction x would be added to the ans
        # So all the elements of the stack, their parents, their parents and so on need to be traversed
        while(len(stack)!=0):
            # Accessing the top element of the stack, and storing that transaction in 'curr_trans'
            curr_trans=stack[-1]

            # if the curr_trans has no parent, simply add its weight and fee to the corresponding cumulative wts and fees, and remove it from the stack
            if(len(curr_trans.parents[0])==0):
                wts+=curr_trans.weight
                fees+=curr_trans.fee
                vis[curr_trans.txid]=1
                stack.pop()
                continue    

            # Check whether all the parents of the curr_trans have been visited, if not push those not visited into the stack    
            all_parents_visited=1
            for p in curr_trans.parents:
                if(vis[p]==0):
                    all_parents_visited=0
                    stack.append(trans[p])
            
            # if all the parents of the curr_trans have been visited, simply add its weight and fee to the corresponding cumulative wts and fees, and remove it from the stack
            if(all_parents_visited==1):
                wts+=curr_trans.weight
                fees+=curr_trans.fee
                vis[curr_trans.txid]=1
                stack.pop()
                continue
                
        # Update the dictionaries        
        cum_wt[x]=wts
        cum_fee[x]=fees
        cur_density[x]=cum_fee[x]/cum_wt[x]
        
    #Second step is to choose the transaction which has the maximum cur_density and its cumulated weight and the current total weight do not exceed the maximum weight allowec
    #keep on removing the current maximum density, if it cannot be added to the ans.
    while(len(cur_density)!=0):
        # Store the transaction with the maximum density
        Keymax = max(cur_density, key=cur_density.get)
        if(cum_wt[Keymax]+wght<=4000000):
            ##since the sum is less than maximum limit, task is to add the current transaction to the ans after adding its non visited parents, their parents, and so on.
            stack=[]
            stack.append(Keymax)
            flag=0;
            while(len(stack)!=0):
                # Accessing the top element of the stack, and storing that transaction in 'curr_trans'
                curr_trans=stack[-1]
                
                # if the curr_trans has no parent, append the transaction to the ans, update wght & feez and remove it from the stack
                if(len(curr_trans.parents[0])==0):
                    wght+=curr_trans.weight
                    feez+=curr_trans.fee
                    ans.append(curr_trans)
#                     print(ans[-1].txid)
#                     print(wght)
#                     print(feez)
                    visited[curr_trans.txid]=1
                    Transactions.remove(curr_trans)
                    stack.pop()
                    continue    
                
                # Check whether all the parents of the curr_trans have been visited, if not push those not visited into the stack
                all_parents_visited=1
                for p in curr_trans.parents:
                    if(visited[p]==0):
                        all_parents_visited=0
                        stack.append(trans[p])

                # if all the parents of the curr_trans have been visited, append the transaction to the ans, update wght & feez and remove it from the stack        
                if(all_parents_visited==1):
                    wght+=curr_trans.weight
                    feez+=curr_trans.fee
                    visited[curr_trans.txid]=1
                    ans.append(curr_trans)
#                     print(ans[-1].txid)
#                     print(wght)
#                     print(feez)
                    Transactions.remove(curr_trans)
                    stack.pop()
            
            break
        else:
            # This transaction can never be added to ans
            Transactions.remove(Keymax)
            cur_density.pop(Keymax)
            
    if(len(cur_density)==0):
        ## NO more transactions can be added to the ans
        break
    cum_wt.clear()
    cum_fee.clear()
    cur_density.clear()

BLOCK=[]
for x in ans:
    BLOCK.append(x.txid)

### Verifying that it is a valid block:
#Count of a particular tx_id in the list BLOCK is '1'
cnt=0
for x in BLOCK:
    if(BLOCK.count(x)!=1):
        print("ERROR: Repeated Transaction")
        
#Setting all transactions to not visited        
for x in orig_Transactions:
    vis[x.txid]=0
    
Total_weight=0
Total_fee=0
for x in BLOCK:
    vis[x]=1
    Total_weight+=trans[x].weight
    Total_fee+=trans[x].fee
    for parent in trans[x].parents:
        if(len(parent)==0):
            break
        if(vis[parent]==0):
            print("ERROR: Parent transaction not found")    
            
# write the tx_id's of BLOCK in the output file block.txt            
output_file = open("block.txt", "w")
for line in BLOCK:
  # write line to output file
  output_file.write(line)
  output_file.write("\n")
output_file.close()


### Step-by-Step verification was done before reaching the above final code:    
# #Naive solution constructing a valid block
# ans=[]
# wt=0
# for x in Transactions:
#     #mark all tx_id's as "Not visited"
#     vis[x.txid]=0
# for x in Transactions:
#     if(vis[x.txid]==0):
#         stack=[]
#         stack.append(x)
#         flag=0;
#         while(len(stack)!=0):
            
#             curr_trans=stack[-1]
            
#             if(len(curr_trans.parents[0])==0):
#                 if(wt+curr_trans.weight<=4000000):
#                     wt+=curr_trans.weight
#                     vis[curr_trans.txid]=1
#                     ans.append(curr_trans)
#                     stack.pop()
#                 else:
#                     flag=1
#                     break
#                 continue    
                    
#             all_parents_visited=1
#             for p in curr_trans.parents:
#                 if(vis[p]==0):
#                     all_parents_visited=0
#                     stack.append(trans[p])
                    
#             if(all_parents_visited==1):
#                 if(wt+curr_trans.weight<=4000000):
#                     wt+=curr_trans.weight
#                     vis[curr_trans.txid]=1
#                     ans.append(curr_trans)
#                     stack.pop()
#                 else:
#                     flag=1
#                     break


# print(len(ans))


# for x in Transactions:
#     vis[x.txid]=0

# for x in ans:
#     vis[x.txid]=1
#     for parent in x.parents:
#         if(len(parent)==0):
#             break
#         if(vis[parent]==0):
#             print(x.txid)


# cum_wt={}
# cum_fee={}
# for x in Transactions:
#     for y in Transactions:
#         vis[y.txid]=0
#     wts=0
#     fees=0
#     stack=[]    
#     stack.append(x)
#     flag=0;
#     while(len(stack)!=0):

#         curr_trans=stack[-1]

#         if(len(curr_trans.parents[0])==0):
#             wts+=curr_trans.weight
#             fees+=curr_trans.fee
#             vis[curr_trans.txid]=1
#             stack.pop()
#             continue    

#         all_parents_visited=1
#         for p in curr_trans.parents:
#             if(vis[p]==0):
#                 all_parents_visited=0
#                 stack.append(trans[p])

#         if(all_parents_visited==1):
#             wts+=curr_trans.weight
#             fees+=curr_trans.fee
#             vis[curr_trans.txid]=1
#             stack.pop()
#             continue
#     cum_wt[x]=wts
#     cum_fee[x]=fees
    

# density={}
# for x in Transactions:
#     density[x]=cum_fee[x]/cum_wt[x]

# Keymax = max(density, key=density.get)
# print(Keymax.txid)



