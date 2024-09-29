from .utils import *
from .config import *


from .suppress_warnings import suppress_warnings

import warnings
from contextlib import contextmanager
import logging

# Suppress absl warnings
import absl.logging
absl.logging.set_verbosity('error')
# Suppress TensorFlow warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
with suppress_warnings():
    import tensorflow as tf
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
dtype = tf.float32
import pickle

class Restore_NN(tf.keras.Model):

    def __init__(self, 
                 parameters=None, 
                 modes=None, 
                 parameters_mean=None, 
                 parameters_std=None, 
                 features_mean=None, 
                 features_std=None, 
                 n_hidden=[512,512,512], 
                 restore=False, 
                 restore_filename=None, 
                 trainable=True,
                 optimizer=None,
                 verbose=False, 
                 ):
        
        # super
        super(Restore_NN, self).__init__()

        # restore
        
        self.restore(restore_filename)


        # input parameters mean and std
        self.parameters_mean = tf.constant(self.parameters_mean_, dtype=dtype, name='parameters_mean')
        self.parameters_std = tf.constant(self.parameters_std_, dtype=dtype, name='parameters_std')

        # (log)-spectra mean and std
        self.features_mean = tf.constant(self.features_mean_, dtype=dtype, name='features_mean')
        self.features_std = tf.constant(self.features_std_, dtype=dtype, name='features_std')

        # weights, biases and activation function parameters for each layer of the network
        self.W = []
        self.b = []
        self.alphas = []
        self.betas = [] 
        for i in range(self.n_layers):
            self.W.append(tf.Variable(tf.random.normal([self.architecture[i], self.architecture[i+1]], 0., 1e-3), name="W_" + str(i), trainable=trainable))
            self.b.append(tf.Variable(tf.zeros([self.architecture[i+1]]), name = "b_" + str(i), trainable=trainable))
        for i in range(self.n_layers-1):
            self.alphas.append(tf.Variable(tf.random.normal([self.architecture[i+1]]), name = "alphas_" + str(i), trainable=trainable))
            self.betas.append(tf.Variable(tf.random.normal([self.architecture[i+1]]), name = "betas_" + str(i), trainable=trainable))

        # restore weights if restore = True

        for i in range(self.n_layers):
            self.W[i].assign(self.W_[i])
            self.b[i].assign(self.b_[i])
        for i in range(self.n_layers-1):
            self.alphas[i].assign(self.alphas_[i])
            self.betas[i].assign(self.betas_[i])

        # optimizer
        self.optimizer = optimizer or tf.keras.optimizers.Adam()
        self.verbose= verbose

        # print initialization info, if verbose
        if self.verbose:
            multiline_str = "\nInitialized cosmopower_NN model, \n" \
                            f"mapping {self.n_parameters} input parameters to {self.n_modes} output modes, \n" \
                            f"using {len(self.n_hidden)} hidden layers, \n" \
                            f"with {list(self.n_hidden)} nodes, respectively. \n"
            print(multiline_str)


    # restore attributes
    def restore(self, 
                filename
                ):
        r"""
        Load pre-trained model

        Parameters:
            filename (str):
                filename tag (without suffix) where model was saved
        """
        # load attributes
        with open(filename + ".pkl", 'rb') as f:
            self.W_, self.b_, self.alphas_, self.betas_, \
            self.parameters_mean_, self.parameters_std_, \
            self.features_mean_, self.features_std_, \
            self.n_parameters, self.parameters, \
            self.n_modes, self.modes, \
            self.n_hidden, self.n_layers, self.architecture = pickle.load(f)



    # auxiliary function to sort input parameters
    def dict_to_ordered_arr_np(self, 
                               input_dict, 
                               ):
        r"""
        Sort input parameters

        Parameters:
            input_dict (dict [numpy.ndarray]):
                input dict of (arrays of) parameters to be sorted

        Returns:
            numpy.ndarray:
                parameters sorted according to desired order
        """
        if self.parameters is not None:
            return np.stack([input_dict[k] for k in self.parameters], axis=1)
        else:
            return np.stack([input_dict[k] for k in input_dict], axis=1)


    # forward prediction given input parameters implemented in Numpy
    def forward_pass_np(self, 
                        parameters_arr
                        ):
        r"""
        Forward pass through the network to predict the output, 
        fully implemented in Numpy

        Parameters:
            parameters_arr (numpy.ndarray):
                array of input parameters

        Returns:
          numpy.ndarray:
            output predictions
        """
        # forward pass through the network
        act = []
        layers = [(parameters_arr - self.parameters_mean_)/self.parameters_std_]
        for i in range(self.n_layers-1):

            # linear network operation
            act.append(np.dot(layers[-1], self.W_[i]) + self.b_[i])

            # pass through activation function
            layers.append((self.betas_[i] + (1.-self.betas_[i])*1./(1.+np.exp(-self.alphas_[i]*act[-1])))*act[-1])

        # final (linear) layer -> (standardised) predictions
        layers.append(np.dot(layers[-1], self.W_[-1]) + self.b_[-1])

        # rescale and output
        return layers[-1]*self.features_std_ + self.features_mean_


    # Numpy array predictions
    def predictions_np(self, 
                       parameters_dict
                       ):
        r"""
        Predictions given input parameters collected in a dict.
        Fully implemented in Numpy. Calls ``forward_pass_np``
        after ordering the input parameter dict

        Parameters:
            parameters_dict (dict [numpy.ndarray]):
                dictionary of (arrays of) parameters

        Returns:
            numpy.ndarray:
                output predictions
        """
        parameters_arr = self.dict_to_ordered_arr_np(parameters_dict)
        return self.forward_pass_np(parameters_arr)


    # Numpy array 10.**predictions
    def ten_to_predictions_np(self,
                            parameters_dict
                            ):
        r"""
        10^predictions given input parameters collected in a dict.
        Fully implemented in Numpy. It raises 10 to the output
        from ``forward_pass_np``

        Parameters:
            parameters_dict (dict [numpy.ndarray]):
                dictionary of (arrays of) parameters

        Returns:
            numpy.ndarray:
                10^output predictions
        """
        return 10.**self.predictions_np(parameters_dict)


