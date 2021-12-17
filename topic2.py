from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('TkAgg')
#from tkinter import *

menu = ['Giới thiệu chung','Dữ liệu','Đề xuất chung','Giải pháp cho từng khách hàng']
choice = st.sidebar.selectbox('Menu',menu)
if choice == 'Giới thiệu chung':
    #dispaly image
    from PIL import Image
    image1 = Image.open('customersegment.jpg')
    st.image(image1)
    #display text
    st.title('CHƯƠNG TRÌNH KHOA HỌC DỮ LIỆU')
    st.header('CUSTOMER SEGMENTATION PROJECT')
    st.header('Giới thiệu về dự án')
    st.write('''
    Công ty X chủ yếu bán các sản phẩm là quà tặng dành cho những dịp đặc biệt. Nhiều khách hàng của công ty là khách hàng bán buôn.
    Công ty X mong muốn có thể bán được nhiều sản phẩm hơn cũng như giới thiệu sản phẩm đến đúng đối tượng khách hàng, chăm sóc và làm hài lòng khách hàng.
    ''')
    st.write('''
    ##### Vấn đề kinh doanh: 
    1. Xây dựng model phân cụm khách hàng
    2. Đánh giá kết quả
    3. Đưa ra chiến dịch quảng cáo, bán hàng, chăm sóc khách hàng phù hợp cho mỗi nhóm
    ''')
