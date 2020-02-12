from django.shortcuts import render,redirect
from svm_app.models import Csv_file,Csv_Features,UserProfileInfo
from svm_app.forms import UserProfileInfoForm, Csv_fileForm, Csv_FeaturesForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from svm.settings import BASE_DIR
import pandas as pd
import os
path = BASE_DIR+'/svm_app/media/'
from django.core.files.storage import FileSystemStorage
import numpy as np
import pandas as pd
import seaborn as sns
sns.set_style('whitegrid')
from sklearn.preprocessing import LabelEncoder
from scipy.stats import norm
from scipy.stats import norm
import re
import pickle
from sklearn.model_selection import train_test_split
X = None
from sklearn.svm import SVC
import pickle
import os
import copy
from django.contrib import messages
classifier = SVC(kernel='linear')
dt1 = ''
file_name=[]
aj =set()
bj=[]
model =[]
Target_value=''
y_pred1=''
y_test=''
contt={}
fe=[]
lent=[]
user=[]
passw=[]
email=[]
tar=[]
good=[]
good1=[]
gooday=''
get_Pickel_list=[]
svm_pickle_file=[]


def user_login(request):
    a=[]
    lst55=[]
    lst=np.array([])
    import mysql.connector as mysql

    connection = mysql.connect(host = "localhost",user = "root",passwd = "root",port = '3306',database = "svm")

    cursor = connection.cursor()

    SQL_select_Query = "select * from UserProfileInfo"



    print('ffffffffffffffffff',SQL_select_Query)

    cursor.execute(SQL_select_Query)
    print("Selecting rows from mobile table using cursor.fetchall")
    mobile_records = cursor.fetchall() 
    print(mobile_records)
    a=[]
       
    for row in mobile_records:
        a.append(row)
    b = pd.DataFrame(a,columns=['id','username','password','email'])    
    b = b.iloc[:,1:3]
    dd = b.values 
    print('dddddddddddd',dd)   

    cursor.close()
    connection.close()

    if request.method=='POST':
        #lst55=[]
        username=request.POST.get('username')
        password=request.POST.get('pass')
        lst55.append(username)
        request.session['user']=str(username)
        request.session['passw']=str(password)
        lst55.append(password)
        lst=np.asarray(lst55)
        print("lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll",lst)
        #s=np.array(lst55)
        #d=np.reshape(s,(1,2))
        #d=list(d)
       # f=pd.DataFrame(d,columns=['username','password'])
        #print("EEEEEEEEEEEEEEEEEEEEEEE",d)
    if 'loginn' in request.POST:    
        for i in range(len(dd)):
            ff=dd[i]
            ff=list(ff)
            print('fffffffffffff',ff)
            if lst55 == ff:
                print('available')
                return redirect('/svm_app/index1/')
        
        
            
        
            
    
        # if user:

        #     if user.is_active:
        #         login(request, user)
        #         return HttpResponseRedirect(reverse('index1'))

        #     else:
        #         return HttpResponse('User is not active')

        # else:
        #     return HttpResponse('Invalid credentials')

    return render(request, 'user_login.html')

def user_register(request):
   
    registered = False  
    if request.method == 'POST':
     # and 'sg' in request.POST:
        username=request.POST.get('username')
        

        
        Email=request.POST.get('email')
        
        

        Password=request.POST.get('pass')
    

        UserProfileInfo.objects.create(Username = username,Password = Password,Email= Email)
        return redirect('/svm_app/login/')
        # UserProfileInfo.objects.create()
        # UserProfileInfo.objects.create()
    return render(request, 'user_registration.html')

def user_logout(request):
    if request.method=='POST':


        return redirect('/svm_app/login/')
    return render(request,'base.html') 


