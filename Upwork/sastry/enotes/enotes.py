from twocaptcha import TwoCaptcha

solver = TwoCaptcha('2c10c1c2ead9e59812117b229ac303eb')

# config = {
#             'server':           '2captcha.com',
#             'apiKey':           'YOUR_API_KEY',
#             'softId':            123,
#             'callback':         'https://your.site/result-receiver',
#             'defaultTimeout':    120,
#             'recaptchaTimeout':  600,
#             'pollingInterval':   10,
#         }
# solver = TwoCaptcha(**config)

result = solver.recaptcha(sitekey='6LeCYNwSAAAAAH0m1mTC_8sEJN2iNPNg8nPd9DER',
                            url='https://www.enotes.com/signin',
                            )


print(result)