import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import mysql.connector
connection = mysql.connector.connect(
    host=st.secrets["DB_HOST"],                   # Database host
    user=st.secrets["DB_USER"],                   # Database username
    password=st.secrets["DB_PASSWORD"],           # Database password  
    allow_local_infile=True,
    database=st.secrets["DB_NAME"]                # Database name
)

cursor = connection.cursor() 

st.logo('C:/Users/HP/Downloads/ola-cabs-logo-svgrepo-com.jpg', size = 'large')

def home_page():
    tab1, tab2 = st.tabs(['Home', 'Dashboard'])
    tab1.title("Ola Ride Insights")
    tab1.write('\n')
    tab1.image('C:/Users/HP/Downloads/OLA Imagee.png')
    tab1.write('\n')
    tab1.write("OLA Ride Analysis provides critical visibility into ride-hailing data to figure out trip cancellation patterns, driver ratings and revenue distributions. We perform this analysis to identify common problems and reduce customer wait times. By evaluating passenger feedback and payment preferences, we can see what annoys riders and make the app better. Ultimately, this research is conducted to transform raw telemetry into data-driven strategies that maximize company profitability while elevating overall user satisfaction.")
    tab1.write('\n')
    tab1.write("For detailed analysis 📈, navigate through each analysis on the left..")
    tab2.image('D:/VSCODE/Project_OLA/OLA Rides Dashboard.png')

def successful_bookings():
    queryall = """
    SELECT * FROM OLA_RidesData
    WHERE Booking_Status = 'Success'
    LIMIT 5;
    """

    cursor.execute(queryall)
    data_result1 = cursor.fetchall()
    column_data1 = [desc[0] for desc in cursor.description]
    table1 = pd.DataFrame(data_result1, columns = column_data1)
    st.title("All Successful Bookings")
    st.write('\n')
    st.table(table1)
    st.write("These are the top five rows for successful bookings.")
    st.write('\n')
    st.subheader("Here is the detailed analysis for successful bookings...")
    st.write('\n')
    
    query_vs = """
    SELECT COUNT(CASE WHEN Booking_Status = 'Success' THEN 1 END) AS Successful_Bookings, COUNT(CASE WHEN Booking_Status != 'Success' THEN 1 END) AS Unsuccessful_Bookings
    FROM OLA_RidesDATA;
    """
    cursor.execute(query_vs)
    data_result2 = cursor.fetchall()
    column_data2 = [desc[0] for desc in cursor.description]
    table2 = pd.DataFrame(data_result2, columns = column_data2)
    
    query_rate = """
    SELECT Vehicle_Type, 100*COUNT(CASE WHEN Booking_Status = 'Success' THEN 1 END)/COUNT(*) AS SUCCESS_RATE
    FROM OLA_RidesDATA
    GROUP BY Vehicle_Type;
    """
    cursor.execute(query_rate)
    data_result3 = cursor.fetchall()
    column_data3 = [desc[0] for desc in cursor.description]
    table3 = pd.DataFrame(data_result3, columns = column_data3)

    query_time = """
    SELECT AVG(V_TAT) AS AVERAGE_V_TAT, AVG(C_TAT) AS AVERAGE_C_TAT
    FROM OLA_RidesDATA
    WHERE V_TAT != -1 AND C_TAT != -1; 
    """
    cursor.execute(query_time)
    data_result4 = cursor.fetchall()
    column_data4 = [desc[0] for desc in cursor.description]
    table4 = pd.DataFrame(data_result4, columns = column_data4)

    query_pay = """
    SELECT Payment_Method, COUNT(*) AS USAGE_COUNT 
    FROM OLA_RidesDATA
    WHERE Payment_Method != 'Not Applicable'
    GROUP BY Payment_Method;
    """
    cursor.execute(query_pay)
    data_result5 = cursor.fetchall()
    column_data5 = [desc[0] for desc in cursor.description]
    table5 = pd.DataFrame(data_result5, columns = column_data5)

    col1, col2 = st.columns(2, gap = 'medium')
    col1.write('**Successful vs Unsuccessful Count:**')
    col1.table(table2)
    col1.write('\n')

    col2.write('**Average V_TAT and C_TAT:**')
    col2.table(table4)
    col2.write('\n')

    col1.write('**Success rate for each vehicle:**')
    fig, ax = plt.subplots()
    ax.bar(table3['Vehicle_Type'], table3['SUCCESS_RATE'])
    for xy in zip(table3['Vehicle_Type'], table3['SUCCESS_RATE']):
        ax.annotate(f'{round(xy[1],1)}%', xy=xy)
    ax.set_xlabel("\nVehicle Type")
    ax.set_ylabel("Success Rate\n")
    col1.pyplot(fig)
    col1.write('\n')

    col2.write('**Different payment methods usage:**')
    fig, ax = plt.subplots()
    ax.bar(table5['Payment_Method'], table5['USAGE_COUNT'])
    for xy in zip(table5['Payment_Method'], table5['USAGE_COUNT']):
        ax.annotate(f'{xy[1]}', xy=xy)
    ax.set_xlabel("\nPayment Methods")
    ax.set_ylabel("Usage Count\n")
    col2.pyplot(fig)
    
    

