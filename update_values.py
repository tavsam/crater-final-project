import pyodbc
from decimal import Decimal, getcontext
SERVER = 'EngSQL01.franciscan.edu'
DATABASE = 'STDB01'
USER = 'stavani001'
PWD = 'OIJ29r8e3f48$38d'

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PWD};'

getcontext().prec = 28  # Set precision to match float's precision

sqlTable = "flightData" 

def fetchValues():
    # Establish a connection to the SQL Server
    connection = pyodbc.connect(connection_string)
    connection.autocommit = True
    cursor = connection.cursor()  # cursor.execute() is used for queries

    SQL_QUERY = f"select top 1 * from {sqlTable} order by timestamp desc"
    cursor.execute(SQL_QUERY)

    records = cursor.fetchall()
    for item in records:
        decimal1, decimal2, decimal3, decimal4, time1, time2 = item
        rtrn = [decimal1, decimal2, decimal3, decimal4, time1, time2]

    return rtrn

def pushValues(h,fW,sW,v,timerem):
    connection = pyodbc.connect(connection_string)
    connection.autocommit = True
    cursor = connection.cursor()
    
    SQL_QUERY = f"insert into {sqlTable} values({h},{fW},{sW},{v},{timerem},current_timestamp)"
    cursor.execute(SQL_QUERY)
# altitude, fuel w, ship weight, vel, time rem, time stamp

#initialdata = fetchValues()
G = Decimal('-6.67E-11')
height = 1000
fuel_e = Decimal('10')
thrust = Decimal('100')
moonMass = Decimal('7.35E22')
moonRadius = Decimal('1740000')
G_moon = -G * moonMass / (moonRadius + height)**2

# Ensure other calculations also use Decimal values
def updateValuesNormal():
    height = fetchValues()[0]
    fuel_w = fetchValues()[1]
    ship_w = fetchValues()[2]
    v = fetchValues()[3]
    global G_moon

    G_moon = -G * moonMass / (moonRadius + height) ** 2
    trem = (2 * float(height) / float(G_moon)) ** (1 / 2)
    print(trem)

    acceleration = G_moon
    v = v + acceleration
    height = height - v
    pushValues(height, fuel_w, ship_w, v, trem)

def updateValuesThrusters():
    height = fetchValues()[0]
    fuel_w = fetchValues()[1]
    totWeight = fetchValues()[2]
    v = fetchValues()[3]
    global G_moon
    
    if fuel_w > fuel_e:    
        G_moon = -G * moonMass / (moonRadius + height) ** 2
        trem = (2 * float(height) / float(G_moon)) ** (1 / 2)
        print('Thrusters engaged!!')
        totWeight = totWeight - fuel_e
        acceleration_thrust = thrust / totWeight
        acceleration = -(acceleration_thrust + G_moon)
        v = v + acceleration
        height = height - v
        fuel_w = fuel_w - fuel_e
        pushValues(height, fuel_w, totWeight, v, trem)
    else:
        print("Out of Fuel!")
        updateValuesNormal()

# altitude, fuel w, ship weight, vel, time rem, time stamp