<h1>Musixcloud-Python Flask Web Appilication (<a href="https://app.musixcloud.com/" target="_blank" >PREVIEW</a>)</h1>
<img src="static/logo.png" style="position: relative; left: 50%; transform: translateX(-50%)">
<br>
<strong>Table of Contents</strong>
<br>
<a href="#Description">
Description
</a>
<br>
<a href="#Features">
Features
</a>
<br>
<a href="#Screenshot">
Screenshot
</a>
<br>
<a href="#Prequisites">
Prequisites
</a>
<br>
<a href="#install">
How To Install
</a>
<br>
<a href="#started">
Getting Started
</a>
<br>
<a href="#Upgrade">
Upgrade
</a>
<br>
<a href="#Conclusion">
Conclusion
</a>
<br>
<strong id="Description">Description (<a href="#Features">SKIP</a>)</strong>
<p>
musixcloud is a music streaming and audio distribution platform. musixcloud is a music library which enables it's user to access it's products with no complexity, the interface is more flexible to communicate with by the end users without been stressful.  This platform is build basically to bring you closer to that leisure moment you have always wanted.
</p>
<strong id="Features">Features (<a href="#Screenshot">SKIP</a>)</strong>
<ul>
<li>
Music streaming
</li>
<li>
Music download
</li>
<li>
Sychronising music with lyrics ( You dont really need to understand the language of the artist the app will interpreat )
</li>
<li>
Music playlist
</li>
<li>
User Profile with personalize songs
</li>
<li>
Push notification ( keep users aware of latest song upload and advert using it customize notification )
</li>
<li>
Admin panel 
</li>
</ul>
<strong id="Screenshot">Screenshot (<a href="#Prequisites">SKIP</a>)</strong>
<div style="display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-around">
<img src="screenshot/Opera Snapshot_2021-10-05_175541_app.musixcloud.com.png" style="width: 400px; height: 300px; margin-bottom: 10px">
<img src="screenshot/Opera Snapshot_2021-10-05_175613_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">
<img src="screenshot/Opera Snapshot_2021-10-05_175637_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">
<img src="screenshot/bandicam 2020-10-19 22-20-26-608.jpg" style="width: 400px; height: 300px; margin-bottom: 10px">
<img src="screenshot/Opera Snapshot_2021-10-05_175658_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">
<img src="screenshot/Opera Snapshot_2021-10-05_175750_accounts.google.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">

<img src="screenshot/Opera Snapshot_2021-10-05_202958_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">

<img src="screenshot/Opera Snapshot_2021-10-05_175819_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">
<img src="screenshot/Opera Snapshot_2021-10-05_175911_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">
<img src="screenshot/Opera Snapshot_2021-10-05_175935_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">
<img src="screenshot/Opera Snapshot_2021-10-05_180135_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">
<img src="screenshot/Opera Snapshot_2021-10-05_175715_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">
<img src="screenshot/Opera Snapshot_2021-10-05_180153_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">
<img src="screenshot/Opera Snapshot_2021-10-05_180247_app.musixcloud.com.png" style="width: 400px; height: 300px ; margin-bottom: 10px">
<div>
<strong id="Prequisites" >
Prequisites (<a href="#install">SKIP</a>)
</strong>
<ol>
<li>
<h4>Google Authentication (<a href="#https://developers.google.com/identity/sign-in/web/sign-in" target="_blank" >Visit</a>)</h4>
<p>
Visit google developer console and create an app for this case Musixcloud Demo App and grap your the following from your console and replace it in app.py bellow. 
<br>
<code>
	client_id=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX,
	client_secret=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX,
</code>
<br>
<a href="#Python">Skip</a> to next step
</p>
</li>

<li>
<h4 id="Python">Python (<a href="#https://www.python.org/downloads/" target="_blank" >Visit</a>)</h4>
<p>
Musixcloud web server is powerby python to get started ensure you have python install on your pc and it available in your system environment variable. For Ubuntu users python is install by default so <a href="#pip">Skip</a> to next step. Open up your terminal (linux) or command prompt (windows) and type in the bellow code
<br>
<code>
	python --version<br>
    Python 3.9.7