def Vehicle_Types():
    st.title("Vehicle Types")
    st.subheader("We have the following vehicle types")
    col1,col2,col3,col4,col5,col6,col7 = st.columns(7, gap='small')
    col1.write('Bike')
    col1.image('https://cdn-icons-png.flaticon.com/128/9983/9983173.png')
    col2.write('Prime SUV')
    col2.image('https://cdn-icons-png.flaticon.com/128/9983/9983204.png')
    col3.write('Mini')
    col3.image('https://cdn-icons-png.flaticon.com/128/3202/3202926.png')
    col4.write('Prime Plus')
    col4.image('https://cdn-icons-png.flaticon.com/128/11409/11409716.png')
    col5.write('Auto')
    col5.image('https://cdn-icons-png.flaticon.com/128/16526/16526595.png')
    col6.write('eBike')
    col6.image('https://cdn-icons-png.flaticon.com/128/6839/6839867.png')
    col7.write('Prime Sedan')
    col7.image('https://cdn-icons-png.flaticon.com/128/14183/14183770.png')
    st.write('\n')

    query2 = """
        SELECT Vehicle_Type, AVG(Ride_Distance) AS Average_Ride_Distance
        FROM OLA_RidesData
        WHERE Ride_Distance != 0 
        GROUP BY Vehicle_Type;
    """

    cursor.execute(query2)
    data_result6 = cursor.fetchall()
    column_data6 = [desc[0] for desc in cursor.description]
    table6 = pd.DataFrame(data_result6, columns=column_data6)
    st.subheader("Average Ride Distance For Each Vehicle Type")
    st.table(table6)
    st.write('\n')
    st.write('This analysis shows average ride distance for each vehicle type. By this it is understood that vehicle types with more average distance are used for long distances and vehicle types with less average distance are used for small distance destinations. So we have to increase the availability of the vehicles(which have more average distance) in the places where people generally take long distance rides like airports or hotels and accordingly we have to increase the availability of vehicles(which have less average distance) in the places where people tend to take short rides.')
    st.write('\n')

    def rides_count(x):
        query_count = f"""
        SELECT COUNT(CASE WHEN Booking_Status = 'Success' THEN 1 END) AS SUCCESS_RIDES,
        COUNT(CASE WHEN Booking_Status = 'Canceled by Driver' THEN 1 END) AS DRIVER_CANCELED_RIDES,
        COUNT(CASE WHEN Booking_Status = 'Canceled by Customer' THEN 1 END) AS CUSTOMER_CANCELED_RIDES,
        COUNT(CASE WHEN Booking_Status = 'Driver Not Found' THEN 1 END) AS DRIVER_NOT_FOUND_RIDES
        FROM OLA_RidesDATA
        WHERE Vehicle_Type = '{x}';
        """
        cursor.execute(query_count)
        data_result7 = cursor.fetchall()
        column_data7 = [desc[0] for desc in cursor.description]
        table7 = pd.DataFrame(data_result7, columns=column_data7)
        st.table(table7)
    st.subheader("Successful and Canceled rides for each vehicle type")
    st.write("Now, lets see the successful, driver canceled, customer canceled rides for each vehicle type. By this we can understand which vehicle type have more successful rides and which vehicle type have more canceled rides.")
    selection = st.selectbox('Choose a vehicle type below..',['Choose', 'Bike', 'Prime SUV', 'Mini', 'Prime Plus', 'Auto', 'eBike', 'Prime Sedan'])
    if selection:
        if selection != 'Choose':
            rides_count(selection)
    
    st.write('\n')
    st.subheader("Successful vs Unsuccessful Rides")
    st.write('Lets visualize successful vs unsuccessful rides for each vehicle type...')
    query_group = """
    SELECT Vehicle_Type, COUNT(CASE WHEN Booking_Status = 'Success' THEN 1 END) AS SUCCESS_RIDES, 
    COUNT(CASE WHEN Booking_Status != 'Success' THEN 1 END) AS UNSUCCESS_RIDES
    FROM OLA_RidesDATA
    GROUP BY Vehicle_Type;
    """
    cursor.execute(query_group)
    data_result8 = cursor.fetchall()
    column_data8 = [desc[0] for desc in cursor.description]
    table8 = pd.DataFrame(data_result8, columns=column_data8)
    table_grouped = table8.set_index('Vehicle_Type')
    fig, ax = plt.subplots()
    table_grouped.plot(kind='bar', ax=ax)
    ax.set_xlabel('Vehicle type')
    ax.set_ylabel('Rides Count\n')
    for container in ax.containers:
        ax.bar_label(container, padding = 3, rotation = 90)
    ax.set_ylim(0, max(table8['SUCCESS_RIDES']) * 1.2) 
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), title="Ride Status")
    st.pyplot(fig)
    
