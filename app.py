import os
import sys
import sqlite3
import json
import math
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote



sys.path.insert(0, os.path.dirname(__file__))
from flask import Flask,url_for,render_template,redirect,request,jsonify,flash,session,get_flashed_messages,make_response
from flask.helpers import make_response
from werkzeug.utils import secure_filename
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.id3 import ID3, TIT2
from mutagen.easyid3 import EasyID3
#  google authentication
from authlib.integrations.flask_client import OAuth
# Protection from other server
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
# Site map genration
from flask_sitemap import Sitemap
# pywebpush
from pywebpush import webpush, WebPushException

app = Flask(__name__)
app.secret_key='Nigeria\'s First Music Library'
csrf.init_app(app)
ext = Sitemap(app=app)
app.config.from_object('config')



CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
	client_id='211692313962-iv1obdoaisa126uihig80l7kodkqjgqk.apps.googleusercontent.com',
	client_secret='mp8Eomf9cgGBRzt2sfDdLFNi',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
# Create a directory in a known location to save files to.
uploads_dir_song = os.path.join('static/songs')
uploads_dir_image = os.path.join('static/album-art')





# Index page
@app.route("/",methods=["POST","GET"])
def index():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	cur=conn.cursor()
	data=c.execute("select rowid,* from music where status='active' ORDER by count + like + downloads DESC LIMIT 8")
	state = cur.execute("select rowid,* from music where status='active' ORDER by count + like + downloads DESC LIMIT 8").fetchone()
	return render_template("index.html",data=data, state=state)
# Index page
@app.route("/<artist>",methods=["POST","GET"])
def direct_link(artist):

	return redirect("artist/"+artist)
#Genre page
@app.route("/genre",methods=["POST","GET"])
def genre():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	data=c.execute("SELECT rowid,* from genre")
	return render_template("genre.html",data=data)
# Calculate
def calculate(url):
	url = './static/songs/'+url
	audio = MP3(url)
	# audio = MP3('./static/songs/clean_live_hillsong_united_mp3_6583.mp3')
	duration = audio.info.length
	hours = math.floor((duration)/3600)
	minute = math.floor((duration - (hours * 3600)) / 60)
	seconds = math.floor(duration - (hours * 3600) - (minute * 60))
	if(seconds < 10):
		seconds = "0" + str(seconds)
	songduration = str(minute) + ':' + str(seconds)
	return songduration
#Genre list page
@app.route("/genre/<genre>",methods=["POST","GET"])
def genre_list(genre):
	cleaned_genre=unquote(genre)
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music WHERE status='active' and genrename=trim(?) COLLATE NOCASE",(cleaned_genre,))
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"duration":calculate(row[3]),
			"genre":row[5]
		}
		songlist.append(mydic)
	if len(result)==0:
		return render_template("404.html")
	else:
		return render_template("genre_playlist.html",songlist=songlist)
#Artist page
@app.route("/artist",methods=["POST","GET"])
def artist():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	data=c.execute("select rowid,* from artist where status='active' order by name")
	return render_template("artist.html",data=data)
# Singe Artist page
@app.route("/artist/<artist>",methods=["POST","GET"])
def playlist(artist):
	cleaned_artist=unquote(artist)
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music WHERE status='active' and artistname=trim(?) COLLATE NOCASE",(cleaned_artist,))
	data=c.fetchall()
	songlist = []
	for row in data:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"duration":calculate(row[3]),
			"genre":row[5]
		}
		songlist.append(mydic)
	if len(data)==0:
		return render_template("404.html")
	else:
		return render_template("artist_playlist.html",songlist=songlist)
	
#Song page
@app.route("/songs",methods=["POST","GET"])
def songs():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	cur=conn.cursor()
	data=c.execute("SELECT rowid,* from music where status='active' ORDER by ROWID DESC")
	state = cur.execute("select rowid,* from music where status='active' ORDER by count + like + downloads DESC LIMIT 8").fetchone()
	return render_template("song.html",data=data, state=state)
