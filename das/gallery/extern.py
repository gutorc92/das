import numpy as np
import caffe
import os
import sys
import cv2
import urllib2
import urllib

dic_root = "/home/gustavo/Documents/unb/das/trabalhofinal/das/gallery"
caffe_root = "/home/gustavo/caffe"

class NetFace:
	def __init__(self):
		path = os.path.join(dic_root,"haarcascade_frontalface_alt.xml")
		self.classifier = cv2.CascadeClassifier(path)
	def classifierImage(self,miniframe):
		return self.classifier.detectMultiScale(miniframe)

class Face:
	def __init__(self,net=NetFace()):
		self.net = net
	
	def detect(self,frame):
		height, width, depth = frame.shape

		# create grayscale version
		grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	 
		# equalize histogram
		cv2.equalizeHist(grayscale, grayscale)

		# detect objects
		DOWNSCALE = 4
		minisize = (frame.shape[1]/DOWNSCALE,frame.shape[0]/DOWNSCALE)
		miniframe = cv2.resize(frame, minisize)
		faces = self.net.classifierImage(miniframe)
		#if len(faces)>0:
			# print 'face detected!'
		#	for i in faces:
		#		x, y, w, h = [ v*DOWNSCALE for v in i ]
		#		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0))
		#cv2.imshow('frame',frame)
		#cv2.waitKey(0)
		#print("Faces: ", len(faces))
		return faces

class Net:

	def __init__(self):
		self.create_net()
		self.create_mu()
		self.create_transformer()
		self.create_labels()
		self.loadsynset()

	def create_transformer(self):
		self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
		self.transformer.set_transpose('data', (2,0,1))
		self.transformer.set_mean('data', self.mu)      
		self.transformer.set_raw_scale('data', 255)      
		self.transformer.set_channel_swap('data', (2,1,0)) 
		
	def create_mu(self):
		self.mu = np.load(os.path.join(caffe_root, 'python','caffe','imagenet','ilsvrc_2012_mean.npy'))
		self.mu = self.mu.mean(1).mean(1)  


	def create_net(self):
		model_weights = os.path.join(caffe_root, 'models','bvlc_reference_caffenet','bvlc_reference_caffenet.caffemodel')
		model_def = os.path.join(caffe_root, 'models', 'bvlc_reference_caffenet','deploy.prototxt')
		self.net = caffe.Net(model_def,model_weights,caffe.TEST)

	def create_labels(self):
		labels_file = os.path.join(caffe_root, 'data','ilsvrc12','synset_words.txt')
		self.labels = np.loadtxt(labels_file, str, delimiter='\t') 
		

	def loadsynset(self):
		f = open(os.path.join(dic_root,"synset_cats"),"r")
		self.cats = f.read().splitlines()
		f.close()
		f = open(os.path.join(dic_root,"synset_dogs"),"r")
		self.dogs = f.read().splitlines()
		f.close()


	def predict_imageNet(self,image_filename):
		image = caffe.io.load_image(image_filename)
		self.net.blobs['data'].data[...] = self.transformer.preprocess('data', image)

		# perform classification
		self.net.forward()

		# obtain the output probabilities
		output_prob = self.net.blobs['prob'].data[0]

		# sort top five predictions from softmax output
		top_inds = output_prob.argsort()[::-1][:5]


		predictions = zip(output_prob[top_inds], self.labels[top_inds])

		return predictions

	def result(self,img):
		predictions = self.predict_imageNet(img)
		total_dogs = 0
		total_cats = 0
		for per, cls in predictions:
			if cls.split()[0] in self.cats:
				total_cats += per
			elif cls.split()[0] in self.dogs:
				total_dogs += per		
		return total_dogs*100,total_cats*100

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
        plt.figure(figsize=(5, 1))
        plt.plot(x)
        plt.title('Query vector')

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
            plt.figure()
            plt.imshow(image)
            plt.axis('off')
            if self.labels.shape[0]==0:
                plt.title('im. idx=%d' % idx)
            else: # Show top label in the title, if possible:
                top_inds = self.Xtr[idx].argsort()[::-1][:5]
                plt.title('%s   im. idx=%d' % (labels[top_inds[0]][10:], idx))
                
            # The next 3 lines are for debugging purposes:
            plt.figure(figsize=(5, 1))
            plt.plot(self.Xtr[idx])       
            plt.title('Vector of the element ranked %d' % n)