def Customer_Canceled():
    query_c_cancel = """ 
    SELECT COUNT(*) AS Customer_Canceled_Rides
    FROM OLA_RidesDATA
    WHERE Booking_Status = 'Canceled by Customer'
    """
    cursor.execute(query_c_cancel)
    data_result9 = cursor.fetchall()
  
    st.title("Cancelled Rides by Customers")
    st.write('\n')
    st.metric("Total Cancelled Rides", value=data_result9[0][0])
    st.write("This is the total number of canceled rides by customers due to various reasons. Lets see the reasons for this, so that we can work on those reasons and find solutions for that to get rid of cancelations if possible.")
    st.write('\n')
    st.subheader("Reasons for canceling")

    query_reason1 = """ 
    SELECT Canceled_Rides_by_Customer AS REASON_FOR_CANCELING, COUNT(*) AS NO_OF_TIMES_CANCELED
    FROM OLA_RidesDATA
    WHERE Booking_Status = 'Canceled by Customer'
    GROUP BY Canceled_Rides_by_Customer;
    """
    cursor.execute(query_reason1)
    data_result10 = cursor.fetchall()
    column_data10 = [desc[0] for desc in cursor.description]
    table10 = pd.DataFrame(data_result10, columns=column_data10)
    st.table(table10)
    st.write('\n')
    st.write("Here we have the reasons for canceling the ride and number of times the ride got cancelled because of that reason. In this the last two reasons 'Change of plans' and 'Wrong address' are depended on customer, so we can't do anything for that. But the first three reasons are depended on driver and vehicle, so we have to work on those issues and resolve them to improve the business.")