#Song list page
@app.route("/songs/<songIds>",methods=["POST","GET"])
def single_song(songIds):
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music WHERE rowid=? and status='active'",(songIds,))
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"url":row[3],
			"description":row[6],
			"duration":calculate(row[3]),
			"genre":row[5]
		}
		songlist.append(mydic)
	if len(result)==0:
		return render_template("404.html")
	else:
		if request.cookies.get('songid'+str(songIds))==None:
			c.execute("UPDATE music set count= count + 1 where ROWID=?;",(songIds,))
			conn.commit()
			rsp = make_response(render_template("single_song.html",songlist=songlist))
			rsp.set_cookie('songid'+str(songIds),songIds)
			# Return response after cookies has been set
			return rsp
		else:
			return render_template("single_song.html",songlist=songlist)

#Song list page
@app.route("/sation",methods=["POST","GET"])
def single_song_action():
	if request.method=='POST':
		value = request.form["value"]
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM music WHERE rowid=? and status='active'",(value,))
		return jsonify(result.fetchall())
	return "You are allowed to be here"
#Artist playlist page
@app.route("/sartist",methods=["POST","GET"])
def single_artist_action():
	if request.method=='POST':
		value = unquote(request.form["value"])
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM music WHERE status='active' and artistname=trim(?) COLLATE NOCASE",(value,))
		return jsonify(result.fetchall())
	return "You are allowed to be here"
#Genre playlist page
@app.route("/sgenre",methods=["POST","GET"])
def single_genre_action():
	if request.method=='POST':
		value = unquote(request.form["value"])
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM music WHERE status='active' and genrename=trim(?) COLLATE NOCASE",(value,))
		return jsonify(result.fetchall())
	return "You are allowed to be here"
#Artist Artist page
@app.route("/searchartist",methods=["POST","GET"])
def artist_search():
	if request.method=='POST':
		value = request.form["value"]
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM artist WHERE artist MATCH(?);",(value,))
		return jsonify(result.fetchall())
	return "You are allowed to be here"
#Song Search page
@app.route("/searchsong",methods=["POST","GET"])
def song_search():
	if request.method=='POST':
		value = request.form["value"]
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		newval = value+'*'
		result=c.execute("SELECT rowid,* FROM music WHERE music MATCH(?);",(newval,))
		return jsonify(result.fetchall())
	return "You are allowed to be here"
#Like Function
@app.route("/like",methods=["POST","GET"])
def like():
	if request.method=='POST':
		songid = request.form["songid"]
		username = request.form["username"]
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		c.execute("UPDATE music set like= like + 1 where ROWID=?;",(songid,))
		c.execute("INSERT INTO user_like(username,songid) VALUES(?,?)",(username,songid,))
		conn.commit()
		return "success",200
	return "You are allowed to be here"
#Unlike Function
@app.route("/unlike",methods=["POST","GET"])
def song_unlike():
	if request.method=='POST':
		songid = request.form["songid"]
		username = request.form["username"]
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		c.execute("UPDATE music set like= like - 1 where ROWID=?;",(songid,))
		c.execute("DELETE FROM user_like where username=? and songid=?",(username,songid,))
		conn.commit()
		return "success",200
	return "You are allowed to be here"
#Dowload Function
@app.route("/downloadcount",methods=["POST","GET"])
def song_download():
	if request.method=='POST':
		songid = request.form["songid"]
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		c.execute("UPDATE music set downloads= downloads + 1 where ROWID=?",(songid,))
		conn.commit()
		return "success",200
	return "You are allowed to be here"
#User like Function
@app.route("/user_like",methods=["POST","GET"])
def user_likes():
	if request.method=='POST':
		username = request.form["username"]
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		data=c.execute("SELECT songid from user_like where username=?",(username,))
		return jsonify(data.fetchall())
	return "You are allowed to be here"
