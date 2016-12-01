## Dependencies
In order to run the program properly, it's necessary to assegure that the pc has:
- [OpenCV 2.4.13](http://opencv.org/downloads.html)
- [Caffe](http://caffe.berkeleyvision.org/installation.html)*

*After installing caffe, run in terminal:
  - `$ ~/caffe/scripts/download_model_binary.py ~/caffe/models/bvlc_reference_caffenet`
  - `$ ~/caffe/data/ilsvrc12/get_ilsvrc_aux.sh`
  
## Installation
- Clone the repository: 
  - `$ https://www.github.com/gutorc92/das.git`
- Get inside the cloned folder: 
  - `$ cd das`
- Install the requirements: 
  - `$ pip install -r requirements.txt`
- Go to the app: 
  - `$ cd das` ('das' in this case is another folder inside the previous 'das' folder)
- Create the database: 
  - `$ python manage.py makemigrations gallery`
- Migrate the data to schema: 
  - `$ python manage.py migrate`
  
## Running the Project
- Run in terminal:
  - `$ python manage.py runserver`
  
The project will run, by default, in `localhost:8000`
