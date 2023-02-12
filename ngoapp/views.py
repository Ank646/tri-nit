from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import io
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib import messages

from .models import ngo, userpro, ngoorder

from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

import requests as re
from bs4 import BeautifulSoup as bs

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import razorpay
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
client = razorpay.Client(
    auth=("rzp_test_8WLT7C9ecj0ZDS", "5rq58y9SC6XQiCiHehc3nMrT"))


def payment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 50000

        client = razorpay.Client(
            auth=("TEST_KEY", "SECRET_KEY"))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})

    return render(request, 'index.html')


def donate(request):

    if request.method == "POST":
        name = request.POST.get('options')
        amount = 50000

        client = razorpay.Client(
            auth=("TEST_KEY", "SECRET_KEY"))
        payment = client.order.create(
            {'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        return redirect("/donate")
    return render(request, "donate.html")


@csrf_exempt
def success(request):
    return render(request, "index.html")


def loginadmin(request):
    if request.method == 'POST':
        ngoregid = request.POST['regid']
        passs = request.POST['password']
        user = auth.authenticate(username=ngoregid, password=passs)
        if user is not None:
            auth.login(request, user)
            return redirect('adminpanel')
        else:
            messages.info(request, "Invalid details")
            return redirect('loginadmin')

    return render(request, "loginadmin.html")


@login_required(login_url='/loginadmin')
def adminpanel(request):
    re = request.user.username
    re = re[0:2]+"-"+re[2: 6]+"-"+re[6:]
    fg = ngo.objects.filter(ngoregid=re).first()
    if request.method == 'POST':
        categ = request.POST['cat']
        exp = request.POST['exp']
        amo = request.POST['amo']

        de = ngoorder.objects.create(
            ngoreg=re, ngocat=categ, ngoexp=exp, ngoamount=amo)
        de.save()
        messages.info(request, "Request sent successfully")
        return redirect('/adminpanel')
    return render(request, "admin.html", {"ngodata": fg})


@login_required(login_url='/loginadmin')
def logout(request):
    auth.logout(request)
    return redirect(loginadmin)


def index(request):
    return render(request, 'index.html')


def admin(request):
    return render(request, "admin.html")


def signupngo(request):
    id = ""
    name = "bkj"
    city = ""
    dict = {}
    button = 0

    if request.method == 'POST':
        regis = request.POST['reg']
        name = request.POST['name']
        city = request.POST['city']
        state = request.POST['state']

        state = state.lower()
        state = state.replace(" ", "-")
        city = city.lower()
        city = city.replace(" ", "-")
        ree = re.get(f"https://www.indiangoslist.com/{state}/ngos-in-{city}")
        f = bs(ree.content, "html.parser")

        g = f.find_all('div', class_="right_head")
        import numpy
        gh = numpy.array(g)
        k = int(len(gh)/5)
        import pandas as pd
        gh = gh.reshape(k, 5)
        fgg = pd.DataFrame(
            gh, columns=['name', 'reg', 'type', 'city', 'state'])
        li = []
        fg = []
        ok = []
        for i in gh:
            fg.append(ok)
            ok = []
            li = []
            for j in range(0, 5):
                li.append(i[j].text)
            ok = numpy.array(li)
        jk = numpy.array(fg)
        c = 0
        d = 1
        file = pd.DataFrame(
            fg, columns=['name', 'reg', 'type', 'state', 'city'])
        for kh in range(1, len(fg)):

            for k in range(0, 5):

                if regis in fg[kh][k]:
                    d = kh
                    break
        id = fg[d][1]
        url = fg[d][0]
        hj = url.split()
        ff = len(url)
        urll = ""
        for t in hj:
            urll += t+"-"
        print(urll)
        urll = urll[:ff]
        urll = urll.lower()
        id = fg[d][1]
        city = fg[d][4]
        city = city.lower()
        city = city.strip()

        id = id.replace("/", "-")
        print(
            f"https://www.indiangoslist.com/ngo-address/{urll}-in-{city}-{state}_{id}")

        rese = re.get(
            f"https://www.indiangoslist.com/ngo-address/{urll}-in-{city}-{state}_{id}")
        f = bs(rese.content, "html.parser")

        gk = f.find_all('div', class_="ngo_right_head")

        gh = numpy.array(gk)
        arr = []
        for i in gh:
            arr.append(i.text)
        ngoname = arr[0]
        uniqueid = arr[1]
        chief = arr[2]
        chairman = arr[3]
        secretary = arr[4]
        registeredat = arr[6]
        type = arr[7]
        registrationno = arr[8]
        cityofreg = arr[9]
        stateofreg = arr[10]
        dateofreg = arr[11]
        telephoneno = arr[16]
        mobileno = arr[17]
        address = arr[18]
        dict = {
            "ngoname": arr[0],
            "uniqueid": arr[1],
            "chief": arr[2],
            "chairman": arr[3],
            " secretary": arr[4],
            "registeredat": arr[6],
            "type": arr[7],
            "registrationn": arr[8],
            "cityofreg": arr[9],
            "stateofreg": arr[10],
            "dateofreg": arr[11],
            "telephoneno": arr[16],
            "mobileno": arr[17],
            "address": arr[18],
        }
        uniqid = uniqueid.replace("/", "")
        button = 1
        print(dict)
        messages.info(request, "NGO name :" + arr[0])
        messages.info(request, "NGO uniqueId :" + arr[1])
        messages.info(request, "chairman :" + arr[3])
        messages.info(request, "NGO Registration No. :" + arr[8])
        messages.info(request, "Date of registration :" + arr[11])
        messages.info(request, "Mobile No. :" + arr[17])
        messages.info(request, "Secretary :" + arr[4])
        messages.info(request, "Type : " + arr[7])
        passs = request.POST['password']
        pass2 = request.POST['password2']
        if passs == pass2:
            if User.objects.filter(username=uniqid).exists():
                messages.info(
                    request, 'Already registered NGO !!!!')
                return redirect('signupngo')
            else:
                user = User.objects.create_user(
                    username=uniqid, password=passs)
                user.save()
                us = auth.authenticate(username=uniqid, password=passs)
                auth.login(request, us)

                return redirect(uniqid+'/details')
        else:
            messages.info(request, 'Enter same password in both')
            return redirect('signupngo')

    return render(request, 'signup.html', {"ngodata": dict, 'name': name, "button": button})


@login_required(login_url='/loginadmin')
def details(request, ngoo):
    userngo = request.user.username
    if request.method == 'POST':
        prevworks = request.POST['prev-works']
        endgoals = request.POST['endgoal']
        plan = request.POST['plan']
        vision = request.POST['vision']
        fund = request.POST['fund']
        field = request.POST['field']
        about = request.POST['about']
        fb = request.POST['social-facebook']
        insta = request.POST['social-instagram']
        twitter = request.POST['social-twitter']
        website = request.POST['social-website']

        use = ngo.objects.filter(ngoname=ngoo).first()
        profile = use.objects.create(ngowork=prevworks, ngoplan=plan, ngovision=vision, ngofundneeds=fund,
                                     ngofb=fb, ngoinsta=insta, ngoweb=website, ngotwitter=twitter)
        profile.save()

        return redirect('/adminpanel')

    return render(request, 'additionaldetails.html', {'username': userngo})


@login_required(login_url='/loginuser')
def listt(request):
    g = ngo.objects.all()

    return render(request, "event.html", {'ngo': g})


def signupuser(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        passs = request.POST['password']
        pass2 = request.POST['password2']
        kindofngo = request.POST['donatef']
        print(kindofngo)
        if passs == pass2:
            if User.objects.filter(email=email).exists():
                messages.info(
                    request, 'Account already created . Please login !!!!')
                return redirect('signupuser')
            elif User.objects.filter(username=username).exists():
                messages.info(
                    request, 'Username already taken . Please try another !!!!')
                return redirect('signupuser')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=passs)
                user.save()
                us = auth.authenticate(username=username, password=passs)
                auth.login(request, us)
                userr = User.objects.get(username=username)
                profile = userpro.objects.create(
                    userid=username, firstname=firstname, lastname=lastname, password=passs)
                profile.save()
                return redirect('/')
        else:
            messages.info(request, 'Enter same password in both')
            return redirect('signupuser')

    return render(request, 'signupuser.html')


def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        passs = request.POST['password']
        user = auth.authenticate(username=username, password=passs)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid details")
            return redirect('loginuser')
    return render(request, "loginuser.html")


def crowdfunding(request):
    return render(request, "donate.html")


def ngos(request, namee):
    ghj = namee

    hg = ngoorder.objects.filter(ngoreg=namee)
    pr = ngo.objects.filter(ngoregid=namee).first()
    df = {
        "regid": pr.ngoregid,
        "name": pr.ngonm,
        "field": pr.ngofield,
        "address": pr.ngoaddress,
        "needs": pr.ngofundneeds,
        "city": pr.ngocity,
        "state": pr.ngostate,
        "about": pr.ngoabout,
        "goal": pr.ngogoal,
        "vision": pr.ngovision,
        "type": pr.ngotype,
        "plan": pr.ngoplan,
        "work": pr.ngowork,
        "fb": pr.ngofb,
        "insta": pr.ngoinsta,
        "linked": pr.ngolinked,
        "twitt": pr.ngotwitter,
        "regid": ghj







    }

    return render(request, 'single.html', {'data': df, 'fat': hg})


def passgen(request, id):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # filter it among ngo
    use = ngo.objects.filter(ngoregid=id).first()
    lines = []
    # Will Add All Progress Accordingly
    lines.append("ID:    "+use.ngoregid)
    lines.append("TYPE:    "+use.ngotype)
    lines.append("=============================")
    lines.append("=============================")
    lines.append("CITY:   "+use.ngocity)
    lines.append("STATE:    "+use.ngostate)
    lines.append("=============================")
    lines.append("=============================")
    lines.append("GOAL:     "+use.ngogoal)
    lines.append("WORK:     "+use.ngowork)
    lines.append("VISION:   "+use.ngovision)
    lines.append("=============================")
    lines.append("=============================")
    lines.append("PLAN:   "+use.ngoplan)
    lines.append("END GOAL:   "+use.ngoendgoal)
    lines.append("ABOUT:   "+use.ngoabout)

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="ngo"+id+".pdf")
