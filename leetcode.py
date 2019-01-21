
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


# In[19]:


isPalindrome(1243321)

