from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import sys
import logging
import web_scrap_red_bus
import Scripts.web_scraping_ixigo
import Scripts.best_outcome as best_outcome
import numpy as np
import time
import os
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/', methods=['GET', 'POST'])
def form_detail():
    if request.method == 'POST':
        firstname = request.form.get('fname')
        lastname = request.form.get('lname')
        gender = request.form.get('gender')
        from1 = request.form.get('FROM')
        to1 = request.form.get('TO')
        date = request.form.get('DATE')
        if request.form.get('submit') == 'Submit':
            data1=web_scrap_red_bus.web(from1,to1,date)
            print('hi')
            print(data1.head())
            data2=Scripts.web_scraping_ixigo.web(from1,to1,date)
            print(data2.head())
            data_result = [data1, data2]
            data = pd.concat(data_result)
            data.index = np.arange(1, len(data) + 1)

            html = data.to_html(header='true', table_id='table')
            output = open(r'templates\result.html', 'w')
            output.write(html)
            output.close()
            if len(data) > 9:
                output = open(r'templates\result.html', 'a+')
                fix = open(r'templates\fixed.html', 'r')
                output.write(fix.read())
                fix.close()
                output.close()
                global best_results
                best_results = best_outcome.best_results(data)






            return redirect(url_for('result'))
    return render_template('html_bus_fetch.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/best',methods=['GET','POST'])
def best():
    if request.method=='POST':
        td = request.form.get('Time in Day')
        price = request.form.get('Price')
        rating = request.form.get('Rating')
        speed = request.form.get('Speed')
        if request.form.get('submit') == "Submit":
            print(td, price, rating, speed)
            final_data = best_results.loc[
                    (best_results['Final_Binned'] <= int(price)) & (best_results['Rating_Binned'] >= int(rating)) & (
                            best_results['Time in Day'] == int(td)) & (best_results['Duration_Binned'] >= int(speed))]

            dataset1 = final_data[
                    ['Site','Bus_Type', 'Bus_Name', 'Starting_Time','Starting_From', 'Destination',
                     'Arrival_Time', 'Total_Duration', 'Rating', 'Rated_By', 'Bus_Fare', 'Final_Price',
                     'Seats_Available']]
            if len(dataset1)==0:
                headers = dataset1.columns
                return render_template('empty.html', headers=headers)
            else:
                headers=dataset1.columns
                results=dataset1.values
                return render_template('best_result.html',headers=headers,results=results)



if __name__ == '__main__':
    app.run()