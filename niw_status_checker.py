import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import time
import smtplib
from email.mime.text import MIMEText


def status_check(id):
	url = 'https://egov.uscis.gov/cris/Dashboard/CaseStatus.do'
	values = {'appReceiptNum' : id}

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	soup = BeautifulSoup(''.join(the_page))
	a = soup.findAll("div", { "id" : "caseStatus" })
	status = a[0].contents[3].contents[3].contents[2].strip()
	return status


def send_email(id,status,email):
	msg = MIMEText(status)
	msg['Subject'] = "NIW Application status : " + status
	msg['From'] = email
	msg['To'] = email
	s = smtplib.SMTP('localhost')
	s.sendmail(email, [email], msg.as_string())
	s.quit()


def run_status_checker(id,email,t):
	while True:
		status = status_check(id)
		send_email(id,status,email)
		time.sleep(t)

if __name__=="__main__":
	ID = "LI23542059235" # your case number
	email = "abcd@gmail.com" # your email address
	t = 60 * 60 * 24
	run_status_checker(ID,email,t)

# run local smtpd server
# sudo apt-get install opensmtpd
# sudo service opensmtpd restart