def index1(request):
    global fe,lent, get_Pickel_list
    if request.method=='POST' and 'upsub' in request.POST:
        file = request.FILES.get('myfile')
        request.session['file_name']=str(file)
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file = path + str(file)
        return redirect('svm_app:index2')
    get_Pickel = Csv_file.objects.all()
    user=request.session['user']
    for pkl in get_Pickel:
        get_Pickel_list.append(pkl)

    file_record_id=[]
    import mysql.connector as mysql

    connection = mysql.connect(host = "localhost",user = "root",passwd = "root",port = '3306',database = "svm")
 


    for file_id_id in Csv_file.objects.raw('SELECT file_id FROM csv_file'):

        print("fileffffffffffffffffffffid",file_id_id)
        file_record_id.append(file_id_id)

    
    import mysql.connector as mysql

    connection = mysql.connect(host = "localhost",user = "root",passwd = "root",port = '3306',database = "svm")
 
    cursor = connection.cursor()
   
    count_record=[]
    features_record1=[]
    

    for fid in file_record_id:
        print("fiiiiiiiiiiid",fid)
        count=1
        features_record=[]
        for SQL_select_Query in Csv_Features.objects.raw('SELECT * FROM Csv_Features WHERE file_id=%s',[fid]):
            print('ffffffffffffffffff',SQL_select_Query,fid)
            count+=1

            features_record.append(SQL_select_Query)
        print("rrreeeeeeeeeeeeee",features_record)
        if count==1:
            pass
        else:

            features_record1.append(features_record)
            count_record.append(count)
            print("coooounnnnnnnnnnt",count)
        print("fffffffffffqqqqqqqqqqqqq",features_record1)
      
        

    


            # cursor.execute(SQL_select_Query)
            # print("Selecting rows from mobile table using cursor.fetchall")
            # mobile_records = cursor.fetchall() 
            # out = [item for t in mobile_records for item in t if isinstance(item, str)] 
            # print("leeeeeeeeentttt",out)
    cursor.close()
    connection.close()
    
    # count_record.remove(1)
    # features_record1.remove([])
    get_model=zip(get_Pickel,count_record,features_record1)
    print('lennnnnnnnnnn',count_record)
    print("pickelllllllllll",get_Pickel)
    print("feeeeeeeeeeeeeeeeeeeeeeeeeeeeeerrrrrrr",features_record1)

    if request.method=='POST' and 'pklsub' in request.POST:
        pickle_name=request.POST.get('h')
        return redirect('svm_app:index8a')



    

    #print('--------------------------------------------',a)
    return render(request, '1.html', {'get_model' : get_model,'user':user})



def index2(request):
    global user,good
    print(request.POST)
    file_name=request.session['file_name']
    Data=pd.read_csv(path+'/'+file_name)
    type = []
    a = Data.columns
    for i in a:
        type.append(Data[i].describe(include='all'))

    context = {}
    context1={}
    context=zip(Data.columns,type)
    context1=(Data.values)
   

     
    # cursor.execute(SQL_select_Query)
    # print("Selecting rows from mobile table using cursor.fetchall")
    
    # connection.close()
    # for k in Csv_file.objects.raw('SELECT * FROM Csv_file  WHERE Target = %s', [tar]):
    return render(request, '2.html', {'context':context,'context1':context1})

