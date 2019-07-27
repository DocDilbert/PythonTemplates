# 1. Import numpy as np and see the version
import numpy as np

print(np.__version__)
#  ---------------------------------------------------------------------------------
# 2. How to create a 1D array?
#> array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

arr = np.arange(10)
print(repr(arr))

#  ---------------------------------------------------------------------------------

# 3. How to create a boolean array?
arr = np.ones((3,3),dtype='bool')
print(repr(arr))

#  ---------------------------------------------------------------------------------

# 4. How to extract items that satisfy a given condition from 1D array?
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#> array([1, 3, 5, 7, 9])
print(repr(arr[arr%2 == 1]))

#  ---------------------------------------------------------------------------------

# 5. How to replace items that satisfy a condition with another value in numpy array?
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#>  array([ 0, -1,  2, -1,  4, -1,  6, -1,  8, -1])
arr[arr%2 == 1]=-1
print(repr(arr))

#  ---------------------------------------------------------------------------------

# 6. How to replace items that satisfy a condition without affecting the original array?
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# out
#>  array([ 0, -1,  2, -1,  4, -1,  6, -1,  8, -1])
# arr
#>  array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
out = np.where(arr % 2 == 1, -1, arr)
print(repr(out))
print(repr(arr))

#  ---------------------------------------------------------------------------------

# 7. How to reshape an array?
arr = np.arange(10)
#> array([[0, 1, 2, 3, 4],
#>        [5, 6, 7, 8, 9]])
arr = arr.reshape((-1,5))
print(repr(arr))

#  ---------------------------------------------------------------------------------

# 8. How to stack two arrays vertically?
a = np.arange(10).reshape(2,-1)
b = np.repeat(1, 10).reshape(2,-1)
#> array([[0, 1, 2, 3, 4],
#>        [5, 6, 7, 8, 9],
#>        [1, 1, 1, 1, 1],
#>        [1, 1, 1, 1, 1]])
print(np.vstack([a,b]))

#  ---------------------------------------------------------------------------------

# 9. How to stack two arrays vertically?
a = np.arange(10).reshape(2,-1)
b = np.repeat(1, 10).reshape(2,-1)
#> array([[0, 1, 2, 3, 4, 1, 1, 1, 1, 1],
#>        [5, 6, 7, 8, 9, 1, 1, 1, 1, 1]])
print(np.hstack([a,b]))

#  ---------------------------------------------------------------------------------

# 10. How to generate custom sequences in numpy without hardcoding?
arr = np.array([1,2,3])
#> array([1, 1, 1, 2, 2, 2, 3, 3, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3])
print(np.r_[np.repeat(arr,3), np.tile(arr,3)])

#  ---------------------------------------------------------------------------------

# 11. How to get the common items between two python numpy arrays?
a = np.array([1,2,3,2,3,4,3,4,5,6])
b = np.array([7,2,10,2,7,4,9,4,9,8])
#array([2, 4])
print(np.intersect1d(a,b))

#  ---------------------------------------------------------------------------------

#12. How to remove from one array those items that exist in another?
a = np.array([1,2,3,4,5])
b = np.array([5,6,7,8,9])
#array([1,2,3,4])
print(np.setdiff1d(a,b))
 
#  ---------------------------------------------------------------------------------

# 13. How to get the positions where elements of two arrays match?

a = np.array([1,2,3,2,3,4,3,4,5,6])
b = np.array([7,2,10,2,7,4,9,4,9,8])

#> (array([1, 3, 5, 7]),)
print(np.where(a==b))

#  ---------------------------------------------------------------------------------

# 14. How to extract all numbers between a given range from a numpy array?

a = np.array([2, 6, 1, 9, 10, 3, 27])

#(array([6, 9, 10]),)
print(a[np.where((a>=5) & (a<=10))]) 

#  ---------------------------------------------------------------------------------

# 15. How to make a python function that handles scalars to work on numpy arrays?

#Input:

def maxx(x, y):
    """Get the maximum of two items"""
    if x >= y:
        return x
    else:
        return y

maxx(1, 5)
#> 5


a = np.array([5, 7, 9, 8, 6, 4, 5])
b = np.array([6, 3, 4, 8, 9, 7, 1])

#Desired Output:
#pair_max(a, b)
#> array([ 6.,  7.,  9.,  8.,  9.,  7.,  5.])

pair_max = np.vectorize(maxx)
print(pair_max(a,b))

#  ---------------------------------------------------------------------------------

# 16. How to swap two columns in a 2d numpy array?

arr = np.arange(9).reshape(3,3)
print(arr)
arr[:,[0, 1]] = arr[:,[1, 0]]
print(arr)

#  ---------------------------------------------------------------------------------

# 17. How to swap two rows in a 2d numpy array?
arr = np.arange(9).reshape(3,3)
print(arr)

