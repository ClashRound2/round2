from django.shortcuts import render
from basic_app.models import Questions, UserProfileInfo, submissions
from basic_app.models import User
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate

import datetime
import os

endtime = 0
_flag = False

starttime = ""

path = 'data/users_code'
path2 = 'data/standard'
path3 = 'data/standard/testcaseScore'


def start_Timer(request):
    if request.method == 'GET':
        return render(request, 'basic_app/timer.html')
    else:
        adminpassword = '1'
        _password = request.POST.get('pass1')
        if _password == adminpassword:
            global _flag
            _flag = True
            now1 = datetime.datetime.now()
            min1 = now1.minute + 1
            hour1 = now1.hour
            time1 = str(hour1) + ':' + str(min1)

            time = now1.second+now1.minute*60+now1.hour*60*60
            global endtime
            global starttime
            starttime = time1
            endtime = time + 7200

            return HttpResponse("Timer set go")
        else:
            return HttpResponse("Invalid login details supplied.")


def waiting(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('question_panel'))
    else:
        now = datetime.datetime.now()
        min = now.minute
        hour = now.hour
        sec = min * 60 + hour * 60 * 60
        time = str(hour)+":" + str(min)

        global starttime

        if not starttime == "":
            _time_string = starttime.split(":")
            _min = int(_time_string[1])
            _hour = int(_time_string[0])
            _sec = _hour * 60 * 60 + _min * 60
            if sec > _sec:
                return HttpResponseRedirect(reverse('register'))

        if time == starttime:
            return HttpResponseRedirect(reverse('register'))
        else:
            return render(request, 'basic_app/waiting.html')


def timer():
    now = datetime.datetime.now()
    time = now.second + now.minute * 60 + now.hour * 60 * 60
    global endtime
    return endtime-time


def questions(request, id=1):
    if request.user.is_authenticated:
        if request.method == 'GET':
            a = Questions.objects.all()
            user = UserProfileInfo.objects.get(user=request.user)
            user.question_id = int(id)
            Q = a[user.question_id-1]
            q = Q.questions

            username = request.user.username

            if not os.path.exists('{}/{}/'.format(path, username)):
                user.attempts = 0  # this line should be exceuted only once
                os.system('mkdir {}/{}'.format(path, username))

                for i in range(1, 7):
                    os.system('mkdir {}/{}/question{}'.format(path, username, i))

            user.save()

            dict = {'q': q, 't': timer(), 's': user.totalScore}

            return render(request, 'basic_app/Codingg.html', context=dict)

        else:

            some_text = request.POST.get('editor')
            subb = submissions(user=request.user)
            subb.sub = some_text
            time = timer()
            hour = time // (60 * 60)
            a = time % (60 * 60)
            if a < 60:
                sec = a
                min = 0
            else:
                min = a // 60
                sec = a % 60
            subb.subtime = '{}:{}:{}'.format(hour, min, sec)

            option = request.POST.get('lang')
            username = request.user.username
            user = UserProfileInfo.objects.get(user=request.user)
            juniorSenior = user.level
            user.option=option
            subb.qid = user.question_id
            subb.save()

            testlist = ['fail', 'fail', 'fail', 'fail', 'fail']

            myfile = open('{}/{}/{}.txt'.format(path3, str(user.question_id), str(user.question_id)))
            content = myfile.readlines()

            junior = [int(i.strip()) for i in content[0:5]]
            senior = [int(i.strip()) for i in content[5:10]]

            user.attempts += 1

            fo = open('{}/{}/question{}/{}{}.{}'.format(path, username, user.question_id, username, user.attempts, option), 'w')
            fo.write(some_text) # writes .c file
            fo.close()

            if os.path.exists('{}/{}/question{}/{}{}.{}'.format(path, username, user.question_id, username, user.attempts, option)):
                ans = os.popen("python data/main.py " + "{}/{}/question{}/{}{}.{}".format(path, username, user.question_id, username, user.attempts, option) + " " + username + " " + str(user.question_id) + " " + juniorSenior + " " + str(user.attempts)).read()
                ans = int(ans)  # saves like 9999899950
                print("THE SANDBOX CODE IS", ans)
                data = [1, 2, 3, 4, 5]
                tcOut = [0, 1, 2, 3, 4]
                switch = {

                    10: 0,
                    99: 1,
                    50: 2,
                    89: 3,
                    70: 4,
                    20: 5,
                    60: 6
                }

                user.score = 0
                for i in range(0, 5):
                    data[i] = ans % 100	# stores output for each case but in reverse order
                    ans = int(ans / 100)

                    tcOut[i] = switch.get(data[i], 2)
                    if tcOut[i] == 0:  # if data[i] is 10 i.e correct answer
                        testlist[4 - i] = 'pass'
                        if juniorSenior == 'junior':
                            user.score = user.score + junior[i]
                        else:
                            user.score = user.score + senior[i]

                cerror = " "

                if tcOut[4] == 3:
                    error = path + "/" + username + "/" + str("error{}.txt".format(user.question_id))

                    with open(error, 'r') as e:
                        cerror = e.read()
                        cerror1 = cerror.split('/')
                        cerror2 = cerror1[0]+'/'+cerror1[1]+'/'+cerror1[2]+'/'
                        cerror = cerror.replace(cerror2, '')

                if tcOut[0] == 2 or tcOut[1] == 2 or tcOut[2] == 2 or tcOut[3] == 2 or tcOut[4] == 2:
                    cerror = "Time limit exceeded"

                if tcOut[0] == 4 or tcOut[1] == 4 or tcOut[2] == 4 or tcOut[3] == 4 or tcOut[4] == 4:
                    cerror = "Abnormal Termination"

                if tcOut[0] == 5 or tcOut[1] == 5 or tcOut[2] == 5 or tcOut[3] == 5 or tcOut[4] == 5:
                    cerror = "Abnormal Termination"

                if tcOut[0] == 6 or tcOut[1] == 6 or tcOut[2] == 6 or tcOut[3] == 6 or tcOut[4] == 6:
                    cerror = "Run time error"

                if int(id) == 1:
                    user.qflag1 = True
                    if user.quest1test <= user.score:
                        user.quest1test = user.score

                elif int(id) == 2:
                    user.qflag2 = True
                    if user.quest2test <= user.score:
                        user.quest2test = user.score

                elif int(id) == 3:
                    user.qflag3 = True
                    if user.quest3test <= user.score:
                        user.quest3test = user.score

                elif int(id) == 4:
                    user.qflag4 = True
                    if user.quest4test <= user.score:
                        user.quest4test = user.score

                elif int(id) == 5:
                    user.qflag5 = True
                    if user.quest5test <= user.score:
                        user.quest5test = user.score

                elif int(id) == 6:
                    user.qflag6 = True
                    if user.quest6test <= user.score:
                        user.quest6test = user.score

                user.total = (user.quest1test + user.quest2test + user.quest3test + user.quest4test + user.quest5test + user.quest6test) // 6
                user.totalScore = (user.quest1test + user.quest2test + user.quest3test + user.quest4test + user.quest5test + user.quest6test)

                user.save()

                a = Questions.objects.all()
                Q = a[user.question_id - 1]

                status = 'Not completed'

                for_count = 0

                for i in testlist:
                    if i == 'pass':
                        for_count += 1

                if for_count == 5:
                    status = 'Completed'
                    Q._submissions += 1
                    Q.save()

                elif for_count == 0:
                    status = 'fail'

                subb.testCaseScore = (for_count / 5) * 100
                subb.save()

                dictt = {'s':user.score,'e':cerror,'d':user.question_id,'t':timer(),'t1':testlist[0],'t2':testlist[1],'t3':testlist[2],'t4':testlist[3],'t5':testlist[4],'status':status}

            return render(request, 'basic_app/Test Casee.html',context=dictt)
    else:
        return HttpResponseRedirect(reverse('register'))