def index3(request):
    file_name=request.session['file_name']
    Data=pd.read_csv(path+'/'+file_name)
    type = []
    a = Data.columns
    for i in a:
        type.append(Data[i].describe(include='all'))
    
    global Target_value, Feature_value,fe,aj,user,good
    context=zip(Data.columns,type)

    if request.method=='POST':
        Target_value=request.POST.get('radio_name')
        aj.add(Target_value)
        request.session['tar']=str(Target_value)
        print('new@@@@@@@@@@@@@@@@@@@@@@@@@@',aj)
        Feature_value=request.POST.getlist('Feature1')
        Feature_value1=','.join(Feature_value)
        Feature_value2 =''.join(Feature_value1)
        print("leeneeeeeeeeeeeee",len(Feature_value))
        lent.append(len(Feature_value)+1)

        for h in Feature_value:

            fe.append(h)

        print('ggggggggggg',Feature_value2)
        bj.append(Feature_value)
        #print('Target_value------------------------',Target_value)
        #print('Feature_value------------------------',Feature_value)
        file_name=request.session['file_name']
        Data=pd.read_csv(path+'/'+file_name)
        type = []
        a = Data.columns
        new_data = []
        for col in a:
            if col in Feature_value:
                new_data.append(col)
        Feature = Data[new_data]


        for col in a:
            if col in Target_value:
                new_data.append(col)
        Feature = Data[new_data]
        #print("Feature#################################",Feature)
        Feature.to_csv('Feature.csv', index=False)
       # Target_value1 = print(Target_value)

        file_name=request.session['file_name']
        Data=pd.read_csv(path+'/'+file_name)
        type = []
        a = Data.columns
        b = Target_value
        new_data = []
        for col in a:
            if col in b:
                new_data.append(col)
        y = Data[new_data]
        y = y.bfill(axis ='rows')
        y = y.dropna(axis=0)
        y.to_csv(r'y.csv', index = False)

        # Target_value_storage = {}
        # Target_value_storage = Target_value
        # Csv_file.objects.create(Target = Target_value_storage)
        user=request.session['user']
        passw=request.session['passw']
        print("wwwwwwwww",user)
        print("eeeeeeeee",passw)
        import mysql.connector as mysql

        connection = mysql.connect(host = "localhost",user = "root",passwd = "root",port = '3306',database = "svm")


        for k in UserProfileInfo.objects.raw('SELECT * FROM UserProfileInfo  WHERE username = %s AND password= %s', [user,passw]):

            print("nnnnnn",k)
            request.session['good']=str(k)
            print("gggggggg",good)
        
        if request.method=='POST' and 'sub' in request.POST:
            return redirect('/svm_app/index4')



     
    return render(request, '3.html', {'context':context})


   
def index4(request):
    print(request.POST)
    X = pd.read_csv(r'Feature.csv')
    features1=''
    features2=''
    features1 = X.select_dtypes('object').copy()
    features2 = X.select_dtypes(['number']).copy()
    p = features1.head(10)
    q = features2.head(10)
    # c=features1.isnull().sum()
    # d=features2.isnull().sum()
    # obj=zip(p,c)
    # obj1=zip(q,d)
    return render(request, '4.html',{'obj':p,'num':p.values,'obj1':q,'num1':q.values})

def index4a(request):
    print(request.POST)
    X = pd.read_csv(r'Feature.csv')
    operation = []
    a = X.columns
    for i in a:
        operation.append(request.POST.getlist('group'+i))
    #print('/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',operation) 
    features1 = X.select_dtypes('object').copy()
    features2 = X.select_dtypes('number').copy()
    l =[]
    for i in operation:
        l.append(*i)

    d = dict(zip(X, l)) #dictonary of user selected items and their operation        
    
    #for mean
    min_value = []
    for i,j in d.items():
        if j == 'Mean':
            min_value.append(i)
    #for median
    median_value = []
    for i,j in d.items():
        if j == 'Median':
            median_value.append(i)      
    #mode
    mode_number = []
    for i,j in d.items():
        if j == 'Mode':
            mode_number.append(i)
    #print('@@@@@@@@@@@@@', mode_number)        
                    
    #B-Fill
    # bfill_value = []
    # for i,j in d.items():
    #     if j == 'B-Fill':
    #         bfill_value.append(i)

    # #F-Fill
    # ffill_value = []
    # for i,j in d.items():
    #     if j == 'F-Fill':
    #         ffill_value.append(i)





    file_name=request.session['file_name']
    #Data=pd.read_csv(path+'/'+file_name)
    type = []
    a = features2.columns
    new_data = []
    for col in a:
        if col in min_value:
            new_data.append(col)
    min_value = features2[new_data]
    #print('min_value---------------------',min_value)
    min_value = min_value.fillna(min_value.mean())

   
  #  Data=pd.read_csv(path+'/'+file_name)
    type = []
    a = features2.columns
    new_data = []
    for col in a:
        if col in median_value:
            new_data.append(col)
    median_value = features2[new_data]
    #print('median_value---------------------',median_value)
    median_value = median_value.fillna(median_value.median())

    
    a = X.columns
    new_data = []
    for col in a:
        if col in mode_number:
            new_data.append(col)
    mode_number = X[new_data]
    #print('', mode_number)
    for column in mode_number.columns:
        mode_number[column].fillna(mode_number[column].mode()[0], inplace=True)
   

    for i in X.columns:
        if i in min_value:
            X[i]=min_value[i]
    for i in X.columns:
        if i in median_value:
            X[i]=median_value[i]
    for i in X.columns:
        if i in mode_number:
            X[i]=mode_number[i]        
    # for i in X.columns:
    #     if i in bfill_value:
    #         X[i]=bfill_value[i]
    # for i in X.columns:
    #     if i in ffill_value:
    #         X[i]=ffill_value[i]
    #print('',X)        
   # print('X@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',X.isnull().sum())
    X = X.dropna(axis=0)   #only 1st and last null of b-fill and f-fill
    lst = list(features1.columns)
    for i in range(0,len(features1.columns)):
        i
    encode = LabelEncoder()
    aList = []
    for index, num in enumerate(X):
        if num in lst:
            aList.append(index)
    for i in aList:
        
        X.iloc[:,i]=encode.fit_transform(X.iloc[:,i])
        #print('newX#####################################',X)
        X.to_csv(r'p.csv', index=False)
    
    

    return render(request, '4a.html',{'obj2':X,'num2':X.values})