#User like Check Function
@app.route("/user_like_check",methods=["POST","GET"])
def user_likes_check():
	if request.method=='POST':
		username = request.form["username"]
		songid = request.form["songid"]
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		data=c.execute("SELECT count(*) from user_like where username=? AND songid=?",(username,songid,))
		return jsonify(data.fetchall())
	return "You are allowed to be here"
#login page
@app.route("/users/profile",methods=["POST","GET"])
def user_profile():
	if 'user' in session:
		user=session.get('user')['email']
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		data=c.execute("SELECT * FROM music INNER JOIN user_like on music.ROWID=user_like.songid WHERE username=?",(user,))
		return render_template("user_profile.html",data=data)
	else:
		return redirect(url_for('login'))

# Admin page
@app.route("/admin",methods=["POST","GET"])
def admin():
	if 'username' in session:
		return redirect(url_for('dashboard'))
	else:
		if request.method=='POST':
			username = request.form["username"]
			password= request.form["pwd"]
			conn=sqlite3.connect("mscdb.db")
			c=conn.cursor()
			c.execute("SELECT count(*) FROM profile WHERE email=? and password=?",(username,password))
			check=c.fetchone()
			if check[0]==1:
				session['username']=username
				return redirect(url_for('dashboard'))
			else:
				flash('Invalid Login credentail')
				return redirect(url_for('admin'))
		return render_template("login.html")

# login page
@app.route("/logout-admin",methods=["POST","GET"])
def logout_admin():
	session.pop('username',None)


	return redirect(url_for("admin"))
#Admin page
@app.route("/dashboard",methods=["POST","GET"])
def dashboard():
	if 'username' in session:
		conn=sqlite3.connect("mscdb.db")
		cursor=conn.cursor()
		email=session['username']
		data=cursor.execute("SELECT * from profile where email=?",(email,))
		profiles=data.fetchone()
		# Count the data in databse
		cursor2=conn.cursor()
		cursor2.execute("SELECT count(*) from music UNION ALL SELECT count(*) from genre UNION ALL SELECT count(*) from artist")
		counts=cursor2.fetchall()
		return render_template("admin.html",profile=profiles,counts=counts)
	else:
		return redirect(url_for("admin"))


#Profile page
@app.route("/profile",methods=["POST","GET"])
def profile():
	if 'username' in session:
		conn=sqlite3.connect("mscdb.db")
		email=session['username']
		c=conn.cursor()
		result=c.execute("SELECT * FROM profile where email=?",(email,))
		return render_template("profile.html",result=result)
	else:
		return redirect(url_for("admin"))


# Profile Update
@app.route('/profile-update', methods=['GET', 'POST'])
def profile_update():
	email=session['username']
	if request.method=='POST':
		name=request.form["name"]
		email=request.form["mail"]
		password=request.form["pwd"]
		phone=request.form["num"]
		image=request.files["image"]
		# Connect to database
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		if image.filename=='':
			c.execute("UPDATE profile SET fullname=?, email=?, password=?, phone=? where email=?", (name,email,password,phone,email))
			conn.commit()
			return redirect(url_for("profile"))
		else:
	# save image
			image_link=secure_filename(image.filename)
			image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
			c.execute("UPDATE profile SET fullname=?, email=?, password=?, phone=?, pix=? where email=?", (name,email,password,phone,image_link,email))
			conn.commit()
			return redirect(url_for("profile"))
	return redirect(url_for("profile"))
#Song table page
@app.route("/song-table",methods=["POST","GET"])
def songs_table():
	if 'username' in session:
		conn=sqlite3.connect("mscdb.db")
		cursor1=conn.cursor()
		cursor2=conn.cursor()
		email=session['username']
		data=cursor1.execute("SELECT * from profile where email=?",(email,))
		profiles=data.fetchone()
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM music")
		genre=cursor2.execute("SELECT * from genre")
		return render_template("basic-table.html",result=result,profile=profiles,genre=genre)
	else:
		return redirect(url_for("admin"))