def question_panel(request):
    if request.user.is_authenticated:
        try:
            user = UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            return register(request)

        user.flag = True
        user.save()

        all_user = UserProfileInfo.objects.all()
        accuracy_count = [0, 0, 0, 0, 0, 0]
        user_sub_count = [0, 0, 0, 0, 0, 0]
        percentage_accuracy = [0, 0, 0, 0, 0, 0]

        for user in all_user:
            if user.qflag1:
                user_sub_count[0] += 1
            if user.qflag2:
                user_sub_count[1] += 1
            if user.qflag3:
                user_sub_count[2] += 1
            if user.qflag4:
                user_sub_count[3] += 1
            if user.qflag5:
                user_sub_count[4] += 1
            if user.qflag6:
                user_sub_count[5] += 1

        for user in all_user:

            if user.quest1test == 100:
                accuracy_count[0] += 1
            if user.quest2test == 100:
                accuracy_count[1] += 1
            if user.quest3test == 100:
                accuracy_count[2] += 1
            if user.quest4test == 100:
                accuracy_count[3] += 1
            if user.quest5test == 100:
                accuracy_count[4] += 1
            if user.quest6test == 100:
                accuracy_count[5] += 1

        for i in range(0, 6):
            try:
                percentage_accuracy[i] = int((accuracy_count[i] / user_sub_count[i]) * 100)
            except ZeroDivisionError:
                percentage_accuracy[i] = 0

        all_question = Questions.objects.all()

        a1 = 0

        for i in all_question:
            i.accuracy = percentage_accuracy[a1]
            a1 += 1
            i.save()

        subs = []
        qtitle = []

        for i in range(0,6):
            subs.append(all_question[i]._submissions)
            qtitle.append(all_question[i].questiontitle)

        dict = {'t': timer(), 'a0': percentage_accuracy[0], 'a1': percentage_accuracy[1], 'a2': percentage_accuracy[2],
                'a3': percentage_accuracy[3], 'a4': percentage_accuracy[4], 'a5': percentage_accuracy[5],
                'subs0': subs[0], 'subs1': subs[1], 'subs2': subs[2], 'subs3': subs[3], 'subs4': subs[4],
                'subs5': subs[5], 'qtitle0': qtitle[0], 'qtitle1': qtitle[1], 'qtitle2': qtitle[2],
                'qtitle3': qtitle[3], 'qtitle4': qtitle[4], 'qtitle5': qtitle[5]}

        return render(request,'basic_app/Question Hubb.html', context=dict)
    else:
        return HttpResponseRedirect(reverse('register'))