def index5(request):
    file_name=request.session['file_name']
   # Data=pd.read_csv(path+'/'+file_name)
    X = pd.read_csv(r'p.csv')
   # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",X)
    
    # p=Target_value+Feature_value
    

    # X=X[R]
    context4=[]
    Data1=pd.DataFrame(X)
    
     
    numeric=Data1
    lst=[]
    dlst=[]
    dlst=Data1.columns
    for v in numeric.columns:
        imagename=v

        #imagename=re.sub(r"\s+","",imagename)

        #print(imagename)
        print(len(numeric[v]))        
        m=np.mean(numeric[v])
        n=np.std(numeric[v])
        #print(m,n)        
        
        k=len(numeric[v])*len(numeric[v])   
        sns.set(color_codes=True,style="whitegrid")
        sns.distplot(numeric,kde=False,hist=False);
        data_normal = norm.rvs(size=k,loc=m,scale=n)
        ax = sns.distplot(data_normal,
                  bins=100,
                  kde=True,
                  color='skyblue',
                  hist_kws={"linewidth": 100,'alpha':1})
        ax.set(xlabel='Normal Distribution', ylabel='Frequency')
    
        
        fig=ax.get_figure()
        fig.savefig("C:/Users/admin/Desktop/svm_new/svm_app/static/images2/"+imagename+".png")
        s='.png'
        imagename=imagename
        #print('&&&&&&&&&&&&22222222222',imagename)

        lst.append(imagename)
        fig.clear()
    return render(request, '5.html',{'lst':lst,'context':context4})


def index5a(request):
    X = pd.read_csv(r'p.csv')
    operation = []
    a = X.columns
    for i in a:
        operation.append(request.POST.getlist('group'+i))
    #print('#######################################', operation)
    l =[]
    for i in operation:
        l.append(*i)

    d = dict(zip(X, l)) #dictonary of user selected items and their operation
    #print('', d)        
    #minmax Scaler
    minMaxScaler = []
    for i,j in d.items():
        if j == 'minMaxScaler':
            minMaxScaler.append(i)
    #print('#####################', minMaxScaler)        
    #for standard scaler
    standardScaler = []
    for i,j in d.items():
        if j == 'standardScaler':
            standardScaler.append(i) 
    #print('$$$$$$$$$$$$$$$$$$$$444',standardScaler)  
    

    type = []
    a = X.columns
    new_data = []
    for col in a:
        if col in minMaxScaler:
            new_data.append(col)
    minMaxScaler = X[new_data]
    #print('#####################', minMaxScaler)

    type = []
    a = X.columns
    new_data = []
    for col in a:
        if col in standardScaler:
            new_data.append(col)
    standardScaler = X[new_data]
    #print('$$$$$$$$$$$$$$$$$$$$$$$',standardScaler)
    #Standardization
    x_np = pd.DataFrame(standardScaler)
    X1 = (x_np - x_np.mean()) / x_np.std()
    #print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',X1)

    #min-max 

    x_np1 = pd.DataFrame(minMaxScaler)
    X2 = (x_np1 - x_np1.min()) / (x_np1.max() - x_np1.min())
    #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',X2)

    for i in X.columns:
        if i in X1.columns:
            X[i]=X1[i]
    for i in X.columns:
        if i in X2.columns:
            X[i]=X2[i]

   # print('############3', X)
    X.to_csv('scaling.csv', index=False)
    

     
    return render(request, '5a.html',{'obj2':X,'num2':X.values})