def Driver_Canceled():
    query_d_cancel = """ 
    SELECT COUNT(*) AS Driver_Canceled_Rides
    FROM OLA_RidesDATA
    WHERE Booking_Status = 'Canceled by Driver'
    """
    cursor.execute(query_d_cancel)
    data_result11 = cursor.fetchall()
  
    st.title("Cancelled Rides by Drivers")
    st.write('\n')
    st.metric("Total Cancelled Rides", value=data_result11[0][0])
    st.write("This is the total number of canceled rides by drivers due to various reasons. Lets see the reasons for this, so that we can work on those reasons and find solutions for that to get rid of cancelations if possible.")
    st.write('\n')
    st.subheader("Reasons for canceling")

    query_reason2 = """ 
    SELECT Canceled_Rides_by_Driver AS REASON_FOR_CANCELING, COUNT(*) AS NO_OF_TIMES_CANCELED
    FROM OLA_RidesDATA
    WHERE Booking_Status = 'Canceled by Driver'
    GROUP BY Canceled_Rides_by_Driver;
    """
    cursor.execute(query_reason2)
    data_result12 = cursor.fetchall()
    column_data12 = [desc[0] for desc in cursor.description]
    table12 = pd.DataFrame(data_result12, columns=column_data12)
    st.table(table12)
    st.write('\n')
    st.write("Here we have the reasons for canceling the ride and number of times the ride got cancelled because of that reason. In this we have to mainly focus on 'Personal & Car related issue' and find solutions for that.")

def Top_Customers():
    query_cust = """ 
    SELECT Customer_ID, COUNT(*) AS No_Of_Rides
    FROM OLA_RidesDATA
    GROUP BY Customer_ID
    ORDER BY No_Of_Rides DESC
    LIMIT 5;
    """
    cursor.execute(query_cust)
    data_result13 = cursor.fetchall()
    column_data13 = [desc[0] for desc in cursor.description]
    table13 = pd.DataFrame(data_result13, columns=column_data13)
    st.title("Frequent Customers")
    st.subheader("Top 5 customers with highest number of rides")
    st.table(table13)
    st.write('\n')
    st.write("These are the top 5 customers who travelled more with OLA. Lets see which vehicle types does these customers used more, so we can understand with which vehicle type they are more comfortable.")
    st.write('\n')
    st.subheader("Most Used Vehicle types ")
    st.write("Click on the respective 'Customer ID' button below to view their most used vehicle types.")
    def Customer_Vehicle(customer):
        query_custv = f""" 
        SELECT Vehicle_Type, COUNT(*) AS No_Of_Times_Used
        FROM OLA_RidesDATA
        WHERE Customer_ID = '{customer}'
        GROUP BY Customer_ID, Vehicle_Type
        ORDER BY No_Of_Times_Used DESC;
        """
        cursor.execute(query_custv)
        data_result14 = cursor.fetchall()
        column_data14 = [desc[0] for desc in cursor.description]
        table14 = pd.DataFrame(data_result14, columns=column_data14)
        st.table(table14)
    
    if st.button('CID954071'):
        Customer_Vehicle('CID954071')
    if st.button('CID539191'):
        Customer_Vehicle('CID539191')
    if st.button('CID189965'):
        Customer_Vehicle('CID189965')
    if st.button('CID268274'):
        Customer_Vehicle('CID268274')
    if st.button('CID952434'):
        Customer_Vehicle('CID952434')

    st.write("Acoording to this 'Bike' is the most used vehicle type.")

