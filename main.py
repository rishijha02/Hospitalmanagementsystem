 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import json
from flask import Flask,render_template,redirect,url_for,request,flash,session,make_response
import random
from datetime import datetime
from datetime import date

with open('config.json','r') as c:
	params=json.load(c)["params"]  
local_server=True

app=Flask(__name__)


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
if(local_server):
	app.config['SQLALCHEMY_DATABASE_URI']=params['local_uri']
else:
	app.config['SQLALCHEMY_DATABASE_URI']=params['prod_uri']
db=SQLAlchemy(app)


class Patient(db.Model):
	ssn=db.Column(db.Integer,nullable=False,primary_key=True)
	id=db.Column(db.Integer,unique=True)
	name=db.Column(db.String(20),nullable=False)
	age=db.Column(db.Integer,)
	doa=db.Column(db.String(12))
	bed=db.Column(db.String(20))
	address=db.Column(db.String(50))
	state=db.Column(db.String(20))
	city=db.Column(db.String(20))
	phn=db.Column(db.String(20))
	email=db.Column(db.String(20))
class Userstore(db.Model):
	username=db.Column(db.String(20),nullable=False,primary_key=True)
	password=db.Column(db.String(20),nullable=False)
	timestamp=db.Column(db.String(20))
class Medicine(db.Model):
	med_id=db.Column(db.String(20),nullable=False,primary_key=True)
	med_name=db.Column(db.String(20),nullable=False)
	med_qty=db.Column(db.Integer)
	rate=db.Column(db.Integer)
class Issued(db.Model):
	sno=db.Column(db.Integer,primary_key=True)
	med_id=db.Column(db.String(20),nullable=False)
	patient_id=db.Column(db.String(20),nullable=False)
	qty_issued=db.Column(db.String(20),nullable=False)
class Diagnostic(db.Model):
	sno=db.Column(db.Integer,primary_key=True)
	
	patient_id=db.Column(db.String(20),nullable=False)
	test_id=db.Column(db.String(20),nullable=False)
class Master(db.Model):
	sno=db.Column(db.Integer,primary_key=True)
	test_id=db.Column(db.String(20),nullable=False)
	test_name=db.Column(db.String(100),nullable=False)
	charge=db.Column(db.Integer,nullable=False)
################Login#################
@app.route("/")
@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/login',methods=['POST'])
def login_post():
	name=request.form.get('username')
	word=request.form.get('password')
	user=Userstore.query.filter_by(username=name).first()
	if user==None:
		flash('invalid user','danger')
		return redirect('login')
	if user and user.password!=word:
		flash('invalid credentials','danger')
		return redirect('login')
	if user and user.password==word:
		session['use']=user.username
		flash('Logged In','success')
		return redirect('home')

###################################################################


#######################  Home  ###################


@app.route('/home')
def home():

	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		time=datetime.now()
		return render_template('home.html',user=user,time=time)

############################# Home ends #########################

#################################### patient Registration##########################
@app.route("/create_patient")
def create_patient():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		return render_template('Create_patient.html')
@app.route("/create_patient",methods=['POST'])
def create_patient_post():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		ssn_id=request.form.get('ssn_id')
		patient_name=request.form.get('patient_name')
		patient_age=request.form.get('patient_age')
		date=request.form.get('Date')
		bed=request.form.get('types')
		address=request.form.get('add')
		state=request.form.get('state')
		city=request.form.get('city')
		phone=request.form.get('num')
		email=request.form.get('email')
		p_id=""
		pid=random.randrange(10000,99999)
		pid=('1'+str(pid))
		p_id=int(pid)

		patiet=Patient.query.filter_by(ssn=ssn_id).first()
		if(patiet):
			flash('already exist','warning')
			return redirect('create_patient')

		

		entry=Patient(ssn=ssn_id,id=p_id,name=patient_name,age=patient_age,doa=date,bed=bed,address=address,state=state,city=city,phn=phone,email=email)
		db.session.add(entry)
		db.session.commit()
		flash('patient Registered successfully','success')
		return render_template('Create_patient.html')

########################### patient registration ends###########################