#Song table post page
@app.route("/song-post",methods=["POST","GET"])
def songs_post():
	if request.method=='POST':
		artist=request.form["artist"]
		title=request.form["title"]
		link=request.files["song"]
		lyrics=request.form["lyrics"]
		genre=request.form["genre"]
		description=request.form["description"]
		image=request.files["image"]
		status='active'
		count='0'
		downloads='0'
		like='0'
# save song
		song_link=secure_filename(link.filename)
		link.save(os.path.join(uploads_dir_song, secure_filename(link.filename)))
# save image
		image_link=secure_filename(image.filename)
		image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Connect to database
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		c.execute("INSERT INTO music(artistname,title,song,lyric,genrename,description,image,count,downloads,like,status) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(artist,title,song_link,lyrics,genre,description,image_link,count,downloads,like,status,))
# Saving Audio id3s
		audio_path='./static/songs/'+song_link
		picture_path='./static/banner.jpg'
# Save song details
		audio = EasyID3(audio_path)
		audio["title"]=title
		audio["artist"]=artist
		audio["genre"]=genre
		audio["lyricist"]=lyrics
		audio["composer"]=u"Musixcloud"
		audio["copyright"]=u"Musixcloud reserve no right to copyright of songs, please refer to artist for copyright poliy"
		audio["website"]=u"www.musixcloud.com"
		audio.save()
# Add album art
		audio_cover =  MP3(audio_path, ID3=ID3)
		audio_cover.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(picture_path,'rb').read()))
		audio_cover.save()
		# c.execute("UPDATE artist set total=total+1 where name=?",(artist,))
		# c.execute("UPDATE genre set total=total+1 where name=?",(genre,))
		conn.commit()
		return redirect(url_for("songs_table"))
	return"Not allowed"
#Song table update page
@app.route("/song-update/<string>",methods=["POST","GET"])
def songs_update(string):
	if request.method=='POST':
		artist=request.form["artist"]
		title=request.form["title"]
		link=request.files["song"]
		lyrics=request.form["lyrics"]
		genre=request.form["genre"]
		description=request.form["description"]
		image=request.files["image"]
		# Connect to database
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		if link.filename=='' and image.filename !='':
			image_link=secure_filename(image.filename)
			image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Delete Previous Image
			# data=c.execute("SELECT rowid,* FROM music where rowid=?",(string,))
			# for row in data:
			# 	os.remove(os.path.join(uploads_dir_image, secure_filename(row[8])))
			data=c.execute("SELECT rowid,* FROM music where rowid=?",(string,))
			for row in data:
				path = './static/songs/'+row[3]
				picture_path='./static/banner.jpg'
				audio_cover =  MP3(path, ID3=ID3)
				audio_cover.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(picture_path,'rb').read()))
				audio_cover.save()

			c.execute("UPDATE music SET artistname=?, title=?, lyric=?, genrename=?, description=?, image=? WHERE rowid=?", (artist,title,lyrics,genre,description,image_link,string))
			conn.commit()
			return redirect(url_for("songs_table"))

		elif image.filename=='' and link.filename !='':
			song_link=secure_filename(link.filename)
			link.save(os.path.join(uploads_dir_song, secure_filename(link.filename)))
			# data=c.execute("SELECT rowid,* FROM music where rowid=?",(string,))
			# for row in data:
			# 	os.remove(os.path.join(uploads_dir_song, secure_filename(row[3])))
			c.execute("UPDATE music SET artistname=?, title=?, song=?, lyric=?, genrename=?, description=? WHERE rowid=?", (artist,title,song_link,lyrics,genre,description,string))
			conn.commit()
			return redirect(url_for("songs_table"))
		
		elif image.filename=='' and link.filename=='':
			c.execute("UPDATE music SET artistname=?, title=?, lyric=?, genrename=?, description=? WHERE rowid=?", (artist,title,lyrics,genre,description,string))
			conn.commit()
			data=c.execute("SELECT rowid,* FROM music where rowid=?",(string,))
			for row in data:
				path = './static/songs/'+row[3]
