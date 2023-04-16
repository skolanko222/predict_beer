import pandas as pd
import numpy as np
from beer_db.models import Beer

class DecisionTreeReg():
	class Branch():
		def __init__(self,
					leaf_value=None,
					left_child=None,
					right_child=None,
					flag=None,
					var_value=None,
					feature_index=None):
			self.leaf_value=leaf_value
			self.left_child=left_child
			self.right_child=right_child
			self.flag=flag
			self.var_value=var_value
			self.feature_index=feature_index


	def __init__(self, max_depth=2,min_samples=2):
		self.root=None
		self.max_depth=max_depth
		self.min_samples=min_samples
		self.leaf_list=[]

	def build(self,data,depth=0):
		split={}
		n_samples=data.shape[0]
		n_features=data.shape[1]-1
		if n_samples>=self.min_samples and depth<=self.max_depth:
			split=self.best_split(data,n_features)
			if split['var_value']>0: 
				left_child=self.build(split['l_data'],depth+1)
				right_child=self.build(split['r_data'],depth+1)

				return self.Branch(None,left_child,right_child,split['flag'],split['var_value'],split['feature_index'])
		node_value=np.mean(data[:,-1])
		self.leaf_list.append(data[:,-1])
		return self.Branch(node_value)

	def data_sep(self,data,f_ind,limit):
		left=np.array([i for i in data if i[f_ind] <=limit])
		right=np.array([i for i in data if i[f_ind] >limit])
		return left,right
	def print_leaf(self):
		print(self.leaf_list)

	def best_split(self,data,n_features):
		split={'var_value': np.NINF}
		for feature_ind in range(n_features):
			flag_arr=np.unique(data[:,feature_ind])
			for flag_val in flag_arr:
				l_data,r_data=self.data_sep(data,feature_ind,flag_val)
				if len(l_data)>0 and len(r_data)>0:
					y,l_y,r_y=data[:,-1],l_data[:,-1],r_data[:,-1]
					variance=np.var(y)- len(l_y)/len(y)*np.var(l_y)-len(r_y)/len(y)*np.var(r_y)
					if variance>split['var_value']:
						split['flag']=flag_val
						split['var_value']=variance
						split['feature_index']=feature_ind
						split['l_data']=l_data
						split['r_data']=r_data
		return split

	def fit(self,data_with_y):
		self.root=self.build(data_with_y)
		return self

	def predict(self,X):
		pred_list=[self.prediction(x,self.root) for x in X]
		return pred_list
	def prediction(self,x,tree):
		if tree==None:
			return 0
		if tree.leaf_value!=None:
			return tree.leaf_value
		if x[tree.feature_index]<=tree.flag:
			return self.prediction(x,tree.left_child)
		else:
			return self.prediction(x,tree.right_child)

def Create_data():
	database=Beer.objects.all()
	data=pd.DataFrame(data=database.values())
	y=data['Ave_Rating']
	data.drop([i for i in data.keys() if (data.dtypes[i]=='object' or i=='key' or i=='id') and i!='ABV'],axis=1,inplace=True)	
	data=np.asarray(data,dtype=np.float64)
	y=np.asarray(y,dtype=np.float64)
	data_with_y=np.insert(data,data.shape[1],y,axis=1)
	return data_with_y,data,y

def SingleTree(features_arr):
	import os

	_,data,y=Create_data()
	
	feature_partition=features_arr.shape[0]
	stripped_data=[]
	cols=[]
	for feature in features_arr:
		cols.append(feature)
		stripped_data.append(data[:,feature])
	stripped_data.append(y)
	stripped_data=np.asarray(stripped_data)
	stripped_data=stripped_data.T

	model=DecisionTreeReg(max_depth=feature_partition*3)
	tree=model.fit(stripped_data)
	print(f'Builing {stripped_data.shape} on {os.getpid()}')
	return tree

def DecisionForestReg(forest):
	best_feature_fit=np.array([[0, 4, 0, 3, 13], 	
							   [0, 8, 1, 8, 11], 	
							   [7, 1, 9, 0, 13], 	#[11, 8, 2, 3, 4]
							   [0, 1, 2, 14, 0], 	# 
							   [0, 11, 10, 5, 4]]) 	#[0, 6, 1, 3, 3]
	import multiprocessing
	with multiprocessing.Pool() as parallel_forest:
		trees=parallel_forest.map(SingleTree,[best_feature_fit[i] for i in range(best_feature_fit.shape[1])])
	forest.append(trees)
	return forest

