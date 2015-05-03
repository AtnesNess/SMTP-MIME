import argparse
import imghdr
import os
import base64
import datetime
import socket


def main(args):
    charset = "UTF-8"
    template = """Content-Type: multipart/mixed; boundary="652b8c4dcb00cdcdda1e16af36781caf"

--652b8c4dcb00cdcdda1e16af36781caf

"""
    multipart_mixed = """
--652b8c4dcb00cdcdda1e16af36781caf
Content-Type: multipart; name="{}"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="{}"
"""
    directory = os.getcwd()
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and imghdr.what(os.path.join(directory, f))]
    name, recv_name, subject = ("me", "to", "test")
    from_email = "from@from.ru"
    to_emails = args.emails
    name = base64.standard_b64encode(name)
    recv_name = base64.standard_b64encode(recv_name)
    subject = subject
    message = template.format(from_email,  ">, <".join(to_emails), subject, datetime.date.today())
    print(message)
    message += "attachments: \n"

    for file in files:
        message += file+"\n"
    for file in files:

        message += multipart_mixed.format(file, file)+"\n\n"
        f_data = open(os.path.join(directory, file), 'r').read()
        f64 = base64.standard_b64encode(f_data)
        message += f64+"\n\n"
    message += "--652b8c4dcb00cdcdda1e16af36781caf--"
    # eml = open("result.eml", "w+")
    # eml.write(message)
    # eml.close()
    if args.server is None:
        addr = str(socket.gethostbyname("mxs.mail.ru"))
    else:
        addr = args.server
    print(addr)
    sock = socket.socket()
    sock.connect((addr, 25))
    print sock.recv(512)
    HELLO = "EHLO atnes\r\n"
    print HELLO
    sock.send(HELLO)
    print(sock.recv(1024))
    MAILFROM = "MAIL FROM: {}\r\n".format(from_email)
    print(MAILFROM)
    sock.send(MAILFROM)
    print(sock.recv(1024))
    for to_email in to_emails:
        RCPT = 'RCPT TO: {}\r\n'.format(to_email)
        print(RCPT)
        sock.send(RCPT)
    print(sock.recv(1024))
    print("DATA\r\n")
    sock.send("DATA\r\n")
    print(sock.recv(1024))
    # CHARSET = "charset={}\r\n".format(charset)
    # print(CHARSET)
    # sock.send(CHARSET)
    # SUBJECT = "SUBJECT: {}\r\n".format(subject)
    # print(SUBJECT)
    # sock.send(SUBJECT)
    FROM = "FROM: me <{}>\r\n".format(from_email)
    print(FROM)
    sock.send(FROM)
    TO = "TO: <{}>\r\n".format(">, <".join(to_emails))
    print(TO)
    sock.send(TO)
    DATE = "Date: {}\r\n".format(datetime.date.today())
    print(DATE)
    sock.send(DATE)
    MIME = "MIME-Version: 1.0\r\n"
    print(MIME)
    sock.send(MIME)

    # sock.send("\r\n")
    # sock.send("\r\n")

    MESSAGE = "{}\r\n".format(message)
    sock.send(MESSAGE)
    sock.send(".\r\n")
    code = sock.recv(1024)
    print(code)
    if code[0:3] == "250":
        print "the letter successfully sent"
    print("quit\r\n")
    sock.send("quit\r\n")


    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("mail pic sender ")
    parser.add_argument("emails", nargs="+", help="receivers")
    parser.add_argument("-s", "--server", help="smtp server on 25 port")
    args = parser.parse_args()
    main(args)