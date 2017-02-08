@@ -0, 0 + 1, 254 @@
#!/usr/bin/env python
# coding:utf-8
import MySQLdb
import datetime
import xlwt
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from email.utils import COMMASPACE, formatdate
from email import encoders

import os


def send_mail(server, fro, to, subject, text, files=[]):
    assert type(server) == dict
    assert type(to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = fro
    if not isinstance(subject, unicode):
        subject = unicode(subject)
    # if not isinstance(text,unicode):
    #   subject = unicode(text)
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to)  # COMMASPACE==', '
    msg['Date'] = formatdate(localtime=True)
    # msg.attach(MIMEText(text))

    for f in files:
        # 'octet-stream': binary data
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(f, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    import smtplib
    smtp = smtplib.SMTP(server['name'], server['port'])
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(server['user'], server['passwd'])
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()


def kmg_convert(s):
    k = s / 1000.0
    m = s / 1000000.0
    g = s / 10000000000.0
    if k < 1:
        s = str('%.3f' % k) + 'K'
    else:
        if m < 1:
            s = str('%.3f' % m) + 'M'
        else:
            s = str('%.3f' % g) + 'G'


def get_mysql_data(sql):
    cur.execute(sql)
    results = cur.fetchall()
    return results


def cover_excel(msg, row, count):
    print "this is cover_excel function"
    print "new msg value"
    print msg
    x = msg
    if count == 1:
        for j in range(0, 12):
            value = x[0]
            if isinstance(value[j], long) or isinstance(value[j], int) or isinstance(value[j], float):
                ws.write(row, j, value[j])
            else:
                ws.write(row, j, value[j].decode('utf8'))
    else:
        for i in (row, row + count - 1):
            # print "i value"
            # print i
            # print "row+count-1"
            # print row+count-1
            for j in range(0, 12):
                value = x[i - 2]
             #   print "value"
             #   print value
                if isinstance(value[j], long) or isinstance(value[j], int) or isinstance(value[j], float):
                    ws.write(i, j, value[j])
                else:
                    ws.write(i, j, value[j].decode('utf8'))
    # print "wb save test"
    # wb.save('/tmp/zabbix_log/chance_zabbix_monitor_test.xls')


def run_print(start_date, end_date):
    # print "run_print"
    date_list = []
    while start_date <= end_date:
        date_str = start_date.strftime("%Y-%m-%d %H")
        date_list.append(date_str)
        start_date += datetime.timedelta(hours=1)
    # print date_list

# def run_select(start_time,end_time):


def run_select(start_date, end_date, row):
    # print "start_date value %s"%start_date
    # print "end_date value %s"%end_date
    start_time = (start_date - datetime.timedelta(hours=1)
                  ).strftime("%Y-%m-%d %H")
    # print "start_time value %s"%start_time
    date_list = []
    while start_date <= end_date:
        date_str = start_date.strftime("%Y-%m-%d %H")
        date_list.append(date_str)
        start_date += datetime.timedelta(hours=1)
    # print date_list
    # for t in (start_time,end_time):
    for t in date_list:
        #    print "t value %s"%t
        get_bgp_route_sql = "select from_unixtime(hi.clock,'%%Y-%%m-%%d %%H:%%i') as Date,g.name as vBras_Name,hi.value as Bgp_Route from hosts_groups hg join groups g on g.groupid = hg.groupid join items i on hg.hostid = i.hostid join hosts h on h.hostid=i.hostid join history_uint hi on  i.itemid = hi.itemid  where  i.key_='vbras.bgp_route' and hi.clock >= UNIX_TIMESTAMP('%s:00:00') and hi.clock < UNIX_TIMESTAMP('%s:01:00')  and g.name like '%%vbras server%%';" % (t, t)
        bgp_route_result = get_mysql_data(get_bgp_route_sql)
        # print "bgp_route_result"
        # print bgp_route_result

        get_bgp_route_peak_sql = "select from_unixtime(hi.clock,'%%Y-%%m-%%d %%T') as Date,g.name as vBras_Name,hi.value_max as Bgp_Route_Peak from hosts_groups hg join groups g on g.groupid = hg.groupid join items i on hg.hostid = i.hostid join hosts h on h.hostid=i.hostid join trends_uint hi on  i.itemid = hi.itemid  where  i.key_='vbras.bgp_route' and  hi.clock >= UNIX_TIMESTAMP('%s:00:00') and hi.clock <= UNIX_TIMESTAMP('%s:00:00') and g.name like '%%vbras server%%';" % (start_time, t)
        bgp_route_peak_result = get_mysql_data(get_bgp_route_peak_sql)
        # print "bgp_route_peak_result"
        # print bgp_route_peak_result

        get_nat_user_peak_sql = "select from_unixtime(hi.clock,'%%Y-%%m-%%d %%T') as Date,g.name as vBras_Name,hi.value_max as Nat_User_Peak from hosts_groups hg join groups g on g.groupid = hg.groupid join items i on hg.hostid = i.hostid join hosts h on h.hostid=i.hostid join trends_uint hi on  i.itemid = hi.itemid  where  i.key_='vbras.nat_totaluser' and hi.clock >= UNIX_TIMESTAMP('%s:00:00') and hi.clock <= UNIX_TIMESTAMP('%s:00:00')  and g.name like '%%vbras server%%';" % (start_time, t)
        nat_user_peak_result = get_mysql_data(get_nat_user_peak_sql)
        # print "nat_user_peak_result"
        # print nat_user_peak_result

        get_nat_user_sql = "select from_unixtime(hi.clock,'%%Y-%%m-%%d %%T') as Date,g.name as vBras_Name,hi.value as Nat_User from hosts_groups hg join groups g on g.groupid = hg.groupid join items i on hg.hostid = i.hostid join hosts h on h.hostid=i.hostid join history_uint hi on  i.itemid = hi.itemid  where  i.key_='vbras.nat_totaluser' and hi.clock >= UNIX_TIMESTAMP('%s:00:00') and hi.clock < UNIX_TIMESTAMP('%s:01:00')  and g.name like '%%vbras server%%';" % (t, t)
        nat_user_result = get_mysql_data(get_nat_user_sql)
        # print "nat_user_result"
        # print nat_user_result

        get_nat_session_sql = "select from_unixtime(hi.clock,'%%Y-%%m-%%d %%T') as Date,g.name as vBras_Name,hi.value as Nat_Session from hosts_groups hg join groups g on g.groupid = hg.groupid join items i on hg.hostid = i.hostid join hosts h on h.hostid=i.hostid join history_uint hi on  i.itemid = hi.itemid  where  i.key_='vbras.nat_totalsess' and hi.clock >= UNIX_TIMESTAMP('%s:00:00') and hi.clock < UNIX_TIMESTAMP('%s:01:00')  and g.name like '%%vbras server%%';" % (t, t)
        nat_session_result = get_mysql_data(get_nat_session_sql)
        # print "nat_session_result"
        # print nat_session_result

        get_nat_session_peak_sql = "select from_unixtime(hi.clock,'%%Y-%%m-%%d %%T') as Date,g.name as vBras_Name,hi.value_max as Nat_Session_Peak from hosts_groups hg join groups g on g.groupid = hg.groupid join items i on hg.hostid = i.hostid join hosts h on h.hostid=i.hostid join trends_uint hi on  i.itemid = hi.itemid  where  i.key_='vbras.nat_totalsess' and  hi.clock >= UNIX_TIMESTAMP('%s:00:00') and hi.clock <= UNIX_TIMESTAMP('%s:00:00')  and g.name like '%%vbras server%%';" % (start_time, t)
        nat_session_peak_result = get_mysql_data(get_nat_session_peak_sql)
        # print "nat_session_peak_result"
        # print nat_session_peak_result

        get_netcard_in_sql = "select from_unixtime(hi.clock,'%%Y-%%m-%%d %%T') as Date,g.name as vBras_Name,hi.value as Netcard_In from hosts_groups hg join groups g on g.groupid = hg.groupid join items i on hg.hostid = i.hostid join hosts h on h.hostid=i.hostid join history_uint hi on  i.itemid = hi.itemid  where  i.key_='net.if.in[eth1]' and hi.clock >= UNIX_TIMESTAMP('%s:00:00') and hi.clock < UNIX_TIMESTAMP('%s:01:00')  and g.name like '%%vbras server%%' group by h.host ;" % (
            t, t)
        netcard_in_result = get_mysql_data(get_netcard_in_sql)
        # print "netcard_in_result"
        # print netcard_in_result

        get_netcard_in_peak_sql = "select from_unixtime(hi.clock,'%%Y-%%m-%%d %%T') as Date,g.name as vBras_Name,hi.value_max as Netcard_In_Peak from hosts_groups hg join groups g on g.groupid = hg.groupid join items i on hg.hostid = i.hostid join hosts h on h.hostid=i.hostid join trends_uint hi on  i.itemid = hi.itemid  where  i.key_='net.if.in[eth1]' and hi.clock >= UNIX_TIMESTAMP('%s:00:00') and  hi.clock <= UNIX_TIMESTAMP('%s:00:00') and g.name like '%%vbras server%%';" % (
            start_time, t)
        netcard_in_peak_result = get_mysql_data(get_netcard_in_peak_sql)
        # print "netcard_in_peak_result"
        # print netcard_in_peak_result

        get_netcard_out_sql = "select from_unixtime(hi.clock,'%%Y-%%m-%%d %%T') as Date,g.name as vBras_Name,hi.value as Netcard_Out from hosts_groups hg join groups g on g.groupid = hg.groupid join items i on hg.hostid = i.hostid join hosts h on h.hostid=i.hostid join history_uint hi on  i.itemid = hi.itemid  where  i.key_='net.if.out[eth1]' and hi.clock >= UNIX_TIMESTAMP('%s:00:00') and hi.clock < UNIX_TIMESTAMP('%s:01:00')  and g.name like '%%vbras server%%' group by h.host;" % (
            t, t)
        netcard_out_result = get_mysql_data(get_netcard_out_sql)
        # print "netcard_out_result"
        # print netcard_out_result

        get_netcard_out_peak_sql = "select from_unixtime(hi.clock,'%%Y-%%m-%%d %%T') as Date,g.name as vBras_Name,hi.value_max as Netcard_Out_Peak from hosts_groups hg join groups g on g.groupid = hg.groupid join items i on hg.hostid = i.hostid join hosts h on h.hostid=i.hostid join trends_uint hi on  i.itemid = hi.itemid  where  i.key_='net.if.out[eth1]' and  hi.clock >= UNIX_TIMESTAMP('%s:00:00') and  hi.clock <= UNIX_TIMESTAMP('%s:00:00')  and g.name like '%%vbras server%%';" % (
            start_time, t)
        netcard_out_peak_result = get_mysql_data(get_netcard_out_peak_sql)
        # print "netcard_out_peak_result"
        # print netcard_out_peak_result

        msg = [list(i) for i in bgp_route_result]
        # print "this is run select"
        # print "msg value"
        # print msg
        for i in msg:
            for a in bgp_route_peak_result:
                if i[1] == a[1]:
                    i[2] = int(i[2])
                    i.append(int(a[2]))
            for b in netcard_in_result:
                if i[1] == b[1]:
                    i.append(int(b[2]))
            for c in netcard_in_peak_result:
                if i[1] == c[1]:
                    i.append(int(c[2]))
            for d in netcard_out_result:
                if i[1] == d[1]:
                    i.append(int(d[2]))
            for e in netcard_out_peak_result:
                if i[1] == e[1]:
                    i.append(int(e[2]))
            for f in nat_user_result:
                if i[1] == f[1]:
                    i.append(int(f[2]))
            for g in nat_user_peak_result:
                if i[1] == g[1]:
                    i.append(int(g[2]))
            for h in nat_session_result:
                if i[1] == h[1]:
                    i.append(int(h[2]))
            for j in nat_session_peak_result:
                if i[1] == j[1]:
                    i.append(int(j[2]))
        count = len(msg)
        # print "count "
        # print count
        # print "msg new value"
        # print msg
        cover_excel(msg, row, count)
        row = row + count
        # print "row :%d"%row


def main():
    row = 2
    run_select(start_date, end_date, row)

if __name__ == "__main__":
    default_encoding = 'utf-8'
    if sys.getdefaultencoding() != default_encoding:
        reload(sys)
        sys.setdefaultencoding(default_encoding)
    # if os.path.exists("/tmp/zabbix_log/"):
    #   os.mkdir("/tmp/zabbix_log/")
    conn = MySQLdb.connect(host='172.16.128.245', user='root',
                           passwd='123456', port=3306, charset="utf8")
    cur = conn.cursor()
    conn.select_db('zabbix')
    sheetname = ['业务巡检项目'.encode('utf-8'), '系统巡检项目'.encode('utf-8'), ]
    # sheetname="sheet"
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheetname[0].decode('utf-8'), cell_overwrite_ok=True)
    ws2 = wb.add_sheet(sheetname[1].decode('utf-8'), cell_overwrite_ok=True)
    mark = ['✔'.encode('utf-8')]
    style = xlwt.easyxf(
        'font: bold True, height 300;'
        'pattern: pattern solid, fore_colour green;'
        'align: vertical center, horizontal center;')
    ws.write_merge(0, 0, 0, 11, sheetname[0].decode('utf-8'), style)
    title = ['时间'.encode('utf-8'), '网元'.encode('utf8'), 'Bgp路由数目'.encode('utf8'), 'Bgp路由峰值'.encode('utf8'), 'In流量(bps)'.encode('utf8'), 'In流量峰值(bps)'.encode('utf8'),
             'Out流量(bps)'.encode('utf8'), 'Out流量峰值(bps)'.encode('utf8'), 'Nat用户数'.encode('utf8'), 'Nat用户数峰值'.encode('utf8'), 'Nat Session'.encode('utf8'), 'Nat session峰值'.encode('utf8')]
    for j in range(0, 12):
        ws.write(1, j, title[j].decode('utf8'))
    ws2.write(0, 0, mark[0].decode('utf8'))
    start_date = datetime.datetime.now() - datetime.timedelta(hours=13)
    end_date = datetime.datetime.now() - datetime.timedelta(hours=13)
    main()
    # print "wb.save"
    # wb.save('/tmp/zabbix_log/chance_zabbix_monitor_hour_avg.xls')
    wb.save('/tmp/zabbix_log/vbras_monitor_hourly_report_test.xls')
    cur.close()
    conn.close()
    # follow is send mail
    server = {'name': 'smtp.163.com', 'user': 'yanghao19890203',
              'passwd': 'yxl19861207', 'port': 25}
    fro = 'yanghao19890203@163.com'
    to = ['yangh@certusnet.com.cn']
    subject = 'test梅州移动政务网专线业务vBRAS巡检报表[%s:00 to %s:00]' % (
        start_date.strftime("%Y-%m-%d %H"), end_date.strftime("%Y-%m-%d %H"))
    # print "subject"
    # print subject
    text = 'Dear,all:\n附件为梅州移动政务网专线业务vBRAS巡检报表,请查收.'
    files = ['/tmp/zabbix_log/vbras_monitor_hourly_report_test.xls']
    send_mail(server, fro, to, subject, text, files=files)