def index6(request):
    global model,fe,user,passw,email,tar,good1,gooday,get_Pickel_list,svm_pickle_file
    # path =os.sys.path('C:/Users/Shantanu.Abhi-HP/Desktop/svm/svm_app/media/advertisment/Social_Network_Ads.csv')
    # print('------------------------',path)
    # print('----------------tar---------------', Target_value)
    print("ggggggggggggggppkkkklll",get_Pickel_list)
    if request.method == "POST":
        percent=request.POST.get('size')
        #pickle

       
        request.session['aa'] = model
    

        x=pd.read_csv('scaling.csv')
        # print(aj)
        y1 = pd.DataFrame()
        # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&',new_data)
        y = pd.read_csv('y.csv')
        y = pd.DataFrame(y)
        y1 = pd.read_csv(r'p.csv')
        for i in y1.columns:
             if i not in y:
                y1 = y1.drop(columns = [i])
        #print('################################y1',y1)        

        for i in x.columns:
            if i in y:
                x = x.drop(columns = [i])
        x_train,x_test,y_train,y_test=train_test_split(x,y1,random_state=0)
        from sklearn.svm import SVC
        classifier = SVC()
        classifier.fit(x_train, y_train)
        y_pred = classifier.predict(x_test)


        

        
        from sklearn.metrics import confusion_matrix,accuracy_score
        cm = confusion_matrix(y_test, y_pred)
        acc=accuracy_score(y_pred,y_test)
        acc1 = '{:.2f}'.format(acc)
        #print(acc)
        #print('---------------------',cm)
        cmd = []
        for i in cm:
            for j in i:
                cmd.append(j)

        cmd1=cmd[0:2]
        cmd2=cmd[2:4]
        recall= cmd[3]/(cmd[2]+cmd[3])      
        r='{:.2f}'.format(recall)
        #print(recall)
        precison=cmd[3]/(cmd[1]+cmd[3])
        a='{:.2f}'.format(precison)
        context = {'cmd1':cmd1, 'cmd2':cmd2, 'acc1':acc1,'rec':r,'pre':a}

        if request.method =='POST' and 'submit' in request.POST:
            model=request.POST.get('abc')
            print('moddddddddd', model)
            request.session['svm_pickle_file']=str(model)
            svm_pickle_file=request.session['svm_pickle_file']
            print("goooooooooood",good1)
            good=request.session['good']
            print("gooogdooodododododod",good)


            import mysql.connector as mysql

            connection = mysql.connect(host = "localhost",user = "root",passwd = "root",port = '3306',database = "svm")
            cursor = connection.cursor()

            pk1='SELECT Pickel_file FROM Csv_file'
            cursor.execute(pk1)
            pk2 = cursor.fetchall() 
            for pk in pk2:
                print("pkpkpkpkpkpkkpkpkpkpkpkpk",pk)
                if svm_pickle_file in pk:
                    print('this file name is already taken')
                    mylist=list(pk)
                    del mylist[:]

                    # messages.info(request, 'Your password has been changed successfully!')

                
                    break
            else:
     
                for f in aj:
                    Csv_file.objects.create(Target=f, Pickel_file = svm_pickle_file,user_id=good)

                    
   
   
           
                if request.method=='POST' and 'submit' in request.POST:
                    return redirect('/svm_app/index8')

            # return redirect('/svm_app/index8/')
           


        return render(request, '7.html',context)
      
    return render(request, '6.html')

