from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib import messages

from .models import ngo, userpro

from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

import requests as re
from bs4 import BeautifulSoup as bs


def index(request):
    return render(request, 'index.html')


def valid(request):
    if request.method == 'POST':
        regis = request.POST['reg']
        name = request.POST['name']
        city = request.POST['city']
        state = request.POST['state']

        state = state.lower()
        state = state.replace(" ", "-")
        ree = re.get(f"https://www.indiangoslist.com/{state}/ngos-in-{city}")
        f = bs(ree.content, "html.parser")
        print(f)
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
                print(fg[kh][k])
                print()
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

        print(id)
        id = id.replace("/", "-")
        print(
            f"https://www.indiangoslist.com/ngo-address/{urll}-in-{city}-{state}_{id}")

        rese = re.get(
            f"https://www.indiangoslist.com/ngo-address/{urll}-in-{city}-{state}_{id}")
        f = bs(rese.content, "html.parser")
        print(f)
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
            "  dateofreg": arr[11],
            " telephoneno": arr[16],
            " mobileno": arr[17],
            " address": arr[18],
        }
        print(dict)

        return redirect("/")
    return render(request, index.html, {"id": id, "city": city})


def details(request, ngoo):
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
        return redirect(ngoo+'/details')

    return render(request, 'additionaldetails.html')


def listt(request):
    g = ngo.objects.all()
    gf = []
    if request.method == 'POST':
        state = request.POST['name']
        gf = ngo.objects.filter(ngostate=state).all()
        return redirect('/listngo')

    return render(request, "event.html", {'ngo': g, 'ngostate': gf})


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
    pass


from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

def passgen(request):
        buf=io.BytesIO()
        c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
        textob=c.beginText()
        textob.setTextOrigin(inch,inch)
        textob.setFont("Helvetica",14)


        # filter it among ngo
        use = ngo.objects.all()
        lines=[]
        # Will Add All Progress Accordingly
        for us in use:
            lines.append(str(us.ngoname))
            lines.append(str(us.ngocity))
        
        for line in lines:
            textob.textLine(line)
        
        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf,as_attachment=True,filename='ngo.pdf')



