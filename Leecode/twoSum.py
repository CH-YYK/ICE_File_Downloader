class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        
        k = 0
        for i in nums:
            j = target - i
            k += 1
            temp = nums[k:]
            if j in temp:
                return [k-1,temp.index(j)+k]