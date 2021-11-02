# APIキー：AIzaSyB6l8_ovgjjfsSIvw9oyFs5FzlT71Hutk8
# export FLASK_APP=application.py

import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import pprint
import googlemaps
from datetime import datetime
import urllib.parse
from collections import defaultdict
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import urllib.request, json
from collections import defaultdict
import requests
import sys
sys.dont_write_bytecode = True

from helpers import apology, login_required

app = Flask(__name__)


# Configure application# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

key = 'AIzaSyB6l8_ovgjjfsSIvw9oyFs5FzlT71Hutk8'

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///tabiji.db")

@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    display_photo = []
    photos = []

    if request.method == "POST":
        user_id = session["user_id"]
        if not request.form.get("newsite"):
            return apology("must provide a place")

        trip_title = request.form.get("newsite")
        try:
            db.execute("INSERT INTO trips (trip_title, user_id) VALUES (?, ?)", trip_title, user_id)
        except:

            return apology("Already taken")
        try:
            trips_ids = db.execute("SELECT trips_id FROM trips WHERE user_id = ? AND trip_title = ?", user_id, trip_title)
            trips_id_dict = trips_ids[0]
            trips_id = trips_id_dict["trips_id"]

            key = 'AIzaSyB6l8_ovgjjfsSIvw9oyFs5FzlT71Hutk8' # 上記で作成したAPIキーを入れる
            client = googlemaps.Client(key)

            #位置情報取得AIzaSyBHmiWAqFiEytkNFn6jxHAqhxcIx_pO8sc
            geocode_result = client.geocode(trip_title)
            loc = geocode_result[0]['geometry']['location']
            print(loc)

            #観光地のみ
            place_results = client.places_nearby(location=loc, radius=1000000,type='tourist_attraction',language='ja') #半径1000000m以内の情報を取得

            # url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?type=tourist_attraction&location={}&radius=1000000&key={}'.format(loc, key)
            # res = requests.get(url)
            # place_results = json.loads(res.text)

            result = []

            for place_result in place_results['results']:
                result.append(place_result)
                # 配列にphotosが存在しないとき
                if not 'photos' in place_result.keys():
                    print("no image")
                else:
                    #評価が高い　名前　電話番号など
                    rating = place_result['rating']
                    if rating > 3.5:
                        name = place_result['name']
                        #同じ名前がない場合?
                        if name not in display_photo:
                            display_photo.append(place_result['name'])
                            place_results = client.places_nearby(location=loc, radius=1000000,name=name,type='tourist_attraction',language='ja') #半径1000000m以内の情報を取得
                            # ここで取得リスト出力
                            # pprint.pprint(display_photo)
                            p_value = place_result['photos'][0]['photo_reference']
                            photo = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={p_value}&key={key}"
                            photos.append(photo)


            # display_photoとphotoを辞書化しました。
            # print("###########################")
            # print(display_photo)
            display_photo=dict(zip(display_photo, photos))
            # print("###########################")
            # print(type(display_photo))
            # pprint.pprint(display_photo)
            # print("###########################")
            return render_template('swipe.html', trips_id=trips_id, trip_title=trip_title, photos=photos, display_photo=display_photo)
        except:
            return apology("APIから情報を取得できません")
    else:
        user_id = session["user_id"]
        trips = db.execute("SELECT start_time, trip_title, trips_id FROM trips WHERE user_id = ?", user_id)


        #ユーザーがまだお気に入りを追加していない場合
        if not trips:
            return render_template("index.html")
        else:
            photos = []
            for trip in trips:
                trips_id = trip['trips_id']

                key = 'AIzaSyB6l8_ovgjjfsSIvw9oyFs5FzlT71Hutk8'

                favorite_sites = db.execute("SELECT site_name FROM favorite_sites WHERE trips_id =?", trips_id)

                if not favorite_sites:
                    photos.append("static/nophoto.png")

                else:
                    favorite_site = favorite_sites[0]
                    print('favorite_site')
                    print(favorite_site)
                    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={favorite_site['site_name']}&key={key}"

                    req_url = requests.get(url)
                    # すべての情報をjsonで取得
                    req_url_json = req_url.json()

                    info_fav_sites = req_url_json['results']
                    print(info_fav_sites)
                    print('&&&&')
                    info_fav_sites = info_fav_sites[0]



                    #写真取得
                    p_value = info_fav_sites['photos'][0]['photo_reference']
                    photo = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={p_value}&key={key}"
                    photos.append(photo)

        return render_template("index.html", data = zip(photos,trips))

