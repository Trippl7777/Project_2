# Function for plot1
import pandas as pd
from flask import jsonify

def graph2(sample, db):
    """Return summarized data by selected sample."""
    data = {}
    words = sample.split("1")
    weather = ["base", "Clear", "Mostly Cloudy", "Overcast", "Partly Cloudy", "Rain", "Snow"]
    print(sample)
    for i in range(len(weather)):
        if (weather[i] == "base") :
            stmt1 = "SELECT " + words[1] +", SUM(Count), AVG(Population) FROM sum_crime"
            stmt5 = " GROUP BY " + words[1]
            stmt6 = " ORDER BY " + words[1]
            stmt = stmt1 + stmt5 + stmt6

            df = pd.read_sql_query(stmt, db.bind)
            df["ratio"] = df.iloc[:,1] * 0
            data.update({weather[i] : {"xAxis": df.iloc[:,0].tolist(), "yAxis": df.iloc[:,3].tolist()}})

        else:
            stmt1 = "SELECT " + words[1] +", SUM(Count), AVG(Population) FROM sum_crime"
            stmt2 = " WHERE MapWeather = " + "'" + weather[i] + "'"
            
            if (words[2] == "All"):
                stmt3 = ""
            else:
                stmt3 = " AND MapCrime = '" + words[2] + "'"
            
            if (words[3] == "All"):
                stmt4 = ""
            else:
                stmt4 = " AND City = '" + words[3] + "'"
            
            stmt5 = " GROUP BY " + words[1]
            stmt6 = " ORDER BY " + words[1]
            stmt = stmt1 + stmt2 + stmt3 + stmt4 + stmt5 + stmt6

            df = pd.read_sql_query(stmt, db.bind)
            
            measure = words[4]
            if (measure == "Percentage") :
                divisor = df["SUM(Count)"].sum()
            elif (measure == "Per Capita") :
                divisor = df["AVG(Population)"].sum() / 1000
            else :
                divisor = 1
 
            df["ratio"] = df.iloc[:,1] / divisor            
            data.update({weather[i] : {"xAxis": df.iloc[:,0].tolist(), "yAxis": df.iloc[:,3].tolist()}})

    return jsonify(data)
