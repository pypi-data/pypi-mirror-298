import numpy as np

class SVM_classifier:


  # initiating the hyperparemeters
  def __init__(self,learning_rate,no_of_iteration,lambda_parameter):
    self.learning_rate = learning_rate
    self.no_of_iteration = no_of_iteration
    self.lambda_parameter = lambda_parameter


  # function to fitting the data
  def fit(self,X,Y):

    # m--> no of data points
    #n-->no of features
    self.m,self.n=X.shape

    #initiating the weight and bias
    self.w = np.zeros(self.n)
    self.b=0
    self.X=X
    self.Y=Y

    #implementing of gradient descent algorithm

    for i in range(self.no_of_iteration):
      self.update_weight()

  #function to update the weight and bias
  def update_weight(self):
    #label encoding
    y_label = np.where(self.Y<=0,-1,1)

    for index,x_i in enumerate(self.X):
      condition = y_label[index]*(np.dot(x_i,self.w)-self.b)>=1

      if(condition==True):
        dw = 2*self.lambda_parameter*self.w
        db=0

      else:
        dw = 2*self.lambda_parameter*self.w - np.dot(x_i,y_label[index])
        db = y_label[index]

      self.w=self.w-self.learning_rate*dw
      self.b=self.b-self.learning_rate*db

  # function to predict the label from the input values
  def predict(self,X):
    output = np.dot(X,self.w)-self.b

    predicted_label = np.sign(output)

    y_hat = np.where(predicted_label <= -1,0,1)

    return y_hat