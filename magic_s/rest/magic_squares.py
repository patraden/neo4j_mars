#!/usr/bin/env python3
def magic_square_calculate(i=0,j=0,sum_col=[7,8],sum_row=[7,8]):
	"""Recursive algorithm to calculate all possible solutions for a random "magic square" (without sums by diagonal)
	with m*k cells and elements as positive integers combined with 0.
	Inputs:
	i - sequential number in a row
	j - sequential number in a column.
	sum_col - sums of elements in each column
	sum_row - sums of elements in each row
	Returns nested array of solutions where elements should be read from right to left, bottom to top to print "magic square".
	Returns [-1] if total sum_col does not match with total sum_row"""
	(k,m)=(len(sum_row),len(sum_col))
	if sum(sum_row)!=sum(sum_col) or len(sum_row)==0 or len(sum_col)==0:
		return [['E']]
	if j%k==k-1: #last row in "magic square"
		return [sum_col[::-1]]
	else:
		result=[]
		elem=min(sum_col[i],sum_row[j])
		if i%m!=m-1:# not a last element in "magic square" row
			if elem==0:
				for x in magic_square_calculate(i+1,j,sum_col,sum_row):
					result.append(x+[elem])
				return result
			else:
				while elem>=0:
					(sum_row_,sum_col_)=(sum_row[:],sum_col[:])
					(i_,j_)=(i,j)
					sum_row[j]-=elem
					sum_col[i]-=elem
					_sum_=0
					for _i_ in range(i+1,m):
						_sum_+=sum_col[_i_]
					if _sum_>=sum_row[j]:
						for x in magic_square_calculate(i+1,j,sum_col,sum_row):
							result.append(x+[elem])
					elem-=1
					(sum_row,sum_col)=(sum_row_[:],sum_col_[:])
					(i,j)=(i_,j_)
				return result
		else: #a last element in "magic square" row
			sum_row[j]-=elem
			sum_col[i]-=elem
			for x in magic_square_calculate(0,j+1,sum_col,sum_row):
				result.append(x+[elem])
			return result
