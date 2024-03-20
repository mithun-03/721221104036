from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Mithun@2003'
app.config["MYSQL_DB"]="AVG_CAL"
app.config["MYSQL_CURSORCLASS"]="DictCursor"

mysql = MySQL(app)




class Average:

  def primes(self):
    nums = requests.get("http://20.244.56.144/numbers/primes").json()
    numbers = set(nums['numbers'])
    numbers = list(numbers)
    numbers.sort()


    cur = mysql.connection.cursor()
    cur.execute('select num from prime ')
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
    
    cur.execute('delete from prime')
    cur.connection.commit()

    for num in new_data:
      print(num)
      cur.execute('insert into prime(num) values(%s)',(num,))
    cur.connection.commit()
    cur.close()
    prev_data =list(prev_data)
    return [prev_data,new_data]
      

      





@app.route("/numbers/<string:id>")
def numbers(id):
  obj = Average()
  if id=='p':
    nums=obj.primes()
    res ={'prev_window':nums[0], 'curr_window':nums[1],'avg':sum(nums[1])/len(nums[1])}
 
    return jsonify(res)


if __name__ =='__main__':
  app.run(debug=True)