# Save song details
				audio = EasyID3(path)
				audio["title"]=title
				audio["artist"]=artist
				audio["genre"]=genre
				audio["lyricist"]=lyrics
				audio["composer"]=u"Musixcloud"
				audio["copyright"]=u"Musixcloud reserve no right to copyright of songs, please refer to artist for copyright poliy"
				audio["website"]=u"www.musixcloud.com"
				audio.save()
			return redirect(url_for("songs_table"))

		else:
	# save song
			song_link=secure_filename(link.filename)
			link.save(os.path.join(uploads_dir_song, secure_filename(link.filename)))
	# save image
			image_link=secure_filename(image.filename)
			image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
			# data=c.execute("SELECT rowid,* FROM music where rowid=?",(string,))
			# for row in data:
			# 	os.remove(os.path.join(uploads_dir_image, secure_filename(row[8])))
			# 	os.remove(os.path.join(uploads_dir_song, secure_filename(row[3])))
			c.execute("UPDATE music SET artistname=?, title=?, lyric=?, genrename=?, description=? WHERE rowid=?", (artist,title,lyrics,genre,description,string))
			conn.commit()
			return redirect(url_for("songs_table"))
	return"Not allowed"
#Song table delete page
@app.route("/song-delete/<string>",methods=["POST","GET"])
def songs_delete(string):
	if request.method=='POST':
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		# data=c.execute("SELECT rowid,* FROM music where rowid=?",(string,))
		# for row in data:
		# 	os.remove(os.path.join(uploads_dir_image, secure_filename(row[8])))
		# 	os.remove(os.path.join(uploads_dir_song, secure_filename(row[3])))
		c.execute("DELETE  FROM music where rowid=?",(string,))
		# c.execute("UPDATE artist set total=total-1 where name=?",(row[1],))
		# c.execute("UPDATE genre set total=total-1 where name=?",(row[5],))
		conn.commit()
		return redirect(url_for("songs_table"))
	return redirect(url_for("songs_table"))
# Artist page
@app.route("/artist-table",methods=["POST","GET"])
def artist_table():
	if 'username' in session:
		conn=sqlite3.connect("mscdb.db")
		cursor=conn.cursor()
		email=session['username']
		data=cursor.execute("SELECT * from profile where email=?",(email,))
		profiles=data.fetchone()
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM artist")
		return render_template("artist-table.html",result=result,profile=profiles)
	else:
		return redirect(url_for("admin"))


# #artist table post page
@app.route("/artist-post",methods=["POST","GET"])
def artists_post():
	if request.method=='POST':
		artist=request.form["artist"]
		image=request.files["image"]
		status="active"
# save image
		image_link=secure_filename(image.filename)
		image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Connect to database
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		c.execute("INSERT INTO artist(name,image,status) VALUES(?,?,?)",(artist,image_link,status))
		conn.commit()
		return redirect(url_for("artist_table"))
	return redirect(url_for("artist_table"))

# #Song table update page
@app.route("/artist-update/<string>",methods=["POST","GET"])
def artists_update(string):
	if request.method=='POST':
		artist=request.form["artist"]
		image=request.files["image"]
		# Connect to database
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		if image.filename=='':
			c.execute("UPDATE artist SET name=? WHERE rowid=?", (artist,string))
			conn.commit()
			return redirect(url_for("artist_table"))
		else:
# save image
			image_link=secure_filename(image.filename)
			image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Delete Previous Image
			data=c.execute("SELECT rowid,* FROM artist where rowid=?",(string,))
		for row in data:
			os.remove(os.path.join(uploads_dir_image, secure_filename(row[3])))
# Update New data
			c.execute("UPDATE artist SET name=?, image=? WHERE rowid=?", (artist,image_link,string))
			conn.commit()
			return redirect(url_for("artist_table"))
	redirect(url_for("artist_table"))