############################Search Patient########################
@app.route("/search_patient",methods=['GET','POST'])
def search_patient():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		if request.method=='POST':
			patient_id=request.form.get('id')
			pat=Patient.query.filter_by(id=patient_id).first()
			if pat:
				flash("patient found","success")
				return render_template('search_patient.html',patient=pat)
			else:
				flash("patient not found","danger")
				return render_template("search_patient.html")
		return render_template('search_patient.html')


#################Ends###################################



######################Update Patient#####################
@app.route("/update_patient",methods=['GET','POST'])
def update_patient():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		if request.method=='POST':
			patient_id=request.form.get('id')
			patient=Patient.query.filter_by(id=patient_id).first()
			if patient:
				flash("Patient Found","success")
				return render_template('update_patient.html',patient=patient)
			else:
				flash("patient not found: please enter a valid Patient Id","danger")
		return render_template('update_patient.html')
@app.route("/edit/<string:sno>",methods=['GET','POST'])
def edit(sno):
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		if request.method=='POST':
			pat_name=request.form.get('patient_name')
			pat_age=request.form.get('patient_age')
			pat_doa=request.form.get('Date')
			pat_bed=request.form.get('types')
			pat_state=request.form.get('state')
			pat_city=request.form.get('city')
			pat_phn=request.form.get('phn')
			pat_email=request.form.get('email')
			pat_add=request.form.get('address')
			patient=Patient.query.filter_by(id=int(sno)).first()
			patient.name=pat_name
			patient.age=pat_age
			patient.doa=pat_doa
			patient.bed=pat_bed
			patient.address=pat_add
			patient.state=pat_state
			patient.city=pat_city
			patient.phn=pat_phn
			patient.email=pat_email
			db.session.commit()
			flash("Edited successfully","success")
			return redirect('/update_patient')
		patient=Patient.query.filter_by(id=int(sno)).first()

		return render_template('edit.html',patient=patient)


#######################Ends#######################################


############################Delete Patient###########################

@app.route("/delete_patient",methods=['GET','POST'])
def delete_patient():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		if request.method=='POST':
			patient_id=request.form.get('id')
			patient= Patient.query.filter_by(id=patient_id).first()
			if patient:
				flash("patient found","success")
				db.session.delete(patient)
				db.session.commit()
				return render_template('delete_patient.html',patient=patient)
			else:
				flash('patient not found')

		return render_template('delete_patient.html')


#########################Ends####################



#######################view Patient#############################
@app.route("/view_patient")
def view_patient():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		patient=Patient.query.all()
		return render_template('views.html',patient=patient)

#######################Ends#######################


@app.route("/issue_medicine",methods=['GET','POST'])
def issue_medicine():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		name=request.form.get('name')
		qty=request.form.get('qty')
		hid=request.form.get('h1')
		pat_id=request.form.get('id')
		patients=Patient.query.all()
		if name:
			k=Medicine.query.filter_by(med_name=name).first()
			if k:
				if k.med_qty>0:
					flash('available','info')
					return render_template('issue_medicine.html',k=k,patients=patients)
				else:
					flash('not available','danger')
					print('not')
					return render_template('issue_medicine.html',patients=patients)
			if k==None:
				flash('invalid medicine name','danger')
				return render_template('issue_medicine.html',patients=patients)
		elif qty and hid:
			k2=Medicine.query.filter_by(med_id=hid).first()
			print(k2)
			if k2:
				
				
				if k2.med_qty<int(qty):
					flash('out of stock',"danger")
					return render_template('issue_medicine.html',patients=patients)
				k2.med_qty=int(k2.med_qty)-int(qty)
				db.session.commit()
				mid=k2.med_id
				flash("issued","success ")
				new=Issued(med_id=mid,patient_id=pat_id,qty_issued=qty)
				db.session.add(new)
				db.session.commit()
				return render_template('issue_medicine.html',patients=patients)
		return render_template('issue_medicine.html',patients=patients)


@app.route("/getpatient")
def get_patient1():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		return render_template('get_patient.html')


