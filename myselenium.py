from selenium import webdriver
import time,pymysql,pyperclip,shutil,os,calendar,logging
from selenium.webdriver.support.select import Select
from datetime import datetime,timedelta
from pykeyboard import PyKeyboard
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.blocking import BlockingScheduler
logging.basicConfig(level=logging.CRITICAL,format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename=r'C:\Users\lenovo\Desktop\自动取表日志.txt',filemode='a')
class MySelenium:
	def __init__(self):
		self.database = None	
		self.cursor = None
		self.data_lists = None
		self.k = PyKeyboard()
	def connect_mysql(self,host,user,passwd,db,charset):
		self.database=pymysql.connect(host=host,user=user,passwd=passwd,db=db,charset=charset)
		self.database.autocommit(True)
		self.cursor=self.database.cursor()
		print('用户{}已成功连接{}数据库'.format(user,db))
	def data_select(self,table_name,select):
		if select:
			sql = 'select * from {} where {};'.format(table_name,select)
			self.cursor.execute(sql)
			self.data_lists=(i for i in self.cursor.fetchall())
			print('已将表{}中{}数据成功取出-----'.format(table_name,select))
		else:
			self.data_lists=()
		self.database.close()
	def selenium_main(self,dr,day_before,operate_lists):
		for operate in operate_lists:
			if operate[0] == 'open_window':
				dr.get(operate[1])
				'''print('打开网页',operate[1])'''
				dr.implicitly_wait(int(operate[-1]))
			elif operate[0] == 'input':
				box=eval('dr.find_element_by_{}(operate[2])'.format(operate[1]))
				box.clear()
				box.send_keys(operate[3])
				time.sleep(int(operate[-1]))
			elif operate[0] == 'click':
				button=eval('dr.find_element_by_{}(operate[2])'.format(operate[1]))
				button.click()
				dr.implicitly_wait(int(operate[-1]))
			elif operate[0] == 'select':
				try:
					option=eval(operate[4])
				except:
					exec('Select(dr.find_element_by_{}(operate[2])).select_by_{}(operate[4])'.format(operate[1],operate[3]))
				else:
					if type(option) == list:
						for o in option:
							exec('Select(dr.find_element_by_{}(operate[2])).select_by_{}(o)'.format(operate[1],operate[3]))
					elif type(option) == int:
						exec('Select(dr.find_element_by_{}(operate[2])).select_by_{}(operate[4])'.format(operate[1],operate[3]))
					else:
						exec('Select(dr.find_element_by_{}(operate[2])).select_by_{}(option)'.format(operate[1],operate[3]))
				time.sleep(int(operate[-1]))
			elif operate[0] == 'deselect':
				try:
					de_option=eval(operate[4])
				except:
					exec('Select(dr.find_element_by_{}(operate[2])).deselect_by_{}(operate[4])'.format(operate[1],operate[3]))
				else:
					if type(de_option) == list:
						for de_o in de_option:
							exec('Select(dr.find_element_by_{}(operate[2])).deselect_by_{}(de_o)'.format(operate[1],operate[3]))
					elif type(de_option) == int:
						exec('Select(dr.find_element_by_{}(operate[2])).deselect_by_{}(operate[4])'.format(operate[1],operate[3]))
					else:
						exec('Select(dr.find_element_by_{}(operate[2])).deselect_by_{}(de_option)'.format(operate[1],operate[3]))
				time.sleep(int(operate[-1]))
			elif operate[0] == 'switch_window':
				windows=dr.window_handles
				dr.switch_to.window(windows[-1])
				try:
					eval('WebDriverWait(dr,500).until(EC.visibility_of(dr.find_element_by_{}(operate[2])))'.format(operate[1]))
				except:
					continue
				time.sleep(int(operate[-1]))
			elif operate[0] == 'tap_key':
				if '_' in operate[1]:
					exec('self.k.tap_key(self.k.{},int(operate[2]),int(operate[3]))'.format(operate[1]))
				else:
					self.k.tap_key(operate[1],int(operate[2]),int(operate[3]))
				time.sleep(int(operate[-1]))
			elif operate[0] == 'clip':
				pyperclip.copy(operate[1])
				time.sleep(int(operate[-1]))
			elif operate[0] == 'press_key':
				exec('self.k.press_key(self.k.{})'.format(operate[1]))
				time.sleep(int(operate[-1]))
			elif operate[0] == 'release_key':
				exec('self.k.release_key(self.k.{})'.format(operate[1]))
				time.sleep(int(operate[-1]))
			elif operate[0] == 'move':
				try:
					path_file=eval(operate[2])
					'''print(path_file)'''
				except:
					path_file=operate[2]
				path=os.path.split(path_file)[0]
				'''print(path)'''
				if not os.path.exists(path):
					os.makedirs(path)
				shutil.move(operate[1],path_file)
				print('已将文件存至',path_file)
				time.sleep(int(operate[-1]))
			elif operate[0] == 'quit':
				dr.quit()
				time.sleep(int(operate[-1]))
	def operate_main(self,driver_kind):
		table_lists=iter(self.data_lists)
		table=next(table_lists)
		while True:
			try:
				shutil.rmtree(r'D:\all_list')
				os.makedirs(r'D:\all_list')
				operate_lists=[eval(table[i]) for i in range(3,43) if table[i]!=None]
				dr=eval('webdriver.{}()'.format(driver_kind))
				self.selenium_main(dr,table[2],operate_lists)
				print('{}表成功提取'.format(table[1]))
				table=next(table_lists)
			except StopIteration:
				break
			except Exception as error:
				logging.critical(error)
				dr.quit()
				self.k.tap_key(self.k.escape_key,2)
				continue
		print('end!所有表操作完毕')
