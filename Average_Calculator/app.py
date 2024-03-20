from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Mithun@2003'
app.config["MYSQL_DB"]="AVG_CAL"                   # created tables for prime,rand,even,fibo in avg_cal tables
app.config["MYSQL_CURSORCLASS"]="DictCursor"

mysql = MySQL(app)




class Average:

  def operation(self,type,table_name):
    nums = requests.get(f"http://20.244.56.144/numbers/{type}").json()
    test_server_res=nums["numbers"]
    numbers = set(nums['numbers'])
    numbers = list(numbers)
    numbers.sort()


    cur = mysql.connection.cursor()
    cur.execute(f'select num from {table_name} ')
    data = cur.fetchall()
    prev_data =set()

    if len(data)>0:
      for num in data:
        prev_data.add(num['num'])
      
    new_data =[]
    for number in numbers:
      if number not in prev_data:
        new_data.append(number)

    if len(new_data) >10:
      LENGTH = len(new_data)
      new_data = new_data[LENGTH-10: LENGTH]
    
    cur.execute(f'delete from {table_name}')
    cur.connection.commit()

    for num in new_data:
      print(num)
      cur.execute(f'insert into {table_name}(num) values(%s)',(num,))
    cur.connection.commit()
    cur.close()
    prev_data =list(prev_data)
    return [prev_data,new_data,test_server_res]
  
  
      

      





@app.route("/numbers/<string:id>")
def numbers(id):
  obj = Average()
  if id=='p':
    nums=obj.operation("primes","prime")
  elif id=='r': 
    nums=obj.operation("rand","rand")
  elif id=='e':
    nums=obj.operation("even","even")
  else:
    nums=obj.operation("fibo","fibo")

  res ={'numbers':nums[2],'window_prev_state':nums[0], 'window_curr_state':nums[1],'avg':sum(nums[1])//len(nums[1])}
  return jsonify(res)
  
  



if __name__ =='__main__':
  app.run(debug=True)