elif choice == 'Dữ liệu':
    from PIL import Image
    image2 = Image.open('part2.jpg')
    st.image(image2)
    # Source Code
    df = pd.read_csv('OnlineRetail.csv',encoding="ISO-8859-1",dayfirst=True)
    # Xử lý dữ liệu
    df.dropna(subset=['CustomerID'],how='all',inplace=True)
    # Drop cancelled transactions
    df=df.drop(df[df['InvoiceNo'].astype(str).str.contains('C')].index)
    df.to_csv('cleandf.csv')
    # coutries 
    c=pd.DataFrame(df.groupby('Country')['CustomerID'].nunique())
    customercoutrywise=pd.DataFrame(c).sort_values(by='CustomerID', ascending=False)
    # Tính Total Price theo số lượng
    df['TotalRevenue'] = df['UnitPrice']*df['Quantity']
    # Phân tích hành vi tiêu dùng dựa trên quốc gia
    country_market = df.groupby('Country').agg({'TotalRevenue':['mean', 'count']})
    country_most_transaction = country_market['TotalRevenue']['count'].reset_index().sort_values('count', ascending=False)
    country_market_transaction = country_market['TotalRevenue']['mean'].reset_index().sort_values('mean', ascending=False)
    st.subheader('Phân tích và trực quan hóa dữ liệu')
    st.write('''##### Show vài dòng dữ liệu:''')
    st.dataframe(df.head(3))
    st.write('''Thông tin dữ liệu :''')
    st.write('''InvoiceNo:	Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. 
    If this code starts with letter 'c', it indicates a cancellation.''')
    st.write('''StockCode: Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.''')
    st.write('''Description: Product (item) name. Nominal.''')
    st.write('''Quantity: The quantities of each product (item) per transaction. Numeric.''')
    st.write('''InvoiceDate: Invice Date and time. Numeric, the day and time when each transaction was generated.''')
    st.write('''UnitPrice: Unit price. Numeric, Product price per unit in sterling.''')
    st.write('''CustomerID: Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.''')
    st.write('''Country: Country name. Nominal, the name of the country where each customer resides.''')
    st.write('''
    ##### Trực quan hóa dữ liệu''')
    #biểu đồ 1
    st.write('Thống kê số lượng đơn hàng theo quốc gia')
    image3 = Image.open('transaction_country.jpg')
    st.image(image3)
    st.write(''' Nhận xét: UK là nước có số lượng đơn hàng online nhiều nhất.''')
    #biểu đồ 2
    st.write('''#### Giá trị giao dịch trung bình theo quốc gia''')
    image4 = Image.open('mean_transaction_country.jpg')
    st.image(image4)
    #biểu đồ 3
    st.write('''Nhận xét: 3 quốc gia có giá trị đơn hàng trung bình cao nhất là Netherlands, Australia và Japan.''')
    st.write('''#### Lượng hóa đơn hàng tháng''')
    #convert object to datetime
    import datetime as dt
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    #Lập cột month, year
    df['Year'] = pd.DatetimeIndex(df['InvoiceDate']).year
    df['Month'] = pd.DatetimeIndex(df['InvoiceDate']).month
    fig3= plt.figure(figsize=(10,5))
    df.groupby(['Year', 'Month']).InvoiceNo.count().plot(kind='bar', title='Amount of invoices per month')
    st.pyplot(fig3)
    st.write('''Nhận xét: Năm 2010, lượng hóa đơn phát sinh hàng tháng khá thấp. Lượng hóa đơn tăng cao từ tháng 12/2010 và đạt cao nhất là tháng 11/2011. Tuy nhiên, đến tháng 12/2011 lại giảm xuống thấp.''')
    st.write('''#### Lượng khách hàng hàng tháng''')
    fig4=plt.figure(figsize=(10,5))
    df.groupby(['Year', 'Month']).CustomerID.count().plot(kind='bar', title='Amount of customers per month')
    st.pyplot(fig4)
    st.write('''Nhận xét: khách hàng mua sắm nhiều nhất vào tháng 9, 10, 11 năm 2011''')
    st.write('''#### Lượng bán các ngày trong tuần''')
    # Ngày nào bán được nhiều nhất trong tuần? Giờ nào là giờ tốt nhất để bán?
    # HOUR
    df['Hour'] = df['InvoiceDate'].dt.hour
    # WEEKDAY. dt.weekday. The day of the week with Monday=0, Sunday=6.
    #This method is available on both Series with datetime values or DatetimeIndex.
    df['WeekDay']=df['InvoiceDate'].dt.weekday
    df['WeekDay'] = df['WeekDay'].replace({0:'Mon', 1:'Thu',2:'Wed', 3:'Thur', 4:'Fri', 5:'Sat', 6:'Sun'})
    fig5= plt.figure(figsize=(10,5))
    df.groupby('WeekDay').TotalRevenue.sum().plot(kind='bar', title='Best Day Of the Week To Sell')
    st.pyplot(fig5)
    st.write('''Nhận xét: Ngày bán được nhiều nhất trong tuần là thứ 5 và thứ 6. ''')
    st.write('''#### Lượng bán trung bình theo giờ''')
    fig6=plt.figure(figsize=(10,5))
    df.groupby('Hour').TotalRevenue.sum().plot(kind='bar', title='Best Hour To Sell')
    st.pyplot(fig6)
    st.write('''Nhận xét: Giờ bán được nhiều nhất trong ngày là 12h''')