@app.route("/trips_delete", methods=["POST"])
@login_required
def trips_delete():
    user_id = session["user_id"]
    trips_id = request.form.get("trips_id")
    if trips_id:
        trips = db.execute("DELETE FROM trips WHERE trips_id = ?", trips_id)
        flash("successful")
    return redirect('/')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation")

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("password must match")

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        users = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if not users:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, password)
            return redirect("/")
        else:
            return apology("username already taken")
    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/info", methods=["GET", "POST"])
@login_required
def info():
    if request.method == "POST":
        user_id = session["user_id"]
        trips_id = request.form.get("trips_id")
        favorite_site = request.form.get("new_string_list")
        # 'をとる
        new_string = ' '.join(filter(str.isalnum, favorite_site))
        photos = []

        key = 'AIzaSyB6l8_ovgjjfsSIvw9oyFs5FzlT71Hutk8' # 上記で作成したAPIキーを入れる

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}".format(favorite_site,key)
        req_url = requests.get(url)
        # すべての情報をjsonで取得
        req_url_json = req_url.json()

        info_fav_sites = req_url_json['results'][0]
        place_id = info_fav_sites['place_id']


        #detailを取得
        detail_url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&key={}&lang=ja".format(place_id,key)
        req_detail_url = requests.get(detail_url)
        # すべての情報をjsonで取得
        req_detail_url_json = req_detail_url.json()
        place_details = req_detail_url_json['result']
        try:
            # 住所
            address = place_details['formatted_address']
        except KeyError:
            address = ' '
        try:
            # 電話番号
            phone_number = place_details['formatted_phone_number']
        except KeyError:
            phone_number = ' '
        try:
            # 評価
            rating = place_details['rating']
        except KeyError:
            rating = ' '
        try:
            #ウェブサイトのurl
            website = place_details['website']
        except KeyError:
            website = ' '

        global weekday_text
        global open_now
        global opening_hours
        try:
            opening_hours = place_details['opening_hours']
            #営業時間、曜日
            try:
                #営業時間、曜日
                weekday_text = opening_hours['weekday_text']
            except KeyError:
                weekday_text = ' '
            #今あいているか
            try:
                open_now = opening_hours['open_now']
                if open_now == True:
                    open_now = "あいている！！！！"
                else:
                    open_now = "しまってる…"
            except KeyError:
                opening_hours = ' '
                open_now = ' '
        except KeyError:
            opening_hours = ' '
            open_now = ' '
            weekday_text = ' '

        #写真取得
        p_value = info_fav_sites['photos'][0]['photo_reference']
        photo = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={p_value}&key={key}"
        photos.append(photo)
        # photsだと同じ観光地の写真がたくさんでる

        return render_template('info.html', favorite_site=new_string, weekday_text=weekday_text,open_now=open_now, phone_number=phone_number, address=address, photo=photo, rating=rating, website=website)
    else:
        return redirect('/')



@app.route("/route", methods=["GET", "POST"])
@login_required
def route():
    if request.method == "POST":
        user_id = session['user_id']
        trip_title = request.form.get("trip_title")
        trips_id = request.form.get("trips_id")
        print('trips_id')
        print(trips_id)
        #お気に入り、出発地、到着地を取り出して、ルート再掲
        origin = db.execute("SELECT start_place FROM trips WHERE trips_id =?", trips_id)
        destination = db.execute("SELECT goal_place FROM trips WHERE trips_id =?", trips_id)
        trip_title = db.execute("SELECT trip_title FROM trips WHERE trips_id =?", trips_id)
        favorite_sites = db.execute("SELECT site_name FROM favorite_sites WHERE trips_id =?", trips_id)

        means = db.execute("SELECT means FROM trips WHERE trips_id =?", trips_id)
        print('means')
        print(means[0]['means'])
        means = means[0]['means']
        favorite_sites_list = []
        for favorite_site in favorite_sites:
            site_name = favorite_site["site_name"]
            new_string = ' '.join(filter(str.isalnum, site_name))
            favorite_sites_list.append(new_string)
        return render_template('route.html',origin=origin, destination=destination, mode=means.upper(), favorite_sites_list=json.dumps(favorite_sites_list))

    else:
        return redirect('/')