def Driver_Ratings():
    query_D_ratings = """ 
    SELECT Vehicle_Type, MAX(Driver_Ratings) AS Max_Rating, MIN(Driver_Ratings) AS Min_Rating, AVG(Driver_Ratings) AS Average_Rating
    FROM OLA_RidesDATA
    WHERE Driver_Ratings != -1.0
    GROUP BY Vehicle_Type;
    """
    cursor.execute(query_D_ratings)
    data_result15 = cursor.fetchall()
    column_data15 = [desc[0] for desc in cursor.description]
    table15 = pd.DataFrame(data_result15, columns=column_data15)
    st.title("Driver Ratings")
    st.subheader("Min, Max, Average driver ratings for each vehicle type")
    st.table(table15)
    st.write('\n')
    st.write("This is the minimum and maximum rating given by customers to the drivers for each vehicle type. According to this each vehicle type have good and less rating. Now lets deep dive into this to understand about ratings even better.")
    st.write('\n')
    st.subheader("Rating 3 vs Rating 5")
    st.write('\n')

    query_3 = """ 
    SELECT Vehicle_Type, COUNT(*) AS COUNT 
    FROM OLA_RidesDATA
    WHERE Driver_Ratings = 3.0
    GROUP BY Vehicle_Type
    ORDER BY COUNT DESC;
    """
    cursor.execute(query_3)
    data_result16 = cursor.fetchall()
    column_data16 = [desc[0] for desc in cursor.description]
    table16 = pd.DataFrame(data_result16, columns=column_data16)

    query_5 = """ 
    SELECT Vehicle_Type, COUNT(*) AS COUNT 
    FROM OLA_RidesDATA
    WHERE Driver_Ratings = 5.0
    GROUP BY Vehicle_Type
    ORDER BY COUNT DESC;
    """
    cursor.execute(query_5)
    data_result17 = cursor.fetchall()
    column_data17 = [desc[0] for desc in cursor.description]
    table17 = pd.DataFrame(data_result17, columns=column_data17)

    col1, col2 = st.columns(2, gap = 'small')
    fig, ax = plt.subplots()
    ax.bar(table16['Vehicle_Type'], table16['COUNT'])
    for xy in zip(table16['Vehicle_Type'], table16['COUNT']):
        ax.annotate(xy[1], xy=xy)
    ax.set_title('Count of rating 3 for each vehicle type\n', fontweight='bold')
    ax.tick_params(axis="x", rotation=90)
    ax.set_xlabel('\nVehicle types')
    ax.set_ylabel('Count\n')
    col1.pyplot(fig)

    fig, ax = plt.subplots()
    ax.bar(table17['Vehicle_Type'], table17['COUNT'])
    for xy in zip(table17['Vehicle_Type'], table17['COUNT']):
        ax.annotate(xy[1], xy=xy)
    ax.set_title('Count of rating 5 for each vehicle type\n', fontweight='bold')
    ax.tick_params(axis="x", rotation=90)
    ax.set_xlabel('\nVehicle types')
    ax.set_ylabel('Count\n')
    col2.pyplot(fig)
    
    st.write('\n')
    st.write("Now it is clearly understandable which vehicle type have more number of Rating 3 and Rating 5. According to this we can implement solutions and improve the ratings")

def Customer_Ratings():
    query_C_ratings = """ 
    SELECT Vehicle_Type, AVG(Customer_Rating) AS Average_Rating
    FROM OLA_RidesDATA
    WHERE Customer_Rating != -1.0
    GROUP BY Vehicle_Type;
    """
    cursor.execute(query_C_ratings)
    data_result18 = cursor.fetchall()
    column_data18 = [desc[0] for desc in cursor.description]
    table18 = pd.DataFrame(data_result18, columns=column_data18)
    st.title("Customer Ratings")
    st.subheader("Average customer ratings for each vehicle type")
    st.table(table18)
    st.write('\n')
    st.write("These are the average customer ratings(Rating given by driver to customer) for each vehicle type. We have almost same average ratings for each vehicle type.")

def Payment_Methods():
    query_pay = """
    SELECT Payment_Method, COUNT(*) AS USAGE_COUNT 
    FROM OLA_RidesDATA
    WHERE Payment_Method != 'Not Applicable'
    GROUP BY Payment_Method;
    """
    cursor.execute(query_pay)
    data_result19 = cursor.fetchall()
    column_data19 = [desc[0] for desc in cursor.description]
    table19 = pd.DataFrame(data_result19, columns=column_data19)
    st.title("Payment Methods")
    st.subheader("Different payment methods usage")
    st.table(table19)
    st.write('\n')
    st.write("These are the number of transactions made by customers through each payment method. Accordting to this 'Cash' is the most used payment method, so it is clear that customers are preferring cash payments over other which can be because of various reasons.")
    st.write('\n')
    
    st.subheader("Revenue made through each payment method")
    query_rev = """ 
    SELECT Payment_Method, SUM(Booking_Value) AS REVENUE_MADE 
    FROM OLA_RidesDATA
    WHERE Payment_Method != 'Not Applicable' 
    GROUP BY Payment_Method;
    """
    cursor.execute(query_rev)
    data_result20 = cursor.fetchall()
    column_data20 = [desc[0] for desc in cursor.description]
    table20 = pd.DataFrame(data_result20, columns=column_data20)
    fig, ax = plt.subplots()
    ax.bar(table20['Payment_Method'], table20['REVENUE_MADE'])
    ticks = np.arange(0, 30000000, 5000000)
    labels = [f'{i//1000000}M' for i in ticks]
    ax.set_yticks(ticks, labels)
    for xy in zip(table20['Payment_Method'], table20['REVENUE_MADE']):
        ax.annotate(f'{round(xy[1]/1000000, 2)}M', xy=xy, xytext=(0, 5), textcoords="offset points")
    ax.set_xlabel('\nPayment Methods')
    ax.set_ylabel('Revenue Made(in millions)\n')
    st.pyplot(fig)