</code>
</p>
</li>

<li id="pip">
<h4>PIP</h4>
<p>
Python Install Package is a package manager for python appications, for this project it will be use to install the dependecies of the app. Visit PIP website for instruction on how to install on your operation system. You can also confirm if you already have it install with the code below
<br>
<code>
	pip --version<br>
    pip 21.2.4 from C:\Users\Psalm\AppData\Local\Programs\Python\Python39\lib\site-packages\pip (python 3.9)
</code>
<a href="#env">Skip</a> to next step if you have it installed<br>
Or install using
<code>
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py<br>
    python get-pip.py
</code>
</p>
</li>

<li id="env">
<h4>Virtual Environment (<a href="#https://pypi.org/project/virtualenv/" target="_blank" >Visit</a>)</h4>
<p>
In a python appilication your virtual environment is where all package partaining the appilication is installed, for this app all package must be install in an activated environment else appilication will return an error
<br>
<code>
	virtualenv --version<br>
    virtualenv 20.8.1 from C:\Users\Psalm\AppData\Local\Programs\Python\Python39\lib\site-packages\virtualenv\__init__.py
</code>
<br>
</p>
<code>
pip install virtualenv
</code>
</li>
</ol>
<strong id="install" >
How To Install (<a href="#started">SKIP</a>)
</strong>
<p>
At this point your pc is ready to go ahead with the installation of this web application. Please following the step below carefully;
<ol>
<Strong>
Steps
</strong>
<li>
Clone the repo using 
<br>
<code>
git clone https://github.com/Samuel-Momoh/Musixcloud.git
</code>
Or download zip file directly from this repository
<br>
</li>
<li>
Start by creating a virtual environment
<br>
<code>
virtualenv env
</code>
<br>
</li>
<li>
Activate your virtual environment using the code below
<br>
<Strong>
Windows
</strong>
<br>
<code>
env\Scripts\activate
</code>
<br>
<Strong>
Ubuntu
</strong>
<br>
<code>
 Source env/bin/activate
</code>
</li>
<li>
Change to the app directory and install the app using pip
<br>

<code>
cd app
</code>
<br>
<code>
 pip install -r requirement.txt
</code>
</li>
<li>
App is now  ready to be serve, start the app by running the below code 
<br>
<code>
flask run
</code>
Follow this <a href="http://127.0.0.1:5000/" target="_blank" >LInk</a> <code>http://127.0.0.1:5000/ </code>open the app in your favorite browser and enjoy
</li>
</ol>
</p>
<Strong id="started">
Getting Started (<a href="#Upgrade">SKIP</a>)
</strong>
<p>
The current source will initialise as an empty app, to get started with streaming songs you will have to upload the following from the admin panel. Follow this link  <a href="http://127.0.0.1:5000/admin" target="_blank" >Link</a> <code>http://127.0.0.1:5000/admin </code>
<br>
<code>
email: admin@example.com<br> 
password: admin
</code>
<br>
<ul>
<li>
Navigate to genre and create a genre of music
</li>
<li>
Navigate to song and upload your desired music
</li>
<li>
You can also upload an artist profile musixcloud app will automatically load all songs associated with the artist in it database and display on the artist profile on the streaming app
</li>
</ul>
</p>
<Strong id="Upgrade">
Upgrade (<a href="#Conclusion">SKIP</a>)
</strong>
<ul>
<li>
Hash admin password in database
</li>
<li>
Add share button
</li>
<li>
Add comment to the app
</li>
<li>
Create a manager panel for artist manager
</li>
<li>
Build the mobile app using react native
</li>
</ul>
<Strong id="Conclusion" >
Conclusion (<a href="#">SKIP</a>)
</strong>
<p>
Thank you for going through this app, i hope you find it helpful and meets your need. To contribute to this project please feel free to submit a pull request. Should you be having problem with setting up the app feel free to send an mail to <a href="mailto:samueldan@live.com">samueldan@live.com</a>
</p>