class Restore_PCAplusNN(tf.keras.Model):

    def __init__(self, 
                 cp_pca=None,
                 n_hidden=[512,512,512], 
                 restore=False, 
                 restore_filename=None, 
                 trainable=True, 
                 optimizer=None,
                 verbose=False,
                 ):
        r"""
        Constructor.
        """
        # super
        super(Restore_PCAplusNN, self).__init__()


        self.restore(restore_filename)

        # input parameters mean and std
        self.parameters_mean = tf.constant(self.parameters_mean_, dtype=dtype, name='parameters_mean')
        self.parameters_std = tf.constant(self.parameters_std_, dtype=dtype, name='parameters_std')

        # PCA mean and std
        self.pca_mean = tf.constant(self.pca_mean_, dtype=dtype, name='pca_mean')
        self.pca_std = tf.constant(self.pca_std_, dtype=dtype, name='pca_std')

        # (log)-spectra mean and std
        self.features_mean = tf.constant(self.features_mean_, dtype=dtype, name='features_mean')
        self.features_std = tf.constant(self.features_std_, dtype=dtype, name='features_std')

        # pca transform matrix
        self.pca_transform_matrix = tf.constant(self.pca_transform_matrix_, dtype=dtype, name='pca_transform_matrix')

        # weights, biases and activation function parameters for each layer of the network
        self.W = []
        self.b = []
        self.alphas = []
        self.betas = [] 
        for i in range(self.n_layers):
            self.W.append(tf.Variable(tf.random.normal([self.architecture[i], self.architecture[i+1]], 0., np.sqrt(2./self.n_parameters)), name="W_" + str(i), trainable=trainable))
            self.b.append(tf.Variable(tf.zeros([self.architecture[i+1]]), name = "b_" + str(i), trainable=trainable))
        for i in range(self.n_layers-1):
            self.alphas.append(tf.Variable(tf.random.normal([self.architecture[i+1]]), name = "alphas_" + str(i), trainable=trainable))
            self.betas.append(tf.Variable(tf.random.normal([self.architecture[i+1]]), name = "betas_" + str(i), trainable=trainable))

        # restore weights if restore = True
        for i in range(self.n_layers):
            self.W[i].assign(self.W_[i])
            self.b[i].assign(self.b_[i])
        for i in range(self.n_layers-1):
            self.alphas[i].assign(self.alphas_[i])
            self.betas[i].assign(self.betas_[i])

        self.optimizer = optimizer or tf.keras.optimizers.Adam()
        self.verbose= verbose

        # print initialization info, if verbose
        if self.verbose:
            multiline_str = "\nInitialized cosmopower_PCAplusNN model, \n" \
                            f"mapping {self.n_parameters} input parameters to {self.n_pcas} PCA components \n" \
                            f"and then inverting the PCA compression to obtain {self.n_modes} modes \n" \
                            f"The model uses {len(self.n_hidden)} hidden layers, \n" \
                            f"with {list(self.n_hidden)} nodes, respectively. \n"
            print(multiline_str)



    # restore attributes
    def restore(self, 
                filename,
                ):
        r"""
        Load pre-trained model

        Parameters:
            filename (str):
                filename tag (without suffix) where model was saved
        """
        # load attributes
        f = open(filename + ".pkl", 'rb')
        self.W_, self.b_, self.alphas_, self.betas_, \
        self.parameters_mean_, self.parameters_std_, \
        self.pca_mean_, self.pca_std_, \
        self.features_mean_, self.features_std_, \
        self.parameters, self.n_parameters, \
        self.modes, self.n_modes, \
        self.n_pcas, self.pca_transform_matrix_, \
        self.n_hidden, self.n_layers, self.architecture = pickle.load(f)
        f.close()




    # auxiliary function to sort input parameters
    def dict_to_ordered_arr_np(self, 
                               input_dict, 
                               ):
        r"""
        Sort input parameters

        Parameters:
            input_dict (dict [numpy.ndarray]):
                input dict of (arrays of) parameters to be sorted

        Returns:
            numpy.ndarray:
                parameters sorted according to desired order
        """
        if self.parameters is not None:
            return np.stack([input_dict[k] for k in self.parameters], axis=1)
        else:
            return np.stack([input_dict[k] for k in input_dict], axis=1)


    # forward prediction given input parameters implemented in Numpy
    def forward_pass_np(self, 
                        parameters_arr,
                        ):
        r"""
        Forward pass through the network to predict the output, 
        fully implemented in Numpy

        Parameters:
            parameters_arr (numpy.ndarray):
                array of input parameters

        Returns:
          numpy.ndarray:
            output predictions
        """
        # forward pass through the network
        act = []
        layers = [(parameters_arr - self.parameters_mean_)/self.parameters_std_]
        for i in range(self.n_layers-1):

            # linear network operation
            act.append(np.dot(layers[-1], self.W_[i]) + self.b_[i])

            # pass through activation function
            layers.append((self.betas_[i] + (1.-self.betas_[i])*1./(1.+np.exp(-self.alphas_[i]*act[-1])))*act[-1])

        # final (linear) layer -> (normalized) PCA coefficients
        layers.append(np.dot(layers[-1], self.W_[-1]) + self.b_[-1])

        # rescale PCA coefficients, multiply out PCA basis -> normalised (log)-spectrum, shift and re-scale (log)-spectrum -> output (log)-spectrum
        return np.dot(layers[-1]*self.pca_std_ + self.pca_mean_, self.pca_transform_matrix_)*self.features_std_ + self.features_mean_


    def predictions_np(self, 
                       parameters_dict,
                       ):
        r"""
        Predictions given input parameters collected in a dict.
        Fully implemented in Numpy. Calls ``forward_pass_np``
        after ordering the input parameter dict

        Parameters:
            parameters_dict (dict [numpy.ndarray]):
                dictionary of (arrays of) parameters

        Returns:
            numpy.ndarray:
                output predictions
        """
        parameters_arr = self.dict_to_ordered_arr_np(parameters_dict)
        return self.forward_pass_np(parameters_arr)


    # 10.**predictions
    def ten_to_predictions_np(self,
                              parameters_dict,
                              ):
        r"""
        10^predictions given input parameters collected in a dict.
        Fully implemented in Numpy. It raises 10 to the output
        from ``forward_pass_np``

        Parameters:
            parameters_dict (dict [numpy.ndarray]):
                dictionary of (arrays of) parameters

        Returns:
            numpy.ndarray:
                10^output predictions
        """
        return 10.**self.predictions_np(parameters_dict)