def index7(request):
    form1=request.POST.get('abc')
    print('bbbbbbbbbbbbb',form1)
    if request.method=='POST':
        form1=request.POST.get('abc')
        form1.save()
        print('vvvvvvvvvvvvvvvvv',form1)
        return redirect('/svm_app/index8/')

    return render(request, '7.html')
        
def isConvertible(value):
    try:
        return(float(value))
    except:
        return value 

def index8(request): 
   # a = [request.POST]
    global dt1,user,tar,good1,fe,gooday,svm_pickle_file
    newData={}
    drop=[]
    col=[]
    lst5=[]
    X = pd.read_csv(r'Feature.csv')
    X = X.dropna(axis=0)
    G=pd.DataFrame(X)
    features1 = X.select_dtypes('object').copy()
    features2 = X.select_dtypes(['number']).copy()
    # print('ooooobbbbbjjjjjj',features1)
    for i in G:
        P=G[i].unique()
        drop.append(P)


    # for j in features2:
    #     drop.append(features2[j].unique())
       

    
    # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",drop)
    svm_pickle_file=request.session['svm_pickle_file']
    print("pspppspsspspssp",svm_pickle_file)
    tar=request.session['tar']
    lst5=[]
    for i in X:
        lst5.append(i)
    lst5.pop(-1)
    import mysql.connector as mysql

    connection = mysql.connect(host = "localhost",user = "root",passwd = "root",port = '3306',database = "svm")
   
    for k in Csv_file.objects.raw('SELECT * FROM Csv_file  WHERE Target= %s AND Pickel_file= %s ',[tar,svm_pickle_file]):

        print("nnnnnn",k)
        request.session['good1']=str(k)
        
    good1=request.session['good1']
    Feature_value_storage = {}
    Feature_value_storage  = fe
    del svm_pickle_file
    del tar

    
        

    for j in Feature_value_storage:

        Csv_Features.objects.create(Features = j,file_id=good1)
    Csv_file.m_info = Csv_Features
    del fe[:]
   
    if request.method=='POST' and 'test' in request.POST:
        for i in lst5:
            test_form=request.POST.get(i)
            newData[i]=test_form
            #print('+++++++++++++++',newData)
        columns = list(newData.keys())
        #print('ccccccc',columns)
        values = list(newData.values())
        #print('valueeeeeeeeeeeee',values)
        arr_len = len(values)
        #print('@@@@@@@@@@@@@@',arr_len)
        df=pd.DataFrame(np.array(values).reshape(1, arr_len), columns=columns)
        #print('dddddddddddddddd',df)

        for i in df:
            df[i]=isConvertible(df[i])
            #print('============',df)
        obj = df.select_dtypes('object').copy()
        num = df.select_dtypes(['number']).copy()
        print('qqqqqqqqqqqq',obj)
        #print('-----------',num)
        # for i in obj:
        #     obj[i].unique()
            

    #   
        lst2 = list(obj.columns) 
        #print('sssssssssssss',lst2)
    #     lst4=[]
    #     lst6=[]  
    #     # print('################################lst4',lst4)
        for i in range(0 ,len(obj.columns)):
            encode = LabelEncoder()
        alist=[]
        for index,num in enumerate(df):
            if num in lst2:
                alist.append(index)
        for i in alist:
            df.iloc[:,i]=encode.fit_transform(df.iloc[:,i])
        #print('pppppppppppppppppppp',df)
       # print('##################################model',model)
        with open('tmp.pckl',  'rb') as fin:
            classifier = pickle.load(fin)
        lst4=[]

        if df.empty==False:
            test1=classifier.predict(df)
            #print('&&&&&&&&&&&&22222222222',test1)
        
               
        for i in test1:
            lst4.append(i)
            #print('lllllllll',lst4)

        y = pd.read_csv('y.csv')
        lst0=[]    
        for i in y.columns:
            lst0.append(i)
            #print("tarrrrrrrrrrrrrrrr",i)     
        dt1=zip(lst0,lst4) 

    


    #--------------------------------------------------------------upload-----------
    if request.method=='POST' and 'upload' in request.POST:
        file = request.FILES.get('myfile')
        Data1=pd.read_csv(file)
        #print('--------------',Data1)
        features3=''
        features4=''
        features3 = Data1.select_dtypes('object').copy()
        features4 = Data1.select_dtypes(['number']).copy()
        #print('featureeeeeeeeeeeeee3',features3)
        #print('featureeeeeeeeeeeeee4',features4)
        #print('nulllllnullllllllnullll',Data1.isnull().sum())
        for column in Data1.columns:
            Data1[column].fillna(Data1[column].mode()[0], inplace=True)
        #print('ghjklhgfdsghjkhgfdgfhjjgh',Data1.isnull().sum())
        Data3=copy.deepcopy(Data1)
        lstobj = list(features3.columns) 
        #print('lololoolololllolooolool',lstobj)
        for i in range(0 ,len(features3.columns)):
            encode = LabelEncoder()
        Blist=[]
        for index,num in enumerate(Data1):
            if num in lstobj:
                Blist.append(index)
        for i in Blist:
            Data1.iloc[:,i]=encode.fit_transform(Data1.iloc[:,i])
        #print("ajajaajajajajajajajajajajaaj",Data1)


        x_std1 = pd.DataFrame(Data1)
        #print('meannnnnnnnn',x_std1.mean())
        #print('stdddddddddddd',x_std1.std())
        Data1 = (x_std1 - x_std1.mean()) / x_std1.std()
        #print('ssssssssssssttnnnnndrrr',standrd_scl)
        

        with open('tmp.pckl', 'rb') as fin:
            classifier = pickle.load(fin)
        test2=classifier.predict(Data1)
        #print('&&&&&&&&&&&&22222222222',test2)
        target=pd.Series(test2)
        Data2=pd.concat([Data3,target],axis=1)
        Data2.dropna(inplace=True)
        Data2.rename( columns={'0':'Result' }, inplace=True)
        # os.remove('scaling.csv')
        # os.remove('Feature.csv')
        # os.remove('p.csv')
        # os.remove('y.csv')
        
        #print('?Q?Q?Q?Q?Q?Q?Q?Q?Q?Q?Q?',Data1)
        return render(request, '8.html', {'lst5':lst5 ,'dt1':dt1,'obj2':Data2,'num2':Data2.values })
    opt=zip(lst5,drop)

    # print('ooooooooooooooooooo',opt)
    return render(request, '8.html', {'opt':opt, 'dt1':dt1})
    # for j in features2:
    #     drop.append(features2[j].unique())
       



