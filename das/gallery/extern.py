import numpy as np
import caffe
import os
import sys
import cv2
import urllib
from scipy import misc
import h5py # to save/load data files
import matplotlib.pyplot as plt


labels = []

home_dir = os.getenv("HOME")
caffe_root = os.path.join(home_dir, "caffe")

caffe.set_mode_cpu()

model_def = os.path.join(caffe_root, 'models', 'bvlc_reference_caffenet','deploy.prototxt')
model_weights = os.path.join(caffe_root, 'models','bvlc_reference_caffenet','bvlc_reference_caffenet.caffemodel')

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)

# load the mean ImageNet image (as distributed with Caffe) for subtraction
mu = np.load(os.path.join(caffe_root, 'python','caffe','imagenet','ilsvrc_2012_mean.npy'))
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR


labels_file = os.path.join(caffe_root, 'data','ilsvrc12','synset_words.txt')
labels = np.loadtxt(labels_file, str, delimiter='\t')

def load_dataset(images_path):
    # Load/build a dataset of vectors (i.e. a big matrix) of probabilities
    # from the ImageNet ILSVRC 2012 challenge using Caffe.
    vectors_filename = os.path.join(images_path, 'vectors.h5')

    if os.path.exists(vectors_filename):
        print 'Loading image signatures (probability vectors) from ' + vectors_filename
        with h5py.File(vectors_filename, 'r') as f:
            vectors = f['vectors'][()]
            img_files = f['img_files'][()]

    else:
        # Build a list of JPG files (change if you want other image types):
        os.listdir(images_path)
        img_files = [f for f in os.listdir(images_path) if (('jpg' in f) or ('JPG') in f)]

        #print 'Loading all images to the memory and pre-processing them...'

        net_data_shape = net.blobs['data'].data.shape
        train_images = np.zeros(([len(img_files)] + list(net_data_shape[1:])))

        for (f,n) in zip(img_files, range(len(img_files))):
            print '%d %s'% (n,f)
            image = caffe.io.load_image(os.path.join(images_path, f))
            train_images[n] = transformer.preprocess('data', image)

        #print 'Extracting descriptor vector (classifying) for all images...'
        vectors = np.zeros((train_images.shape[0],1000))
        for n in range(0,train_images.shape[0],10): # For each batch of 10 images:
            # This block can/should be parallelised!
            #print 'Processing batch %d' % n
            last_n = np.min((n+10, train_images.shape[0]))

            net.blobs['data'].data[0:last_n-n] = train_images[n:last_n]

            # perform classification
            net.forward()

            # obtain the output probabilities
            vectors[n:last_n] = net.blobs['prob'].data[0:last_n-n]

        #print 'Saving descriptors and file indices to ' + vectors_filename
        with h5py.File(vectors_filename, 'w') as f:
            f.create_dataset('vectors', data=vectors)
            f.create_dataset('img_files', data=img_files)

    return vectors, img_files

def predict_imageNet(image_filename):
    image = caffe.io.load_image(image_filename)
    net.blobs['data'].data[...] = transformer.preprocess('data', image)

    # perform classification
    net.forward()

    # obtain the output probabilities
    output_prob = net.blobs['prob'].data[0]

    # sort top five predictions from softmax output
    top_inds = output_prob.argsort()[::-1][:5]

    #plt.imshow(image)
    #plt.axis('off')

    #print 'probabilities and labels:'
    #predictions = zip(output_prob[top_inds], labels[top_inds]) # showing only labels (skipping the index)
    #for p in predictions:
    #    print p

    # plt.figure(figsize=(15, 3))
    # plt.plot(output_prob)
    return output_prob


class NearestNeighbors:
    def __init__(self, K=10, Xtr=[], images_path='Photos/', img_files=[], labels=np.empty(0)):
        # Setting defaults
        self.K = K
        self.Xtr = Xtr
        self.images_path = images_path
        self.img_files = img_files
        self.labels = labels

    def setXtr(self, Xtr):
        """ X is N x D where each row is an example."""
        # the nearest neighbor classifier simply remembers all the training data
        self.Xtr = Xtr

    def setK(self, K):
        """ K is the number of samples to be retrieved for each query."""
        self.K = K

    def setImagesPath(self,images_path):
        self.images_path = images_path

    def setFilesList(self,img_files):
        self.img_files = img_files

    def setLabels(self,labels):
        self.labels = labels

    def predict(self, x):
        """ x is a test (query) sample vector of 1 x D dimensions """

        # Compare x with the training (dataset) vectors
        # using the L1 distance (sum of absolute value differences)

        # p = 1.
        # distances = np.power(np.sum(np.power(np.abs(X-x),p), axis = 1), 1./p)
        distances = np.sum(np.abs(self.Xtr-x), axis = 1)
        # distances = 1-np.dot(X,x)

        # plt.figure(figsize=(15, 3))
        # plt.plot(distances)
        # print np.argsort(distances)
        return np.argsort(distances) # returns an array of indices of of the samples, sorted by how similar they are to x.

    def retrieve(self, x):
        # The next 3 lines are for debugging purposes:
        #plt.figure(figsize=(5, 1))
        #plt.plot(x)
        #plt.title('Query vector')

        nearest_neighbours = self.predict(x)
        for n in range(self.K):
            idx = nearest_neighbours[n]

            # predictions = zip(self.Xtr[idx][top_inds], labels[top_inds]) # showing only labels (skipping the index)
            # for p in predictions:
            #     print p

            ##
            # In the block below, instead of just showing the image in Jupyter notebook,
            # you can create a website showing results.
            image =  misc.imread(os.path.join(self.images_path, self.img_files[idx]))
            if self.labels.shape[0]==0:
                print("Teste")
            else: # Show top label in the title, if possible:
                top_inds = self.Xtr[idx].argsort()[::-1][:5]
                print('%s   im. idx=%d' % (labels[top_inds[0]][10:], idx))



def make():
    images_path = "../images"
    vectors, img_files = load_dataset(images_path)
    KNN = NearestNeighbors(Xtr=vectors, img_files=img_files, images_path=images_path, labels=labels)
    img = "../images/2b97481.jpg"
    KNN.retrieve(predict_imageNet(img))
