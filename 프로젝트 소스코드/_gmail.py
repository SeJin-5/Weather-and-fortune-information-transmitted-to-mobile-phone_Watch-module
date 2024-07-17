import imaplib
import email

def get_senderinfo_from_gmail() :
    mail = imaplib.IMAP4_SSL('imap.gmail.com','993')
    mail.login('your gmail id','your gmail password')
    mail.select('inbox')
    unread_count = len(mail.search(None, 'UnSeen')[1][0].split()) # number of unread mail  

    rv, data = mail.search(None, 'UnSeen')

    correct_string = [] # for correct sender string
    unread_senders = [] # sender numbers

    for num in data[0].split():
        rv, data = mail.fetch(num, '(RFC822)')

        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['From']))
        from_sender = str(hdr)

        if not from_sender:
                pass
        else:
            correct_string = from_sender.split('@')[0]  
            correct_string = correct_string.split('<')[1] 
            unread_senders.append(correct_string)

    mail.logout()

    sender_info = {'count':str(unread_count), 'senders':unread_senders}
    
    return sender_info