def from_tree_to_lin(forest):
	data_with_y,X,y=Create_data()
	data=[tree.predict(X) for tree in forest[0]]
	data = np.asmatrix(data,dtype=np.float64).T
	free_column=np.matrix([[1] for _ in range(data.shape[0])],dtype=np.float64)
	data=np.insert(data,data.shape[1],free_column.T,axis=1)
	y = np.asmatrix(y, dtype=data.dtype)
	y=y.T
	wages=np.ones([*data.shape])
	wages=wages.T
	factor_mx=[]
	for i in range(data.shape[1]):
		factor_mx.append([wages[i,0] if i==j else 0 for j in range(data.shape[1])])
	factor_mx=np.asarray(factor_mx, dtype=np.float64)
	data=np.dot(data,factor_mx)

	gradient=(data.T @ data).I @ data.T @ y
	return gradient
# def DecisionForestReg():
	best_feature_fit=np.array([[13, 1, 8, 10, 10],
 							[9, 12, 4, 9, 6],
 							[0, 4, 5, 6, 7],
 							[7, 5, 8, 9, 0],
 							[7, 1, 0, 12, 11]])
	import multiprocessing
	with multiprocessing.Pool() as parallel_forest:
		trees=parallel_forest.map(SingleTree,[[random.randint(0,14) for _ in range(5)] for i in range(best_feature_fit.shape[1])])
	# forest.append(trees)
	return trees
# def from_tree_to_lin(forest):
	data_with_y,X,y=Create_data()
	data=[tree.predict(X) for tree in forest]
	data = np.asmatrix(data,dtype=np.float64).T
	free_column=np.matrix([[1] for _ in range(data.shape[0])],dtype=np.float64)
	data=np.insert(data,data.shape[1],free_column.T,axis=1)
	print(data.shape)
	y = np.asmatrix(y, dtype=data.dtype)
	y=y.T
	wages=np.ones([*data.shape])
	wages=wages.T
	factor_mx=[]
	for i in range(data.shape[1]):
		factor_mx.append([wages[i,0] if i==j else 0 for j in range(data.shape[1])])
	factor_mx=np.asarray(factor_mx, dtype=np.float64)
	data=np.dot(data,factor_mx)

	gradient=(data.T @ data).I @ data.T @ y
	return gradient
# def Finding_best_columns_to_forest():
	all_result_v5_trees=[]
	all_result_v5_cols=[]
	all_linTree_reg_result_v5=[]

	for numerek in range(1000):
		f_1=open('grad_list.txt','a')
		f_2=open('cols_list.txt','a')
		data_arr,y,data=Create_data()
		result_v5=DecisionForestReg()
		result_v5_trees=[result_v5[i][0] for i in range(len(result_v5))]
		result_v5_cols=[result_v5[i][1] for i in range(len(result_v5))]
		f_2.write(str(numerek))
		f_2.write(str(result_v5_cols))
		f_2.write('\n\n')
		all_result_v5_trees.append(result_v5_trees)
		all_result_v5_cols.append(result_v5_cols)
		# //////////////////////////////////////////////////////////////////
		linTree_reg_result_v5=from_tree_to_lin(result_v5_trees)
		f_1.write(str(numerek))
		f_1.write(str(linTree_reg_result_v5))
		f_1.write('\n\n')
		all_linTree_reg_result_v5.append(linTree_reg_result_v5)
		print('---')
		f_1.close()
		f_2.close()
	print(str(all_linTree_reg_result_v5))
	return all_result_v5_trees,all_result_v5_cols,all_linTree_reg_result_v5

def definite_fit(data,forest):
	data=np.asarray(data)
	factors=from_tree_to_lin(forest)
	# print(factors)
	res_before_linreg=[tree.predict(data) for tree in forest[0]]
	res_before_linreg_arr=np.asarray(res_before_linreg).T
	final_results_linreg=np.insert(res_before_linreg_arr,res_before_linreg_arr.shape[1],np.ones([1,res_before_linreg_arr.shape[0]]),axis=1)
	final_results_linreg=final_results_linreg.dot(factors)
	
	return final_results_linreg

