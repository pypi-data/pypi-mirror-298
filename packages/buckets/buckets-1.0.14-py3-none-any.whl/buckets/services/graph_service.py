from datetime import datetime
from services.config_service import config
import mysql.connector
from matplotlib import pyplot as plt

#from mplfinance import candlestick_ohlc 
import pandas as pd 
import matplotlib.dates as mpl_dates 
import numpy as np 

class GraphService(): 
    
    def show_cases_by_user(self, table):
        print(f"Counting cases by user in {table}...")
        with mysql.connector.connect(**config.db_config) as cnx:
            cursor = cnx.cursor()

            # Set the isolation level to READ UNCOMMITTED
            cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;")
            
            query = (f"select user_id, count(*) from {table} group by user_id;")
            cursor.execute(query)
            
            # Fetch the case counts by user
            case_counts_by_user = cursor.fetchall()
            cursor.close()
            
            fig, ax = plt.subplots(figsize=(12,5))
            
            # Generate a bar graph of the case counts by user
            #ax.bar([case_count[0] for case_count in case_counts_by_user], [case_count[1] for case_count in case_counts_by_user])
            x = [case_count[0] for case_count in case_counts_by_user]
            y = [case_count[1] for case_count in case_counts_by_user]
            y_sum = sum(y)
            y_max = max(y)
            x_max = max(x)
                
            ax.plot(x, y, label='cases?')

            # Set the ticks and labels for the x-axis
            plt.xticks(
                [0,500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000], 
                ["0", "0.5k", "1k", "1.5k", "2k", "2.5k", "3k", "3.5k", "4k", "4.5k", "5k"] 
            )
            
            total_cases_ypos = y_max
            
            multipliers = [
               0, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 
               260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 
               410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 
               560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 
               710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 
               860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000]

            for i in range (1, len(multipliers) - 1):
                mul = multipliers[i]
                prev_mul = multipliers[i-1]
                if (9*prev_mul <= y_max < 9*mul):
                    plt.yticks(
                        [0, 1*mul, 2*mul, 3*mul, 4*mul, 5*mul, 6*mul, 7*mul, 8*mul, 9*mul, 10*mul], 
                        [0, 1*mul, 2*mul, 3*mul, 4*mul, 5*mul, 6*mul, 7*mul, 8*mul, 9*mul, 10*mul], 
                    )                
                    total_cases_ypos = int( 9.5 * mul)

            # Set the title and labels of the graph
            plt.title(f"Cases by User in {table}")
            plt.xlabel("User ID")
            plt.ylabel("Number of Cases")
            plt.text(x=x_max - 50, y= total_cases_ypos, s=f'Total cases: {y_sum:7,}', ha='right', va='top')

            # Save the graph to a file
            filename = f"graph/{table}_{datetime.now().strftime('%m%d%H%M')}.png"

            plt.savefig(filename, bbox_inches='tight')
            #plt.savefig(f"/home/fernando/repos/architect/buckets/buckets/cases_by_user_{table}.png")            
            
            print (f"\n{filename} \ntotal: {y_sum}\n")
            return 
            
            
            # Extracting Data for plotting 
            stock_prices = pd.DataFrame({
                'date': np.array([datetime(2021, 11, i+1) for i in range(7)]), 
                'open': [36, 56, 45, 29, 65, 66, 67], 
                'close': [29, 72, 11, 4, 23, 68, 45], 
                'high': [42, 73, 61, 62, 73, 56, 55], 
                'low': [22, 11, 10, 2, 13, 24, 25]
            }) 

            #data = pd.read_csv("C:/Users/aparn/Desktop/data.csv") 
            #ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']] 
            ohlc = stock_prices.loc[:, ['date', 'open', 'high', 'low', 'close']] 
            
            # Converting date into datetime format 
            ohlc['date'] = pd.to_datetime(ohlc['date']) 
            ohlc['date'] = ohlc['date'].apply(mpl_dates.date2num) 
            ohlc = ohlc.astype(float) 
            
            # Creating Subplots 
            fig, ax = plt.subplots() 
            
            candlestick_ohlc(ax, ohlc.values, width=0.6, 
                            colorup='green', colordown='red', alpha=0.8) 
            
            # Setting labels & titles 
            ax.set_xlabel('Date') 
            ax.set_ylabel('Price') 
            fig.suptitle('Daily Candlestick Chart of NIFTY50') 
            
            # Formatting Date 
            date_format = mpl_dates.DateFormatter('%d-%m-%Y') 
            ax.xaxis.set_major_formatter(date_format) 
            fig.autofmt_xdate() 
            
            fig.tight_layout() 
            
            filename_candle = f"candle_{datetime.now().strftime('%m_%d_%H_%M')}.png"
            plt.savefig(filename_candle)             