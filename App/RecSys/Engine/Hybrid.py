import glob
import horovod.tensorflow as hvd
import numpy as np
import os
import tensorflow as tf

from Technipedia.App.RecSys.Extract import read_in_csv_file
from Technipedia.App.RecSys.User_dispatcher import dispatch


def buid_Tensorflow_Engine_Model(df_train, users_number, items_number, steps, batch_size, feature_len):
    tf.reset_default_graph()
    # Build model...
    datapoint_size = df_train.shape[0]
    U = tf.Variable(initial_value=tf.truncated_normal([users_number, feature_len]), name='users', dtype=tf.float32)
    P = tf.Variable(initial_value=tf.truncated_normal([feature_len, items_number]), name='items', dtype=tf.float32)
    result = tf.matmul(U, P)
    result_flatten = tf.reshape(result, [-1])
    global_step = tf.train.get_or_create_global_step() #tf.contrib.framework.get_or_create_global_step()  # for horovod
    lr = tf.constant(.1, name='learning_rate')
    learning_rate = tf.train.exponential_decay(lr, global_step, 10000, 0.96, staircase=True)
    user_indecies = tf.placeholder(tf.int32, shape=(batch_size,))
    item_indecies = tf.placeholder(tf.int32, shape=(batch_size,))
    rates = tf.placeholder(tf.float32, shape=(batch_size,))
    R = tf.gather(result_flatten, (user_indecies - 1) * tf.shape(result)[1] + item_indecies - 1)
    # calcul du cout total
    user_indeciesall = [x - 1 for x in df_train.user.values]
    item_indeciesall = [x - 1 for x in df_train.item.values]
    ratesall = df_train.rate.values
    result_flattenall = tf.reshape(tf.matmul(U, P), [-1])
    Rall = tf.gather(result_flattenall, user_indeciesall * tf.shape(result)[1] + item_indeciesall)
    diff_opall = tf.subtract(Rall, ratesall)
    true_cost = tf.sqrt(tf.reduce_sum(tf.square(diff_opall))) / datapoint_size
    # calcul du cout debile
    diff_op = tf.subtract(R, rates)
    cost = tf.reduce_mean(tf.square(diff_op), name='cost')
    # fin définition du modèle

    # Horovod: adjust learning rate based on number of GPUs.
    opt = tf.train.GradientDescentOptimizer(learning_rate, )  # 0.001 * hvd.size())

    # Horovod: add Horovod Distributed Optimizer.
    opt = hvd.DistributedOptimizer(opt)

    # entrainement du modèle
    training_step = opt.minimize(cost, global_step=global_step, var_list=[U, P])

    hooks = [
        # Horovod: BroadcastGlobalVariablesHook broadcasts initial variable states
        # from rank 0 to all other processes. This is necessary to ensure consistent
        # initialization of all workers when training is started with random weights
        # or restored from a checkpoint.
        hvd.BroadcastGlobalVariablesHook(0),

        # Horovod: adjust number of steps based on number of GPUs.
        # tf.train.StopAtStepHook(last_step=(20000 // hvd.size()),

        tf.train.LoggingTensorHook(tensors={'step': global_step, 'loss': true_cost}, every_n_iter=10),
    ]

    # Horovod: pin GPU to be used to process local rank (one GPU per process)
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    config.gpu_options.visible_device_list = str(hvd.local_rank())

    # Horovod: save checkpoints only on worker 0 to prevent other workers from
    # corrupting them.

    """filelist = glob.glob("./checkpoints/*")
    for file in filelist:
        os.remove(file)
    if os.path.isdir('./checkpoints'):
        os.removedirs('./checkpoints')"""
    checkpoint_dir = './checkpoints' if hvd.rank() == 0 else None

    # The MonitoredTrainingSession takes care of session initialization,
    # restoring from a checkpoint, saving to a checkpoint, and closing when done
    # or an error occurs.
    with tf.train.MonitoredTrainingSession(checkpoint_dir=checkpoint_dir,hooks=hooks, config=config) as mon_sess:
        while not mon_sess.should_stop():
            # Run a training step synchronously.
            j = 0
            batch_start_idx = 0
            for i in range(steps):
                if (i % 50 == 0 and i != 0):
                    j = j + 1
                if datapoint_size == batch_size:
                    batch_start_idx = 0
                elif datapoint_size < batch_size:
                    raise ValueError(
                        "datapoint_size: %d, must be greater than batch_size: %d” " % (datapoint_size, batch_size))
                else:
                    batch_start_idx = (j * batch_size) % (datapoint_size - batch_size)
                    batch_end_idx = batch_start_idx + batch_size
                    batch_numbers = range(batch_start_idx, batch_end_idx)
                    batch_user_indecies = np.array(df_train.user.values[batch_numbers]).astype(np.int32)
                    batch_item_indecies = np.array(df_train.item.values[batch_numbers]).astype(np.int32)
                    batch_rates = np.array(df_train.rate.values[batch_numbers]).astype(float)
                    feed = {user_indecies: batch_user_indecies, item_indecies: batch_item_indecies,
                            rates: batch_rates, }
                    mon_sess.run(training_step, feed_dict=feed)
                #if (i % 10 == 0): # 20
                #    print("le cout a l'indice " + str(i) + " est : " + str(mon_sess.run(cost, feed_dict=feed)))
                print("le cout a l'indice " + str(i) + " est : " + str(mon_sess.run(cost, feed_dict=feed)))

            res = result.eval(session=mon_sess)
            err = mon_sess.run(true_cost)
            return res, err


def build_Tensorflow_Engine_With_Horovod():
    # Horovod: initialize Horovod.
    hvd.init()

    # Path of ratings file
    path = '../ratings.csv'
    path_User_Recommend_Opp = '../Users_Recommendations'

    while True:
        if os.access(path, os.F_OK):
            if os.access(path, os.R_OK):
                df_train, users_number, items_number = read_in_csv_file(path)
                if not df_train.empty:
                    matrix, err = buid_Tensorflow_Engine_Model(df_train=df_train, users_number=users_number,
                                                               items_number=items_number
                                                               , steps=5, batch_size=100, feature_len=10)
                    # dispatch(matrix, path_User_Recommend_Opp)
                    print("NEXT LECTURE IN RATINGS FILE >>>")
                else:
                    print("MATRIX IS EMPTY >>>")
            else:
                print(path+" does not reading yet")
        else:
            print(path+" does not existing yet")


def main(_):
    build_Tensorflow_Engine_With_Horovod()


if __name__ == "__main__":
    tf.app.run()