print(arr[[1,0,2], :])

#  ---------------------------------------------------------------------------------

# 18. How to reverse the rows of a 2D array?

# Input
arr = np.arange(9).reshape(3,3)
print(arr[::-1, :])
 
#  ---------------------------------------------------------------------------------

#19. How to reverse the columns of a 2D array?

# Input
arr = np.arange(9).reshape(3,3)
print(arr[:, ::-1])
 
#  ---------------------------------------------------------------------------------

# 20. How to create a 2D array containing random floats between 5 and 10?
print(np.random.uniform(5,10, size=(5,3)))
 
#  ---------------------------------------------------------------------------------

# 21. How to print only 3 decimal places in python numpy array?

rand_arr = np.random.random((5,3))
np.set_printoptions(precision=2)
print(rand_arr)
 
#  ---------------------------------------------------------------------------------

# 22. How to pretty print a numpy array by suppressing the scientific notation (like 1e10)?

# Create the random array
np.random.seed(100)
rand_arr = np.random.random([3,3])/1e3
print(rand_arr)

#> array([[  5.434049e-04,   2.783694e-04,   4.245176e-04],
#>        [  8.447761e-04,   4.718856e-06,   1.215691e-04],
#>        [  6.707491e-04,   8.258528e-04,   1.367066e-04]])

np.set_printoptions(precision=6, suppress=True)
# Desired Output:

#> array([[ 0.000543,  0.000278,  0.000425],
#>        [ 0.000845,  0.000005,  0.000122],
#>        [ 0.000671,  0.000826,  0.000137]])
print(rand_arr)

 #  ---------------------------------------------------------------------------------

# 23. How to limit the number of items printed in output of numpy array?

a = np.arange(15)
#> array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14])

# Desired Output:

#> array([ 0,  1,  2, ..., 12, 13, 14])

np.set_printoptions(threshold=6)
a = np.arange(15)
print(a)
#> array([ 0,  1,  2, ..., 12, 13, 14])
 
#  ---------------------------------------------------------------------------------

# 24. How to print the full numpy array without truncating

np.set_printoptions(threshold=6)
a = np.arange(15)
a
#> array([ 0,  1,  2, ..., 12, 13, 14])

np.set_printoptions(threshold=np.sys.maxsize)

print(a)
#> array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14])
 
#  ---------------------------------------------------------------------------------

# 25. How to import a dataset with numbers and texts keeping the text intact in python numpy?
iris_1d = np.genfromtxt('iris.data',delimiter=',', dtype='object')
print(a)
 
#  ---------------------------------------------------------------------------------

# 26. How to extract a particular column from 1D array of tuples?
iris_1d = np.genfromtxt('iris.data',delimiter=',', dtype='object')
print(np.array([row[4] for row in iris_1d]))
 
#  ---------------------------------------------------------------------------------

# 27. How to convert a 1d array of tuples to a 2d numpy array?
iris_1d = np.genfromtxt('iris.data',delimiter=',', dtype=None)
iris_2d = np.array([row.tolist()[:4] for row in iris_1d])
print(iris_2d)
 
#  ---------------------------------------------------------------------------------

# 28. How to compute the mean, median, standard deviation of a numpy array?
print(np.mean(iris_2d[:,0]))
print(np.median(iris_2d[:,0]))
print(np.std(iris_2d[:,0]))
 
#  ---------------------------------------------------------------------------------

# 29. How to normalize an array so the values range exactly between 0 and 1?
a=iris_2d[:,0]
b = (a-np.amin(a)) / (np.amax(a)-np.amin(a))
print(b)
 
#  ---------------------------------------------------------------------------------

# 30. How to compute the softmax score?

sepallength = a

# Solution
def softmax(x):
    """Compute softmax values for each sets of scores in x.
    https://stackoverflow.com/questions/34968722/how-to-implement-the-softmax-function-in-python"""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

print(softmax(sepallength))
 
#  ---------------------------------------------------------------------------------

# 31. How to find the percentile scores of a numpy array?

print(np.percentile(sepallength, [5,95]))
 
#  ---------------------------------------------------------------------------------

#32. How to insert values at random positions in an array?
iris_1d = np.genfromtxt('iris.data',delimiter=',', dtype='object')
i, j = np.where(iris_2d)

iris_1d[np.random.choice(i,20), np.random.choice(j,20) ] = np.nan
print(iris_1d)
 
#  ---------------------------------------------------------------------------------

#33. How to find the position of missing values in numpy array?

iris_2d = np.genfromtxt('iris.data', delimiter=',', dtype='float', usecols=[0,1,2,3])
iris_2d[np.random.randint(150, size=20), np.random.randint(4, size=20)] = np.nan

sepallength = iris_2d[:,0]

i = np.where(np.isnan(sepallength))
print(i[0])
print(len(i[0]))