def get_hist(filename):
    image =  misc.imread(filename)
    image = image[::4,::4,:]
    # Normalizing images:
    im_norm = (image-image.mean())/image.std()
    
    # Computing a 10-bin histogram in the range [-e, +e] (1 standard deviationto 255 for each of the colours:
    # (the first element [0] is the histogram, the second [1] is the array of bins.)
    hist_red = np.histogram(im_norm[:,:,0], range=(-np.e,+np.e))[0] 
    hist_green = np.histogram(im_norm[:,:,1], range=(-np.e,+np.e))[0]
    hist_blue = np.histogram(im_norm[:,:,2], range=(-np.e,+np.e))[0]
    # Concatenating them into a 30-dimensional vector:
    histogram = np.concatenate((hist_red, hist_green, hist_blue)).astype(np.float)
    return histogram/histogram.sum()

def load_dataset_hist(images_path):
    # Load/build a dataset of vectors (i.e. a big matrix) of RGB histograms.
    vectors_filename = os.path.join(images_path, 'vectors_hist.h5')

    if os.path.exists(vectors_filename):
        print 'Loading image signatures (colour histograms) from ' + vectors_filename
        with h5py.File(vectors_filename, 'r') as f:
            vectors = f['vectors'][()]
            img_files = f['img_files'][()]

    else:
        # Build a list of JPG files (change if you want other image types):
        os.listdir(images_path)
        img_files = [f for f in os.listdir(images_path) if (('jpg' in f) or ('JPG') in f)]

        print 'Loading all images to the memory and pre-processing them...'
        vectors = np.zeros((len(img_files), 30))
        for (f,n) in zip(img_files, range(len(img_files))):
            print '%d %s'% (n,f)
            vectors[n] = get_hist(os.path.join(images_path, f))
                    
        print 'Saving descriptors and file indices to ' + vectors_filename
        with h5py.File(vectors_filename, 'w') as f:
            f.create_dataset('vectors', data=vectors)
            f.create_dataset('img_files', data=img_files)
    
    return vectors, img_files

class Input:

	FACES = 1
	PREDICTION = 2
	def __init__(self, load=None):
		self.img = None
		if(load): self.resolve(load)

	def resolve(self,load):
		if(self.isFile(load)):
			self.fileResolver(load)	
		elif(self.isUrl(load)):
			self.urlResolver(load)

	def isFile(self,load):
		return os.path.isfile(load)
	def isUrl(self,load):
		try:
			urllib2.urlopen(load)
			return True
		except urllib2.HTTPError, e:
			return False
		except urllib2.URLError, e:
			return False
		return False
			
	def fileResolver(self,load):
		self.img = cv2.imread(load)
		self.load = load

	def urlResolver(self,load):
		image = urllib.URLopener()
		path = os.path.join(dic_root,"0000001.jpg")
		image.retrieve(load,path)
		image.close()
		self.fileResolver(path)
		return None
	
	def getImage(self,destination):
		if(destination == self.FACES):
			return self.img
		else:
			return self.load

class Output:
	
	def outFaces(self,faces):
		if(len(faces) > 0):
			print("Foram detectadas {0} faces").format(str(len(faces)))
			print("As coordendas das faces: ")
			for face in faces:
				print(face)
		else:
			print("Nao foram encontradas faces")
	
	def outAnimals(self,dogs,cats):
		if(dogs > 0):
			print("A probabilidade de haver caninos na imagem e de: {0}").format(str(dogs))
		else:
			print("Nao ha caninos na imagem")
		if(cats > 0):
			print("A probabilidade de haver felinos na imagem e de: {0}").format(str(cats))
		else:
			print("Nao ha felinos na imagem")