# #Song table delete page
@app.route("/artist-delete/<string>",methods=["POST","GET"])
def artists_delete(string):
	if request.method=='POST':
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		data=c.execute("SELECT rowid,* FROM artist where rowid=?",(string,))
		for row in data:
			os.remove(os.path.join(uploads_dir_image, secure_filename(row[3])))
		c.execute("DELETE  FROM artist where rowid=?",(string,))
		conn.commit()
		return redirect(url_for("artist_table"))
	return redirect(url_for("artist_table"))

#Genre page
@app.route("/genre-table",methods=["POST","GET"])
def genre_table():
	if 'username' in session:
		conn=sqlite3.connect("mscdb.db")
		cursor=conn.cursor()
		email=session['username']
		data=cursor.execute("SELECT * from profile where email=?",(email,))
		profiles=data.fetchone()
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM genre")
		return render_template("genre-table.html",result=result,profile=profiles)
	else:
		return redirect(url_for("admin"))

#Song table post page
@app.route("/genre-post",methods=["POST","GET"])
def genre_post():
	if request.method=='POST':
		genre=request.form["genre"]
		image=request.files["image"]
# save image
		image_link=secure_filename(image.filename)
		image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Connect to database
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		c.execute("INSERT INTO genre (name,image) VALUES(?,?)",(genre,image_link,))
		conn.commit()
		return redirect(url_for("genre_table"))
	return redirect(url_for("genre_table"))
# #Song table update page
@app.route("/genre-update/<string>",methods=["POST","GET"])
def genre_update(string):
	if request.method=='POST':
		genre=request.form["genre"]
		image=request.files["image"]
		# Connect to database
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		if image.filename=='':
			c.execute("UPDATE genre SET genre=? WHERE rowid=?", (genre,string))
			conn.commit()
			return redirect(url_for("genre_table"))
		else:
	# save image
			image_link=secure_filename(image.filename)
			image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Delete Previous Image
			data=c.execute("SELECT rowid,* FROM genre where rowid=?",(string,))
			for row in data:
				os.remove(os.path.join(uploads_dir_image, secure_filename(row[3])))

			c.execute("UPDATE genre SET genre=?, image=? WHERE rowid=?", (genre,image_link,string))
			conn.commit()
			return redirect(url_for("genre_table"))
	redirect(url_for("genre_table"))

# #Song table delete page
@app.route("/genre-delete/<string>",methods=["POST","GET"])
def genre_delete(string):
	if request.method=='POST':
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		data=c.execute("SELECT rowid,* FROM genre where rowid=?",(string,))
		for row in data:
			os.remove(os.path.join(uploads_dir_image, secure_filename(row[3])))
		c.execute("DELETE  FROM genre where rowid=?",(string,))
		conn.commit()
		return redirect(url_for("genre_table"))
	return redirect(url_for("genre_table"))
#Pending Song page
@app.route("/pending/artists",methods=["POST","GET"])
def pending_artists():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	# data=c.execute("SELECT * from music ORDER By ROWID DESC")
	data=c.execute("SELECT rowid,* from artist where status!='active'")
	return render_template("song.html",data=data)
#Pending Song page
@app.route("/pending/songs",methods=["POST","GET"])
def pending_songs():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	# data=c.execute("SELECT * from music ORDER By ROWID DESC")
	data=c.execute("SELECT rowid,* from music where status!='active'")
	return render_template("song.html",data=data)
@app.route("/approve/song")
def approve_Song():
	if request.method=='POST':
		artist=request.form["artist"]
		title=request.form["title"]
		song=request.form["song"]
		decision=request.form["decision"]
		sondId=request.form["decision"]
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		c.execute("update music set status=? where rowid=?",(decision,sondId,))
		conn.commit()
# Saving Audio id3s
		audio_path='./static/songs/'+song
		picture_path='./static/banner.jpg'
# Save song details
		audio = EasyID3(audio_path)
		audio["title"]=title
		audio["artist"]=artist
		audio["genre"]=genre
		audio["composer"]=u"Musixcloud"
		audio["copyright"]=u"Musixcloud reserve no right to copyright of songs, please refer to artist for copyright poliy"
		audio["website"]=u"www.musixcloud.com"
		audio.save()
