from flask import Flask, render_template, request, session, redirect

import more_itertools

import altair as alt
import pandas as pd

alt.data_transformers.disable_max_rows()

app = Flask(__name__)

# These are read-only GLOBAL variables.
mydata = pd.read_csv("data/data.csv")  # From the 51 meg CSV.
#symbols = sorted(mydata.Councils.unique())  # The list of symbols.
types = sorted(mydata.Type.unique()) # list of councils type.
city = mydata[mydata["Type"] == "City"] # list of cities.
cities = sorted(city.Councils.unique()) # sorted list of city council.
county = mydata[mydata["Type"] == "County"] # list of county council.
counties = sorted(county.Councils.unique()) # sorted list of county council.
years = mydata['Years'] # list of years.
Years = sorted(years.unique())# sorted list of years.

#..............................Welcome Page...................................................
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/processcheck0", methods=["POST"])
def process_checks0():
    session['selection'] = list(request.form.keys())
    print("er1"+session['selection'])
    return redirect("/types")


#...............................Council_Type Table starts here................................

def produce_table1(types, size=5):
    output1 = "<table>"
    for chunk in more_itertools.chunked(types, size):
        output1 += "<tr>"
        for s in chunk:
            output1 += f"<td><input type='checkbox' name='{s}' value='{s}'>{s}</td>"
        output1 += "</tr>"
    output1 += "</table>"
    return output1

@app.route("/types", methods = ['POST'])
def show_symbols1():
    the_table1 = produce_table1(types, 1)	
    return render_template("typechecks.html", data=the_table1)


@app.route("/processchecks1", methods=["POST"])
def process_checks1():
    session["location"] = list(request.form.keys())	
    print("loc  "+session['location'][0])
    if (session["location"][0]) == 'City':
        return redirect("/cities")
    else:
        return redirect("/counties")


#..................................City Table Starts here.........................................

def produce_table3(cities, size=10):
    output3 = "<table>"
    for chunk in more_itertools.chunked(cities, size):
        output3 += "<tr>"
        for c in chunk:
            output3 += f"<td><input type='checkbox' name='{c}' value='{c}'>{c}</td>"
        output3 += "</tr>"
    output3 += "</table>"
    return output3


@app.route("/cities")
def show_symbols3():
    the_table3 = produce_table3(cities,3)	
    return render_template("citychecks.html", data=the_table3)


@app.route("/processchecks3", methods=["POST"])
def process_checks3():
    session["selection"] = list(request.form.keys())
    print("cities  "+session['selection'][0])
    return redirect("/Years")



#....................................County starts here...............................................

def produce_table2(counties, size=5):
    output2 = "<table>"
    for chunk in more_itertools.chunked(counties, size):
        output2 += "<tr>"
        for i in chunk:
            output2 += f"<td><input type='checkbox' name='{i}' value='{i}'>{i}</td>"
        output2 += "</tr>"
    output2 += "</table>"
    return output2


@app.route("/counties")
def show_symbols2():
    the_table2 = produce_table2(counties, 5)
    return render_template("countychecks.html", data=the_table2)


@app.route("/processchecks2", methods=["POST"])
def process_checks2():
    session["selection"] = list(request.form.keys())
    print("county  "+session['selection'][0])
    return redirect("/Years")



#....................................Year table starts here............................................

def produce_table4(Years, size=4):
    output4 = "<table>"
    for chunk in more_itertools.chunked(Years, size):
        output4 += "<tr>"
        for y in chunk:
            output4 += f"<td><input type='checkbox' name='{y}' value='{y}'>{y}</td>"
        output4 += "</tr>"
    output4 += "</table>"
    return output4

@app.route("/Years")
def show_symbols4():
    the_table4 = produce_table4(Years, 2)
    return render_template("yearschecks.html", data=the_table4)

@app.route("/processchecks4", methods=["POST"])
def process_checks4():
    session["year"] = list(request.form.keys())
    print (session["year"])
    return redirect("/visual")


#.......................................Visuals starts here...............................................

@app.route("/visual")
def display_the_plot():
    print(session['selection'])
    df = pd.concat(
        mydata[mydata["Councils"] == loc] for loc in session['selection']
    )
    #print(df["Years"])
    df1 = pd.concat(
        df[df["Years"] == int(yr)] for yr in session["year"]
    )
    #print(df1)
    plot = (
        alt.Chart(df1).mark_bar(tooltip = {"content": "data"}).encode(
            x=alt.X("Councils", title="Councils"),
            y=alt.Y("sum(ESB_Connections):Q", title="ESB_Connections"),
            color="Years:N",
            order=alt.Order(
            'Years',
            sort='ascending'
            ),
        ).properties(title = "ESB_Connections For Selected Councils by selected Years",width=100, height=400)
    )
    plot.save("templates/plot.html")
    return render_template("plot.html")





app.secret_key = "you-will-never-guess"

if __name__ == "__main__":
    app.run(debug=True)