def Incomplete_Rides():
    query_totalincomp = """
    SELECT COUNT(*)
    FROM OLA_RidesDATA
    WHERE Incomplete_Rides = 'Yes';
    """
    cursor.execute(query_totalincomp)
    data_result21 = cursor.fetchall()
    st.title("Incomplete Rides")
    st.write('\n')
    st.metric("Total Incomplete Rides", value=data_result21[0][0])
    st.write("So we have total of '3926' incomplete rides. Lets see the reasons behind this to understand more about this.")
    st.subheader("Incomplete Ride Reasons")
    
    query_reasonincomp = """
    SELECT Incomplete_Rides_Reason, COUNT(*) AS COUNT
    FROM OLA_RidesDATA
    WHERE Incomplete_Rides = 'Yes'
    GROUP BY Incomplete_Rides_Reason;
    """
    cursor.execute(query_reasonincomp)
    data_result22 = cursor.fetchall()
    column_data22 = [desc[0] for desc in cursor.description]
    table22 = pd.DataFrame(data_result22, columns=column_data22)
    st.table(table22)
    st.write('\n')
    st.write("These are the incomplete ride reasons along with their count(means how many times ride was incomplete because of that reason). In this we have to focus more on 'Vehicle Breakdown' because it is related to the service. So we have to make sure necessary back up is in place or we should come up with any other solution to complete the journey of the customer, as these kind of reasons will impact the service and business.")
    st.write("Lets see the count of incomplete rides for each vehicle type")
    st.subheader("Incomplete rides for each vehicle type")

    query_vehincomp = """ 
    SELECT Vehicle_Type, COUNT(*) AS Incomplete_Ride_Count
    FROM OLA_RidesDATA
    WHERE Incomplete_Rides = 'Yes'
    GROUP BY Vehicle_Type
    ORDER BY Incomplete_Ride_Count DESC;
    """
    cursor.execute(query_vehincomp)
    data_result23 = cursor.fetchall()
    column_data23 = [desc[0] for desc in cursor.description]
    table23 = pd.DataFrame(data_result23, columns=column_data23)
    st.table(table23)
    st.write("According to this 'Prime Sedan' have more number of incomplete rides")
    st.subheader("Incomplete ride reason count for each vehicle type")
    st.write("For better understanding the count according to the reasons, lets see the incomplete ride count for each vehicle type due to particular reason ")

    def vehicle_reason(reason):
        query_vehreaincomp = f""" 
        SELECT Vehicle_Type, COUNT(*) AS Incomplete_Ride_Count
        FROM OLA_RidesDATA
        WHERE Incomplete_Rides = 'Yes'AND Incomplete_Rides_Reason = '{reason}'
        GROUP BY Vehicle_Type
        ORDER BY Incomplete_Ride_Count DESC;
        """
        cursor.execute(query_vehreaincomp)
        data_result24 = cursor.fetchall()
        column_data24 = [desc[0] for desc in cursor.description]
        table24 = pd.DataFrame(data_result24, columns=column_data24)
        st.table(table24)
    
    selection = st.selectbox('Choose a reason', ['Choose', 'Customer Demand', 'Vehicle Breakdown', 'Other Issue'])
    if selection:
        if selection != 'Choose':
            vehicle_reason(selection)