# Add album art
		audio_cover =  MP3(audio_path, ID3=ID3)
		audio_cover.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(picture_path,'rb').read()))
		audio_cover.save()
		return redirect(url_for("approve_table"))
	return redirect(url_for("approve_table"))
#Validate Song page
@app.route("/validate/artist",methods=["POST","GET"])
def validete_artists():
	if request.method=="POST":
		artistid=request.form['id']
		artistname=request.form['name']
		user=request.form['email']
		conn=sqlite3.connect("mscdb.db")
		c=conn.cursor()
		# data=c.execute("SELECT * from music ORDER By ROWID DESC")
		c.execute("UPDATE artist SET status='ative' WHERE rowid=?",(artistid,))
		c.execute("UPDATE music SET user=? WHERE artistname=?",(user,artistname,))
		conn.commit()
		return redirect(url_for("validateArtist.html"))
	return render_template("validateArtist.html")
# Error handler
@app.errorhandler(404)
def error (e):

	return render_template('error.html')
@app.errorhandler(500)
def internal_server_error(e):
	return "internal server error", 50

# User login
@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

# Google authetication
@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    session['user'] = user
    return redirect('/')

# user logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@ext.register_generator
def index():
    # Not needed if you set SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True
    yield 'index', {}
#Service worker
  #Admin page push messages
@app.route("/push",methods=["POST","GET"])
def admin_push_page():
	if 'username' in session:
		conn=sqlite3.connect("mscdb.db")
		cursor=conn.cursor()
		email=session['username']
		data=cursor.execute("SELECT * from profile where email=?",(email,))
		profiles=data.fetchone()
		return render_template("push.html",profile=profiles)
	else:
		return redirect(url_for("admin"))  

@app.route("/musixcloudpush")
def serveic():
    response = make_response('''
    'use strict';
self.addEventListener('push', function(event) {
    const pushData = event.data.text();
    console.log('[Service Worker] Push Received.');
    console.log(`[Service Worker] Push had this data: "${event.data.text()}"`);
   var data = JSON.parse(pushData);
    const title = data.title;
    const options = {
      body: data.body,
      icon: 'https://app.musixcloud.com/static/logo.png',
      badge: 'https://app.musixcloud.com/static/logo.png',
      sound:'https://app.musixcloud.com/static/juntos-607.mp3',
      image:data.image,
      vibrate: [200, 100, 200, 100, 200, 100, 400],
	  requireInteraction: true
    };
  
    event.waitUntil(self.registration.showNotification(title, options));
	  // Handle click event
  self.addEventListener('notificationclick', function(event) {
    console.log('[Service Worker] Notification click received.');
  
    event.notification.close();
  
    event.waitUntil(
      clients.openWindow(data.url)
    );
  });
  });

    ''')
    response.headers['Content-Type'] = 'text/javascript ; charset=windows-1251'
    return response 
@app.route("/push-api", methods=["POST"])
def create_push_subscription():
    json_data = request.get_json()
    endpoint=json_data["endpoint"]
    pkey=json_data["keys"]["p256dh"]
    auth=json_data["keys"]["auth"]
    conn = sqlite3.connect('mscdb.db')
    c = conn.cursor()
    c.execute('INSERT into pushsub(endpoint,pkey,auth) values (?,?,?)',(endpoint,pkey,auth))
    conn.commit()
    return "success"

# Delete subscription
@app.route("/delete-push-api", methods=["POST"])
def delete_push_subscription():
    json_data = request.get_json()
    endpoint=json_data["endpoint"]
    conn = sqlite3.connect('mscdb.db')
    c = conn.cursor()
    c.execute('DELETE FROM pushsub where endpoint=?',(endpoint,))
    conn.commit()
    return "success"
