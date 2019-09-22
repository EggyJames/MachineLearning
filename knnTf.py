import numpy as np
import tensorflow as tf
#导入数据
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/",one_hot=True)
#设置样本数目
X_train,Y_train = mnist.train.next_batch(5000)
X_test,Y_test = mnist.test.next_batch(200)
#tf graph input 占位符 用来feed数据
x_train = tf.placeholder(tf.float32,[None,784])
x_test = tf.placeholder(tf.float32,[784])

distance = tf.reduce_sum(tf.abs(tf.add(x_train,tf.negative(x_test))),reduction_indices=1)
pred = tf.arg_min(distance,0)

accuracy = 0

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    for i in range(len(X_test)):
        nn_index = sess.run(pred,feed_dict={x_train:X_train,x_test:X_test[i,:]})
        print("Test", i, "Prediction:", np.argmax(Y_train[nn_index]), \
              "True Class:", np.argmax(Y_test[i]))
        if np.argmax(Y_train[nn_index]) == np.argmax(Y_test[i]):
            accuracy+= 1./len(X_test)
    print("Done!")
    print("Accuracy",accuracy)

