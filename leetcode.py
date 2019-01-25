
# coding: utf-8

# In[47]:


def getmd(nums1, nums2, cuta, cutb, starta, enda):
    if_even = ((len(nums1) + len(nums2)) % 2 == 0)
    if len(nums1)==0 and len(nums2)==0:
        return 0
    elif len(nums1)==0:
        if if_even:
            return (nums2[int(len(nums2)/2-1)]+nums2[int(len(nums2)/2)])/2
        else:
            return nums2[int(len(nums2)/2)]
    elif len(nums2)==0:
        if if_even:
            return (nums1[int(len(nums1)/2-1)]+nums1[int(len(nums1)/2)])/2
        else:
            return nums1[int(len(nums1)/2)]
    if cuta==0:
        max_a = nums2[cutb-1]
    elif cutb==0:
        max_a = nums1[cuta-1]
    elif nums1[cuta-1]>=nums2[cutb-1]:
        max_a = nums1[cuta-1]
    else:
        max_a = nums2[cutb-1]
    if cuta >= len(nums1):
        min_b = nums2[cutb]
    elif cutb >= len(nums2):
        min_b = nums1[cuta]
    elif nums1[cuta]<=nums2[cutb]:
        min_b = nums1[cuta]
    else:
        min_b = nums2[cutb]
    if max_a<=min_b:
        if if_even:
            return (max_a + min_b)/2
        elif (cuta + cutb) > (len(nums1) + len(nums2)) / 2:
            return max_a
        else:
            return min_b
    elif nums1[cuta-1]>=nums2[cutb-1]:
        enda = cuta
        cuta = int((starta + cuta - 1) / 2)
        cutb = int((len(nums1) + len(nums2) + 1) / 2) - cuta
        return getmd(nums1, nums2, cuta, cutb, starta, enda)
    else:
        starta = cuta
        cuta = int((cuta + enda + 1) / 2)
        cutb = int((len(nums1) + len(nums2) + 1) / 2) - cuta
        return getmd(nums1, nums2, cuta, cutb, starta, enda)
def getMedianFromSorted(nums1, nums2):
    size_a = len(nums1)
    size_b = len(nums2)
    cut_a = int((0 + size_a) / 2)
    cut_b = int((size_a + size_b + 1) / 2) - cut_a
    return getmd(nums1, nums2, cut_a, cut_b, 1, size_a)


# In[13]:


def genList(x):
    while(x>0):
        yitem = x%10
        x = x//10
        yield yitem

def isPalindrome(x):
    if x<0:
        return False
    isPalin = True
    ilist = list(genList(x))
    i = 0
    j = len(ilist) - 1
    while(i<j):
        if(ilist[i]!=ilist[j]):
            isPalin = False
            break
        else:
            i+=1
            j-=1
    return isPalin


# In[2]:


def longestCommonPrefix(slist):
    common_prefix = []
    if len(slist)==0:
        return '' 
    min_size = len(slist[0])
    for item in slist:
        if len(item)<min_size:
            min_size = len(item)
    counter = 0
    while(min_size>0):
        min_size-=1;
        substr = slist[0][counter]
        for item in slist:
            if(item[counter]!=substr):
                return ''.join(common_prefix)
        common_prefix.append(substr)
        counter+=1
    return common_prefix


# In[11]:


def sw3ap(swaplist, index1, index2):
    tempitem = swaplist[index1]
    swaplist[index1] = swaplist[index2]
    swaplist[index2] = tempitem

def qsort(qlist, sindex, eindex):
    qsize = eindex - sindex + 1
    mindex = (sindex + eindex) // 2
    if qsize==1:
        return
    elif qsize==2:
        if qlist[sindex]>qlist[eindex]:
            sw3ap(qlist, sindex, eindex)
        return
    else:
        if qlist[sindex]>qlist[mindex]:
            sw3ap(qlist, sindex, mindex)
        if qlist[sindex]>qlist[eindex]:
            sw3ap(qlist, sindex, eindex)
        if qlist[mindex]>qlist[eindex]:
            sw3ap(qlist, mindex, eindex)
        if qsize==3:
            return
    sw3ap(qlist, mindex, eindex-1)
    i = sindex + 1
    j = eindex - 2
    pivot = qlist[eindex-1]
    while(True):
        while(qlist[i]<pivot):
            i+=1;
        while(qlist[j]>pivot):
            j-=1;
        if i>j:
            break
        else:
            sw3ap(qlist, i, j)
    sw3ap(qlist, i, eindex-1)
    qsort(qlist, sindex, i-1)
    qsort(qlist, i+1, eindex)

def get3sum(qlist):
    qsize = len(qlist)
    r_result = []
    if qsize<3:
        return r_result
    else:
        qsort(qlist, 0, qsize-1)
    if_exist = False
    for i in range(0, qsize-2):
        for j in range(i+1, qsize-1):
            for k in range(j+1, qsize):
                if(qlist[i]+qlist[j]+qlist[k]==0):
                    to_append = [qlist[i],qlist[j],qlist[k]]
                    for item in r_result:
                        if item==to_append:
                            if_exist = True
                            break
                    if if_exist:
                        continue
                    r_result.append(to_append)
    return r_result


# In[14]:


qtest = [5,3,1,4,-4,0,-1]
get3sum(qtest)