@app.route("/admin-api/send-push-notifications", methods=["POST","GET"])
def send_push_notifications():
    title = request.form["title"]
    body = request.form["body"]
    url=request.form["url"]
    image=request.form["img"]
    conn = sqlite3.connect('mscdb.db')
    c = conn.cursor()
    c.execute('SELECT * FROM pushsub')
    result = c.fetchall()
    serverError = "Success"
    for row in result:
        try:
            webpush(
                subscription_info={
                "endpoint": row[0],
                "keys": {
                "p256dh": row[1],
                "auth": row[2]
                }},
                data=json.dumps({"title": title, "body": body,"url": url ,"image":image}),
                vapid_private_key="yXcbyUJ_Yzlx2RxW0vwsjUqUS1sJeE8npqdMdrH82l8",
                vapid_claims={
                "sub": "mailto:samuel@musixcloud.com",
                }
                )
        except WebPushException as ex:
            if ex.response and ex.response.json():
                extra = ex.response.json()
                serverError = "I'm sorry, Dave, but I can't do that: {}", repr(ex)
    return jsonify(serverError)	
# Musixcloud App apis
# Songs
@app.route('/v1/api/songs')
def songs_api():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music")
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"image":"https://app.musixcloud.com/static/album-art/"+row[8],
			"url": "https://app.musixcloud.com/static/songs/"+row[3],
			"description":row[6],
			"duration":calculate(row[3]),
			"genre":row[5]
		}
		songlist.append(mydic)
	return jsonify(songlist)
# Genre 
@app.route('/v1/api/genre')
def genrelist_api():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM genre")
	result=c.fetchall()
	artist = []
	for row in result:
		mydic={
			"id":row[0],
			"genre":row[1],
			"link":"https://app.musixcloud.com/v1/api/genre/"+row[1],
			"image":"https://app.musixcloud.com/static/album-art/"+row[3]
		}
		artist.append(mydic)
	return jsonify(artist)
# Genre Songs
@app.route('/v1/api/genre/<genre>')
def genresong_api(genre):
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music where genrename=?",(genre,))
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"image":"https://app.musixcloud.com/static/album-art/"+row[8],
			"url": "https://app.musixcloud.com/static/songs/"+row[3],
			"description":row[6],
			"duration":calculate(row[3]),
			"genre":row[5],
			"lyric":row[9]
		}
		songlist.append(mydic)
	return jsonify(songlist)
# Genre Songs
@app.route('/v1/api/artist/<name>')
def artistsong_api(name):
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music where artistname=trim(?)",(name,))
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"image":"https://app.musixcloud.com/static/album-art/"+row[8],
			"url": "https://app.musixcloud.com/static/songs/"+row[3],
			"description":row[6],
			"duration":calculate(row[3]),
			"genre":row[5]
		}
		songlist.append(mydic)
	return jsonify(songlist)
# Artist Songs
@app.route('/v1/api/artist')
def artistlist_api():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM artist")
	result=c.fetchall()
	artist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"image":"https://app.musixcloud.com/static/album-art/"+row[3]
		}
		artist.append(mydic)
	return jsonify(artist)
# Trending Songs
@app.route('/v1/api/songs/trending')
def songstrend_api():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	c.execute("select rowid,* from music ORDER by count + like + downloads DESC LIMIT 10")
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"image":"https://app.musixcloud.com/static/album-art/"+row[8],
			"url": "https://app.musixcloud.com/static/songs/"+row[3],
			"description":row[6],
			"duration":calculate(row[3]),
			"genre":row[5],
			"lyric":row[9]
		}
		songlist.append(mydic)
	return jsonify(songlist)
# New Songs
@app.route('/v1/api/songs/new')
def songsnew_api():
	conn=sqlite3.connect("mscdb.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* from music ORDER by ROWID DESC LIMIT 10")
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"image":"https://app.musixcloud.com/static/album-art/"+row[8],
			"url": "https://app.musixcloud.com/static/songs/"+row[3],
			"description":row[6],
			"duration":calculate(row[3]),
			"genre":row[5]
		}
		songlist.append(mydic)
	return jsonify(songlist)
if __name__ == "__main__":
	app.run(debug=true)
