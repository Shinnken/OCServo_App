import OCServo_App as ocapp


app = ocapp.App()
app.run()
print('Now we can continue running code while mainloop runs!')
# try:
#     app.go()
# except:
#     print('error')
for i in range(100000):
    print(i)