def index8a(request):
    global dt1,classifier,lst5,test1,y,drop
    newData={}
    drop=[]
    lst5=[]
    
    
    #print("zzzzzzzzzz",X)
    if request.method=='POST' and 'dropdown' in request.POST:
        a = request.POST['dropdown']
        print(a)
        # import yaml
        # d = yaml.load(a)
        # print(type(d))
        dt = []
        
        #print('bbbbbbbbbbbbb',model) 
        svm_pickle_file=str(a)
            #print('#########################',svm_pickle_file)
        with open(svm_pickle_file, 'rb') as fin:
            x1 = pickle.load(fin)
            X = pd.read_csv(r'Feature.csv')
            X = X.dropna(axis=0)
            features1 = X.select_dtypes('object').copy()
            features2 = X.select_dtypes(['number']).copy()
            for i in X:
                drop.append(X[i].unique())

        
    
            for col in drop:
                print('++++++++++++++++++++++',col)
        x = x1.drop(x1.columns[-1],axis=1)
        
        for i in x:
            lst5.append(i)
        y = x1.iloc[:,-1:]
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",lst5)
        #print(y)
        x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=0)
        from sklearn.svm import SVC
        classifier = SVC()
        classifier.fit(x_train, y_train)

    if request.method=='POST' and 'test' in request.POST:
        for i in lst5:
            test_form=request.POST.get(i)
            newData[i]=test_form
                #print('+++++++++++++++',newData)
        columns = list(newData.keys())
            #print('ccccccc',columns)
        values = list(newData.values())
            #print('valueeeeeeeeeeeee',values)
        arr_len = len(values)
            #print('@@@@@@@@@@@@@@',arr_len)
        df=pd.DataFrame(np.array(values).reshape(1, arr_len), columns=columns)
            #print('dddddddddddddddd',df)

        for i in df:
            df[i]=isConvertible(df[i])
                #print('============',df)
        obj = df.select_dtypes('object').copy()
        num = df.select_dtypes(['number']).copy()
            #print('qqqqqqqqqqqq',obj)
            #print('-----------',num)

        #   
        lst2 = list(obj.columns) 
            #print('sssssssssssss',lst2)
        #     lst4=[]
        #     lst6=[]  
        #     # print('################################lst4',lst4)
        for i in range(0 ,len(obj.columns)):
            encode = LabelEncoder()
        alist=[]
        for index,num in enumerate(df):
            if num in lst2:
                alist.append(index)
        for i in alist:
            df.iloc[:,i]=encode.fit_transform(df.iloc[:,i])
            #print('pppppppppppppppppppp',df)
           # print('##################################model',model)
        lst4=[]
        test1 = []
        if df.empty==False:
            test1=classifier.predict(df)
                #print('&&&&&&&&&&&&22222222222',test1)
            
                   
        for i in test1:
            lst4.append(i)
        print('lllllllll',lst4)
 
        lst0=[]    
        for i in y.columns:
            lst0.append(i)
        print("tarrrrrrrrrrrrrrrr",lst0)     
        dt1=zip(lst0,lst4)
        return render(request, '8a.html', {'lst5':lst5 ,'dt1':dt1})
    


    #--------------------------------------------------------------upload-----------
    if request.method=='POST' and 'upload' in request.POST:
        file = request.FILES.get('myfile')
        Data1=pd.read_csv(file)
        #print('--------------',Data1)
        features3=''
        features4=''
        features3 = Data1.select_dtypes('object').copy()
        features4 = Data1.select_dtypes(['number']).copy()
        #print('featureeeeeeeeeeeeee3',features3)
        #print('featureeeeeeeeeeeeee4',features4)
        #print('nulllllnullllllllnullll',Data1.isnull().sum())
        for column in Data1.columns:
            Data1[column].fillna(Data1[column].mode()[0], inplace=True)
        #print('ghjklhgfdsghjkhgfdgfhjjgh',Data1.isnull().sum())
        Data3=copy.deepcopy(Data1)

        lstobj = list(features3.columns) 
        #print('lololoolololllolooolool',lstobj)
        for i in range(0 ,len(features3.columns)):
            encode = LabelEncoder()
        Blist=[]
        for index,num in enumerate(Data1):
            if num in lstobj:
                Blist.append(index)
        for i in Blist:
            Data1.iloc[:,i]=encode.fit_transform(Data1.iloc[:,i])
        #print("ajajaajajajajajajajajajajaaj",Data1)


        x_std1 = pd.DataFrame(Data1)
        #print('meannnnnnnnn',x_std1.mean())
        #print('stdddddddddddd',x_std1.std())
        Data1 = (x_std1 - x_std1.mean()) / x_std1.std()
        #print('ssssssssssssttnnnnndrrr',standrd_scl)
        test2=classifier.predict(Data1)
        #print('&&&&&&&&&&&&22222222222',test2)
        target=pd.Series(test2)
        Data2=pd.concat([Data3,target],axis=1)
        Data2.dropna(inplace=True)
        Data2.rename( columns={'0':'Result' }, inplace=True)
        #print('?Q?Q?Q?Q?Q?Q?Q?Q?Q?Q?Q?',Data1)
        
        return render(request, '8a.html', {'lst5':lst5 ,'dt1':dt1,'obj2':Data2,'num2':Data2.values})
    opt=zip(lst5,drop)

    return render(request, '8a.html', {'opt':opt,'dt1':dt1})
def index9(request):
    return render(request, '9.html')