@app.route("/spots", methods=["GET", "POST"])
@login_required
def spots():
    if request.method == "POST":
        trip_title = request.form.get("trip_title")

        user_id = session["user_id"]
        trips_id = request.form.get("trips_id")

        favorite_sites = db.execute("SELECT site_name FROM favorite_sites WHERE trips_id =?", trips_id)

        if not favorite_sites:
            return apology('no favorite sites registered')

        else:
            photos = []
            new_string_lists = []
            #'をとばしたfavorite_siteが入る
            new_string_list = []
            key = 'AIzaSyB6l8_ovgjjfsSIvw9oyFs5FzlT71Hutk8' # 上記で作成したAPIキーを入れる
            for favorite_site in favorite_sites:
                site_name = favorite_site['site_name']
                # new_string_listsは特殊文字つき
                new_string_lists.append(site_name)

                url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}".format(favorite_site['site_name'],key)
                req_url = requests.get(url)
                # すべての情報をjsonで取得
                req_url_json = req_url.json()


                info_fav_sites = req_url_json['results']
                info_fav_sites = info_fav_sites[0]
                place_id = info_fav_sites['place_id']

                #写真取得
                p_value = info_fav_sites['photos'][0]['photo_reference']
                photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_value, key)
                photos.append(photo)
            print("new_string_list")
            print(new_string_list)
            #特殊文字を飛ばしたリスト作成
            for new_string_temp in new_string_lists:
                new_string = ''.join(filter(str.isalnum, new_string_temp))
                new_string_list.append(new_string)

            return render_template('spots.html', trip_title=trip_title, trips_id=trips_id, place_id=place_id, data=zip(new_string_list,photos))

@app.route("/startandgoal", methods=["GET", "POST"])
@login_required
def startandgoal():
    if request.method == "POST":
        user_id = session['user_id']
        trips_id = request.form.get("trips_id")
        origin = request.form.get("start_place")
        start_time = request.form.get("start_time")
        destination = request.form.get("goal_place")
        mode = request.form.get("mode")

        #route_urlにmodeをいれました
        db.execute("UPDATE trips SET start_place = ?, start_time = ?, goal_place = ?, means = ? WHERE trips_id = ?", origin, start_time, destination,  mode, trips_id)

        api_key = 'AIzaSyB6l8_ovgjjfsSIvw9oyFs5FzlT71Hutk8'
        endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

        favorite_sites = db.execute("SELECT site_name FROM favorite_sites WHERE trips_id =?", trips_id)

        favorite_lis = defaultdict(list)
        for i in favorite_sites:
            favorite_lis['hoge'].append(i['site_name'])
            print(favorite_lis)

        lis = []
        for d in favorite_lis['hoge']:
            d = d.replace("'", "")
            lis.append(d)


        #python用
        favorite_sites_list = []

        #json用
        waypoints = []

        for favorite_site in favorite_sites:
            site_name = favorite_site["site_name"]

            new_string = ' '.join(filter(str.isalnum, site_name))
            print(new_string)
            # print(site_name)
            print("##############################")
            favorite_sites_list.append(new_string)

            #waypoints用
            site_name_new = '{location: ' + site_name + '}'
            waypoints.append(site_name_new)

        print("waypointsを出力")
        print(waypoints)

        print("favorite_site_listを出力")
        print(favorite_sites_list)

        # place_idを取得できましたンゴ
        place_id = []
        i = []
        for favotite_list in favorite_sites_list:

            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={favotite_list}&key={api_key}"

            req_url = requests.get(url)
            # すべての情報をjsonで取得
            req_url_json = req_url.json()

            i=req_url_json['results'][0]['place_id']
            print(type(i))
            print(i)
            print("####################")
            place_id.append(i)

        # try:
        #     dep_time = str(start_time)
        #     dt = datetime.strptime(dep_time, '%H:%M')
        #     unix_time = int(dt.timestamp())
        # except:
        #     return apology('provide time')


        favorite_sites_list = []
        for favorite_site in favorite_sites:
            site_name = favorite_site["site_name"]
            new_string = ' '.join(filter(str.isalnum, site_name))
            favorite_sites_list.append(new_string)

        print("favorite_sites_list:")
        print(favorite_sites_list)

        return render_template('route.html', origin=origin, destination=destination, mode=mode.upper(), start_time=start_time, favorite_sites_list=json.dumps(favorite_sites_list),route = route)

    else:
        return redirect('/')

@app.route("/swipe", methods=["GET", "POST"])
@login_required
def swipe():
    if request.method == "POST":
        trips_id = request.form.get("trips_id")
        favs = request.form.get("like")
        #favsをどうやって配列にするか
        print("favs")
        print(list(favs.split(',')))
        favs = list(favs.split(','))
        for fav in favs:
            db.execute("INSERT INTO favorite_sites (trips_id, site_name) VALUES (?, ?)", trips_id, fav)
        return render_template('startandgoal.html', trips_id=trips_id)
    else:
        return redirect('/')


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)