def leader(request):
    if request.user.is_authenticated:
        a=UserProfileInfo.objects.order_by("total")
        b=a.reverse()
        dict={'list':b,'t': timer()}
        return render(request,'basic_app/Leaderboard.html',context=dict)

    else:
        return HttpResponseRedirect(reverse('register'))


def instructions(request):
    if request.user.is_authenticated:
        try:
            user = UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            user = UserProfileInfo()
        if user.flag:
            return HttpResponseRedirect(reverse('question_panel'))
        if request.method=="POST":
            return HttpResponseRedirect(reverse('question_panel'))
        return render(request,'basic_app/instruction.html')
    else:
        return HttpResponseRedirect(reverse('register'))


def user_logout(request):
    if request.user.is_authenticated:
        try:
            user = UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            return register(request)
        a = UserProfileInfo.objects.order_by("total")
        b = a.reverse()
        counter = 0
        for i in b:
            counter += 1
            if str(i.user) == str(request.user.username):
                break

        dict = {'count': counter, 'name': request.user.username, 'score': user.totalScore}

        logout(request)
        return render(request, 'basic_app/Result.htm', context=dict)
    else:
        return HttpResponseRedirect(reverse('register'))


def register(request):
    if request.user.is_authenticated:
        try:
            user = UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            user = UserProfileInfo()
        if not user.flag:
            return HttpResponseRedirect(reverse('instructions'))
        return HttpResponseRedirect(reverse('question_panel'))
    else:
        try:
            global _flag
            if not _flag:
                return HttpResponseRedirect(reverse('waiting'))
            if request.method == 'POST':
                username = request.POST.get('name')
                username = username.split(" ")[0]

                if username == "":
                    return render(request,'basic_app/Loginn.html')
                password = request.POST.get('password')
                name1 = request.POST.get('name1')

                if name1 == "":
                    return render(request, 'basic_app/Loginn.html')
                name2 = request.POST.get('name2')
                phone1 = request.POST.get('phone1')

                if len(phone1) is not 10:
                    return render(request, 'basic_app/Loginn.html')
                phone2 = request.POST.get('phone1')
                email1 = request.POST.get('email1')

                if email1 == "":
                    return render(request, 'basic_app/Loginn.html')
                email2 = request.POST.get('email2')
                level = request.POST.get('level')

                a = User.objects.create_user( username=username, password=password)

                a.save()
                login(request,a)
                b=UserProfileInfo()
                b.user=a
                b.name1= name1
                b.name2= name2
                b.phone1 = phone1
                b.phone2 = phone2
                b.email1 = email1
                b.email2 = email2
                b.level = level
                b.save()

                return HttpResponseRedirect(reverse('instructions'))

        except IntegrityError:
            return HttpResponse("you have already been registered.")
        return render(request,'basic_app/Loginn.html')


def sub(request):
    user = UserProfileInfo.objects.get(user=request.user)
    a = submissions.objects.filter(user=request.user,qid=user.question_id)
    b=a.reverse()

    dict={'loop':b,'t':timer()}
    return render(request,'basic_app/Submissionn.html',context=dict)


def retry(request,id=1):
    if request.method=="GET":
        user = UserProfileInfo.objects.get(user=request.user)
        a = submissions.objects.filter(user=request.user,qid=user.question_id)
        array=[]
        idd=[]

        for i in a:
            array.append(i.sub)
            idd.append(i.qid)
        var= Questions.objects.all()

        f=idd[int(id)-1]
        q=var[int(f)-1]
        question=q.questions
        dict = {'sub': array[int(id)-1], 'question':question,'s':user.score,'t':timer()}

        return render(request, 'basic_app/Codingg.html', context=dict)
    if request.method=="POST":
        return HttpResponseRedirect(reverse('questions'))


def checkuser(request):
    response_data = {}
    uname = request.POST.get("name")
    check1 = User.objects.filter(username=uname)
    if not check1:
        response_data["is_success"] = True
    else:
        response_data["is_success"] = False
    return JsonResponse(response_data)


def loadbuff(request):
    response_data = {}
    username = request.user.username
    user = UserProfileInfo.objects.get(user=request.user)

    file = '{}/{}/question{}/{}{}.{}'.format(path, username, user.question_id, username, user.attempts,
                                                           user.option)
    f = open(file, "r")
    text = f.read()

    if not text:
        data = ""
    response_data["text"] = text
    return JsonResponse(response_data)


def elogin(request):
    if request.method == 'POST':
        adminpassword = 1
        username = request.POST.get('user')
        password = request.POST.get('pass')
        _password = request.POST.get('pass1')
        user = authenticate(username=username, password=password)

        if user is not None and _password is adminpassword:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('question_panel'))

        else:
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'basic_app/elogin.html', {})