@app.route("/getpatient", methods=['POST'])
def get_patient():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
	    c=None
	    r=[]
	    r2=[]
	    r3=[]
	    pat_id = request.form.get('id')
	    if pat_id    :
	        c=Patient.query.filter_by(id=pat_id).first()
	        
	        if c:
	            d=Issued.query.filter_by(patient_id=pat_id).all()
	            
	            if d:
	                flash("Patient Found with medicine Information","success")
	                for i in d:
	                    r2.append(i.med_id)
	                    r3.append(i.qty_issued)
	                r2=list(set(r2))
	                l=len(r3)-1
	                print(r2,r3)

	                for i in r2:
	                    mid=i
	                    p=Medicine.query.filter_by(med_id=mid).first()
	                    if p:
	                        r.append(p)
	                resp=make_response(render_template('get_patient.html',c=c,d=d,r3=r3,l=l,r=r))
	                resp.set_cookie('obj5',pat_id)
	                return resp
	                
	            flash("Patient Found with No Medicine information","danger")
	            resp=make_response(render_template("get_patient.html",c=c))
	            resp.set_cookie('obj5',pat_id)
	            return resp


	        
	        flash("Patient not found","danger")
	        return render_template('get_patient.html')




@app.route("/getpatient2")
def add_diagnostic():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		return render_template("get_patient2.html")
	

@app.route("/getpatient2", methods=['GET', 'POST'])
def get_patient2():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		c=None
		r=[]
		ssn_id=request.form.get('id')
		if ssn_id:
			c=Patient.query.filter_by(id=ssn_id).first()
			if c:
				d=Diagnostic.query.filter_by(patient_id=ssn_id).all()
				if d:
					for i in d:
						mid=i.test_id
						p=Master.query.filter_by(test_id=mid).first()
						if p:
							r.append(p)
					print(d,r,c)
					resp=make_response(render_template('get_patient2.html',c=c,d=d,r=r))
					resp.set_cookie('obj6',ssn_id)
					return resp
				resp=make_response(render_template("get_patient2.html",c=c))
				resp.set_cookie('obj6',ssn_id)
				return resp
			flash('patient not found')
			return render_template('get_patient2.html')


    

@app.route("/add_diagnostics",methods=['GET','POST'])
def add_diagnostics():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		tst=Master.query.all()
		if request.method=='POST':
			patient=Patient.query.all()
			name=request.form.get('name')
			test=Master.query.filter_by(test_name=name).first()
			t_id=request.form.get('t_id')
			pat_id=request.form.get('id')
			if test:
				
				return render_template('add_diagnostics.html',test=test,patient=patient)
			new_test=Diagnostic(patient_id=pat_id,test_id=t_id)
			db.session.add(new_test)
			db.session.commit()
		return render_template('add_diagnostics.html',tst=tst)






################Final billing##########
@app.route("/final_bill",methods=['GET','POST'])
def final_bill():
	user=Userstore.query.filter_by(username=session['use']).first()
	if 'use' in session and session['use']==user.username:
		r=[]
		r2=[]
		gt=0
		bcharge=0
		dcharge=0
		mcharge=0
		if request.method=='POST':
			pat_id=request.form.get('id')
			if pat_id:
				c=Patient.query.filter_by(id=pat_id).first()
				if c:
					today=date.today()
					d0=c.doa
					d1=today
					day=d1-d0
					nday=str(day)
					for i in range(len(nday)):
						if nday[i]==' ':
							pos=i
							break
					nday=nday[:pos]
					nday=int(nday)
					if c.bed=='General ward':
						bcharge=nday*2000
					elif c.bed=='Semi sharing':
						bcharge=nday*4000
					elif c.bed=='Single room':
						bcharge=nday*8000
	 
					d=Issued.query.filter_by(patient_id=pat_id).all()
					k=Diagnostic.query.filter_by(patient_id=pat_id).all()
					if d or k:
						if d:
							for i in d:
								m_id=i.med_id
								p=Medicine.query.filter_by(med_id=m_id).first()
								if p:
									mcharge=mcharge+(p.rate*i.qty_issued)
									r.append(p)
						if k:
							for i in k:
								t_id=i.test_id
								p2=Master.query.filter_by(test_id=t_id).first()
								if p2:
									dcharge=dcharge+(p2.charge)
									r2.append(p2)
						
					gt=bcharge+mcharge+dcharge
					return render_template('final_bill.html',c=c,today=today,nday=nday,d=d,k=k,r=r,r2=r2,gt=gt,bcharge=bcharge,mcharge=mcharge,dcharge=dcharge)
		return render_template('final_bill.html')
	return "<h1> sorry</h1>"


@app.route("/logout")
def logout():
	session.pop('use')
	return redirect('/login')