def do_selenium_day():
	myselenium_day=MySelenium()
	myselenium_day.connect_mysql('localhost','root','','myselenium','utf8')
	myselenium_day.data_select('myselenium_table','day_before="1"')
	myselenium_day.operate_main('Ie')
	shutil.rmtree(r'D:\all_list')
	os.mkdir(r'D:\all_list')
def do_selenium_week():
	myselenium_week=MySelenium()
	myselenium_week.connect_mysql('localhost','root','','myselenium','utf8')
	myselenium_week.data_select('myselenium_table','day_before="7"')
	myselenium_week.operate_main('Ie')
	shutil.rmtree(r'D:\all_list')
	os.mkdir(r'D:\all_list')
def do_selenium_error():
	with open(r'C:\Users\lenovo\Desktop\表.txt','r+') as f:
		error_lists=('name="{}"'.format(i.split()[1]) for i in f.readlines()[23:50])
		do_error=" or ".join(error_lists)
	myselenium_error=MySelenium()
	myselenium_error.connect_mysql('localhost','root','','myselenium','utf8')
	myselenium_error.data_select('myselenium_table','{}'.format(do_error))
	myselenium_error.operate_main('Ie')
	shutil.rmtree(r'D:\all_list')
	os.mkdir(r'D:\all_list')
def do_selenium_aim():
	myselenium_day=MySelenium()
	myselenium_day.connect_mysql('localhost','root','','myselenium','utf8')
	myselenium_day.data_select('myselenium_table','name="LTE关键指标挂牌督办A表周报"')
	myselenium_day.operate_main('Ie')
	shutil.rmtree(r'D:\all_list')
	os.mkdir(r'D:\all_list')
if __name__ == '__main__':
	scheduler=BlockingScheduler()
	scheduler.add_job(do_selenium_day,'cron',hour='6',minute='5',second='*')
	#scheduler.add_job(do_selenium_error,'cron',hour='8',minute='31',second='*')
	#scheduler.add_job(do_selenium_week,'cron',day='8-31',day_of_week='mon',hour='15',minute='19',second='*')
	#scheduler.add_job(do_selenium_error,'cron',hour='10',minute='0',second='*')
	#scheduler.add_job(do_selenium_aim,'cron',hour='15',minute='24',second='*')
	scheduler.start()