elif choice == 'Đề xuất chung':
    from PIL import Image
    image10 = Image.open('part3.jpg')
    st.image(image10)
    st.subheader('Mô hình phân nhóm khách hàng')
    #BUILD MODEL
    ##4.1 RFM ((Recency, Frequency, MonetaryValue)
    # Define function to parse date
    def get_day(x) : return dt.datetime(x.year, x.month, x.day)
    df=pd.read_csv('cleandf.csv')
    # Tính Total Price theo số lượng
    df['TotalRevenue'] = df['UnitPrice']*df['Quantity']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['day'] = df['InvoiceDate'].apply(get_day)
    max_date = df["day"].max().date()

    Recency = lambda x: (max_date - x.max().date()).days
    Frequency = lambda x: len(x.unique())
    Monetary = lambda x: round(sum(x),2)

    df_RFM = df.groupby("CustomerID").agg({"day":Recency,
                                        "InvoiceNo": Frequency,
                                        "TotalRevenue": Monetary})

    # Đổi tên cột
    df_RFM.columns = ["Recency","Frequency","Monetary"]
    #Sắp xếp dữ liệu
    df_RFM = df_RFM.sort_values("Monetary",ascending=False)
    # reference date is one day after transaction day so that the minimum recency is 1
    df_RFM['Recency'] = df_RFM["Recency"] + 1
    df_RFM.loc[df_RFM['Monetary']==0, 'Monetary'] = 0.0001

    # Xử lý triệt để outlier
    df_RFM = df_RFM[(df_RFM.Recency<=500)&(df_RFM.Frequency<=30)&(df_RFM.Monetary<=15000)]

    #Calculate RFM quartiles
    #Create labels
    r_labels = range(4,0,-1)
    f_labels = range(1,5)
    m_labels = range(1,5)

    # Assign these labels to 4 equal percentile groups
    r_group = pd.qcut(df_RFM["Recency"].rank(method="first"),q=4, labels=r_labels)
    f_group = pd.qcut(df_RFM["Frequency"].rank(method="first"),q=4, labels=f_labels)
    m_group = pd.qcut(df_RFM["Monetary"].rank(method="first"),q=4, labels=m_labels)
    # Create new columns R, F, M
    df_RFM = df_RFM.assign(R=r_group.values, F=f_group.values, M= m_group.values)
    df_RFM.head()
    #Create RFM Segments
    df_RFM["Segment"] = df_RFM[["R","F","M"]].astype("str").agg("".join,axis=1)
    def rfm_level(df):
        if (df['R'] == 4 and df['F'] ==4 and df['M'] == 4)  :
            return 'STARS'
        elif (df['R'] == 4 and df['F'] ==1 and df['M'] == 1):
            return 'NEW'
        else:     
            if df['R'] == 1:
                return 'LOST' 
            return 'REGULARS'
    #Calculate RFM Level
    df_RFM["RFM_Level"] = df_RFM.apply(rfm_level,axis=1)
    columns = ["Recency", "Frequency", "Monetary", "R", "F", "M", "Segment", "RFM_Level"]
    df_RFM = df_RFM.reindex(columns=columns)
    rfmdf = df_RFM[["Recency", "Frequency", "Monetary", "RFM_Level"]]
    rfmdf.to_csv('rfmdf.csv')
    #import json
    #with open('rfm.json', 'w+') as file:
        #json.dump(rfmdf, file)
    from PIL import Image
    image11 = Image.open('FRM.jpg')
    st.image(image11)
    st.header('Nhận xét chung:')
    st.write('''
    Với dữ liệu cho sẵn, thông qua 3 mô hình đều cho thấy có thể chia khách hàng của doanh nghiệp thành 4 nhóm. Trong đó:
- Nhóm khách hàng thông thường đang chiếm tỷ trọng cao. 
- Vấn đề cần quan tâm là số lượng khách hàng rời bỏ là khá lớn, khoảng hơn 20%. - Nhóm khách hàng mới có phát sinh nhưng nhóm này số lượng còn khá khiêm tốn dù có tần suất giao dịch nhiều và giá trị đơn hàng cao. 
- Nhóm khách hàng trung thành vẫn còn chiếm tỷ trong khiêm tốn.
    ''')
    st.header('Đề xuất')
    st.write('''
    - Tiếp tục thu hút thêm khách hàng mới, tập trung bán vào những khung giờ cao điểm mua sắm như vào 12h trưa thứ 5 và thứ 6 hàng tuần. 
- Nước Anh đang là quốc gia tập trung nhiều khách hàng nhất nên cần chú trọng đến các chương trình quảng cáo, chiến dịch marketing cho khách hàng ở Anh. 
- Đẩy mạnh quảng cáo các sản phẩm được nhiều người quan tâm ưa chuộng theo Top 10 sản phẩm được mua sắm nhiều nhất của công ty. 
- Nghiên cứu triển khai những quốc gia có nhiều tiềm năng, đẩy mạnh truyền thông ở các quốc gia có số lượng Kh mua sắm nhiều, giá trị đơn hàng cao. 
- Ngoài ra nên xem xét có những đợt khuyến mãi, tặng quà để tiếp tục giữ chân khách hàng và thu hút lại nhóm khách hàng đã rời bỏ. 
    ''')