def Revenue_Made():
    query_rcomp = """ 
    SELECT SUM(Booking_Value) AS Total_Booking_Value
    FROM OLA_RidesDATA
    WHERE Incomplete_Rides = 'No';
    """
    cursor.execute(query_rcomp)
    data_result25 = cursor.fetchall()

    query_rincomp = """ 
    SELECT SUM(Booking_Value) AS Total_Booking_Value
    FROM OLA_RidesDATA
    WHERE Incomplete_Rides = 'Yes';
    """
    cursor.execute(query_rincomp)
    data_result26 = cursor.fetchall()

    st.title("Revenue")
    col1, col2 = st.columns(2, gap = 'small')
    col1.subheader("Total booking value of rides completed successfully")
    col1.metric("Value(in millions)", value=f'{round(data_result25[0][0]/1000000, 2)}M')
    col2.subheader("Total booking value of rides incompleted")
    col2.metric("Value(in millions)", value=f'{round(data_result26[0][0]/1000000, 2)}M')
    st.write('\n')
    st.write("Lets see the total booking value for canceled rides")
    query_rcancel = """ 
    SELECT SUM(Booking_Value) AS Total_Booking_Value
    FROM OLA_RidesDATA
    WHERE Booking_Status != 'Success';
    """
    cursor.execute(query_rcancel)
    data_result27 = cursor.fetchall()
    st.subheader("Total booking value of canceled rides")
    st.metric("Value(in millions)", value=f'{round(data_result27[0][0]/1000000, 2)}M')
    st.write("Lets segregate this and see the total booking value for each type of cancelation")

    query_drivcancel = """ 
    SELECT SUM(Booking_Value) AS Total_Booking_Value
    FROM OLA_RidesDATA
    WHERE Booking_Status = 'Canceled by Driver';
    """
    cursor.execute(query_drivcancel)
    data_result28 = cursor.fetchall()

    query_custcancel = """ 
    SELECT SUM(Booking_Value) AS Total_Booking_Value
    FROM OLA_RidesDATA
    WHERE Booking_Status = 'Canceled by Customer';
    """
    cursor.execute(query_custcancel)
    data_result29 = cursor.fetchall()

    query_drinotfound = """ 
    SELECT SUM(Booking_Value) AS Total_Booking_Value
    FROM OLA_RidesDATA
    WHERE Booking_Status = 'Driver Not Found';
    """
    cursor.execute(query_drinotfound)
    data_result30 = cursor.fetchall()

    col1, col2, col3 = st.columns(3, gap = 'small')
    col1.subheader("Canceled by driver")
    col1.metric("Total Booking Value(in millions)", value=f'{round(data_result28[0][0]/1000000, 2)}M')

    col2.subheader("Canceled by customer")
    col2.metric("Total Booking Value(in millions)", value=f'{round(data_result29[0][0]/1000000, 2)}M')

    col3.subheader("Driver Not Found")
    col3.metric("Total Booking Value(in millions)", value=f'{round(data_result30[0][0]/1000000, 2)}M')



home = st.Page(home_page, title="Home", default = True)
bookings = st.Page(successful_bookings, title="Successful Bookings")
vehicle = st.Page(Vehicle_Types, title="Vehicle Types")
c_canceled = st.Page(Customer_Canceled, title="Cancelled Rides by Customers")
d_canceled = st.Page(Driver_Canceled, title="Canceled Rides by Drivers")
customers = st.Page(Top_Customers, title="Frequent Customers")
d_ratings = st.Page(Driver_Ratings, title="Driver Ratings")
c_ratings = st.Page(Customer_Ratings, title="Customer Ratings")
payments = st.Page(Payment_Methods, title="Payment Methods")
incomplete = st.Page(Incomplete_Rides, title="Incomplete Rides")
revenue = st.Page(Revenue_Made, title="Revenue")

pg = st.navigation([home, bookings, vehicle, c_canceled, d_canceled, incomplete, customers, d_ratings, c_ratings, payments, revenue])
pg.run()

