from django import template

register = template.Library()


@register.filter()
def hide_email(mail):
    mail_list = mail.split('@')
    domain_name = ''.join(mail_list[0:-1])
    if len(domain_name) <= 4:
        return '*' * len(domain_name) + mail_list[-1]
    hidden_mail = domain_name[:4] + ('*' * (len(domain_name) - 4)) + '@' + mail_list[-1]
    return hidden_mail