elif choice == 'Giải pháp cho từng khách hàng':
    from PIL import Image
    image11 = Image.open('tangdoanhthu.jpg')
    st.image(image11)
    #import json
    #with open('rfm.json') as json_file:
        #rfm1 = pd.read_json(json_file, orient='index')
    st.subheader('GIỚI THIỆU CẤU TRÚC TẬP DỮ LIỆU')
    rfm1 = pd.read_csv('rfmdf.csv')
    rfm1['CustomerID'] = rfm1['CustomerID'].astype(str)
    rfm1['CustomerID'] =  rfm1['CustomerID'].map(lambda x: x.rstrip('.0'))
    st.dataframe(rfm1.head(3))
    st.write('''Trong đó:''')
    st.write('Recency (R): Thời gian giao dịch cuối cùng.')
    st.write('Frequency (F): Tổng số lần giao dịch chi tiêu.')
    st.write('Monetary value (M): Tổng só tiền giao dịch chi tiêu.')
    st.write('RFM_Level: Nhóm khách hàng')
    st.subheader('XÁC ĐỊNH KHÁCH HÀNG THUỘC NHÓM VÀ GIẢI PHÁP TƯƠNG ỨNG')
    st.write('#### Nhập thông tin khách hàng cần tìm (CustomerID): ')
    #rfm1['CustomerID']=pd.to_numeric(rfm1['CustomerID'])
    input= st.text_input('CustomerID')
    submit= st.button('Submit')
    if submit:
        if input in rfm1['CustomerID'].values:
            st.subheader('Thông tin của khách hàng như sau:')
            #rfm1['CustomerID'] = rfm1['CustomerID'].astype(int)
            #input=pd.to_numeric(input)
            result=rfm1[rfm1['CustomerID'] == input]
            result=DataFrame(result)
            st.dataframe(result)
            if result['RFM_Level'].values == "STARS":
            #if result['RFM_Level'].str.contains('STARS'):
                st.subheader('Đề xuất liên quan đến khách hàng')
                st.write('''
                Đây là khách hàng thuộc nhóm STAR - tức có thời gian mua sắm gần đây, mua sắm liên tục và giá trị mua sắm cao.
                Đối với khách hàng này, cần có nhiều gợi ý sản phẩm, chương trình tặng quà khách hàng thân thiết, gia tăng hứng thú mua sắm
                cũng như làm khách hàng trung thành hơn với công ty.
                ''')
            elif result['RFM_Level'].values == "LOST":
                st.subheader('Đề xuất liên quan đến khách hàng')
                st.write('''
                Đây là khách hàng thuộc nhóm LOST - tức đã rời bỏ công ty.
                Công ty cần thực hiện marketing trực tiếp, đưa ra đơn hàng 0 đồng để khuyến khích khách hàng quay trở lại. 
                ''')
            elif result['RFM_Level'].values == "NEW":
                st.subheader('Đề xuất liên quan đến khách hàng')
                st.write('''
                Đây là khách hàng thuộc nhóm NEW - tức đã mới tham gia mua sắm hàng của công ty.
                Công ty cần thực hiện marketing trực tiếp, đưa ra đề xuất mua hàng phù hợp với nhu cầu. 
                Tặng voucher giảm giá, mua 1 tặng 1 cũng như có những chương trình kích thích mua sắm như 
                tích lũy nâng hạng, tặng quà...để biến khách hàng thành khách hàng thường xuyên.
                ''')
            else:
                st.subheader('Đề xuất liên quan đến khách hàng')
                st.write('''
                Đây là khách hàng thuộc nhóm REGULAR - thuộc nhóm khách hàng thông thường.
                Công ty cần thực hiện marketing trực tiếp, đưa ra đề xuất mua hàng phù hợp với nhu cầu. 
                Tặng voucher giảm giá, mua 1 tặng 1 cũng như có những chương trình kích thích mua sắm như 
                tích lũy nâng hạng, tặng quà...để khuyến khích khách hàng thành nhóm STARS."
                ''')
        else:
            st.subheader('ID của khách hàng không tồn tại!')

            