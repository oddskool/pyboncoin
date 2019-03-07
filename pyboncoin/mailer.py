import smtplib


def send_mail(query, new_offers, config):
    if not len(new_offers):
        return
    session = smtplib.SMTP_SSL(config['smtp_server'], int(config['smtp_port']))
    session.login(config['smtp_login'], config['smtp_pwd'])
    headers = ["from: " + config['from'],
               "subject: " + '[BonCoin] %d nouvelles offres ! (%s)' % (len(new_offers), query),
               "to: " + config['recipients'],
               "mime-version: 1.0",
               "encoding: utf-8",
               "content-type: text/html"]
    headers = "\r\n".join(headers)
    body = "<html><head><title>%d Nouvelles offres !</title></head><body><ul>" % len(new_offers)
    for offer in new_offers:
        body += "<li>%s</li>" % offer.html()
    body += "</ul></body></html>"
    transmission = headers + "\r\n\r\n" + body
    open('last_mail.txt', 'w').write(transmission)
    result = session.sendmail(
        config['smtp_login'], config['recipients'].split(','), transmission.encode('utf-8')
    )
    print('mail sent', result)
