# # Error Handle Function
# def handle_response(response):
#     try:  # Check if the response is a correct json file
#         response_data = response.json()
#         if "IsSuccess" in response_data.keys() and response_data["IsSuccess"] == True:  # Suc
#             return
#         elif "ValidationErrors" in response_data.keys() and response_data["ValidationErrors"] != None:
#             error = []
#             for i in range(len(response_data["ValidationErrors"])):
#                 v_error = [response_data["ValidationErrors"][i]["Name"],
#                            response_data["ValidationErrors"][i]["Error"]]
#                 error.append(v_error)
#         elif "ErrorMessage" in response_data.keys() and response_data["ErrorMessage"] != None:
#             error = response_data["ErrorMessage"]
#         elif "Message" in response_data.keys() and response_data["Message"] != None:
#             error = response_data["Message"]
#     except:
#         if response.text == "":  # In case of empty response
#             error = "API key or API URL is not correct"
#         else:
#             error = "An Error has occuered. API response: ", response.text
#     print(error)
#     exit()
#
#
# # Call API Function
# def call_api(api_url, api_key, request_data, request_type="POST"):
#     request_data = json.dumps(request_data)
#     headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}
#     try:
#         response = requests.request(request_type, api_url, data=request_data, headers=headers)
#     except:
#         print("An Error has occurred. Kindly check your API URL")
#         exit()
#     handle_response(response)
#     return response
#
#
# # Initiate Payment endpoint Function
# def initiate_payment(initiatepay_request):
#     api_url = base_url + "/v2/InitiatePayment"
#     initiatepay_response = call_api(api_url, api_key, initiatepay_request).json()
#     payment_methods = initiatepay_response["Data"]["PaymentMethods"]
#     # Initiate Payment output if successful
#     # print("Payment Methods: ", payment_methods)
#     return payment_methods
#
#
# # Execute Payment endpoint Function
# def execute_payment(executepay_request):
#     api_url = base_url + "/v2/ExecutePayment"
#     executepay_response = call_api(api_url, api_key, executepay_request).json()
#     invoice_id = executepay_response["Data"]["InvoiceId"]
#     invoice_url = executepay_response["Data"]["PaymentURL"]
#     # Execute Payment output if successful
#     # print("InvoiceId: ", invoice_id,
#     #      "\nInvoiceURL: ", invoice_url)
#     return invoice_id, invoice_url
#
#
# # Direct Payment endpoint Function
# # The payment link from execute payment is used as the API for direct payment
# def direct_payment(directpay_request, invoice_url):
#     directpay_response = call_api(invoice_url, api_key, directpay_request).json()
#     directpay_status = directpay_response["Data"]
#     # Direct Payment output if successful
#     print("Direct Payment Status: ", directpay_status)
#     return directpay_status
#
#
# # Cancel Token
# def cancel_token(token):
#     api_url = base_url + "/v2/CancelToken?token=" + token
#     cancel_token_response = call_api(api_url, api_key, initiatepay_request).json()
#     print(cancel_token_response)
#     return cancel_token_response
#
#
# # Test Environment
# base_url = "https://apitest.myfatoorah.com"
# api_key = "rLtt6JWvbUHDDhsZnfpAhpYk4dxYDQkbcPTyGaKp2TYqQgG7FGZ5Th_WD53Oq8Ebz6A53njUoo1w3pjU1D4vs_ZMqFiz_j0urb_BH9Oq9VZoKFoJEDAbRZepGcQanImyYrry7Kt6MnMdgfG5jn4HngWoRdKduNNyP4kzcp3mRv7x00ahkm9LAK7ZRieg7k1PDAnBIOG3EyVSJ5kK4WLMvYr7sCwHbHcu4A5WwelxYK0GMJy37bNAarSJDFQsJ2ZvJjvMDmfWwDVFEVe_5tOomfVNt6bOg9mexbGjMrnHBnKnZR1vQbBtQieDlQepzTZMuQrSuKn-t5XZM7V6fCW7oP-uXGX-sMOajeX65JOf6XVpk29DP6ro8WTAflCDANC193yof8-f5_EYY-3hXhJj7RBXmizDpneEQDSaSz5sFk0sV5qPcARJ9zGG73vuGFyenjPPmtDtXtpx35A-BVcOSBYVIWe9kndG3nclfefjKEuZ3m4jL9Gg1h2JBvmXSMYiZtp9MR5I6pvbvylU_PP5xJFSjVTIz7IQSjcVGO41npnwIxRXNRxFOdIUHn0tjQ-7LwvEcTXyPsHXcMD8WtgBh-wxR8aKX7WPSsT1O8d8reb2aR7K3rkV3K82K_0OgawImEpwSvp9MNKynEAJQS6ZHe_J_l77652xwPNxMRTMASk1ZsJL"
# # Test token value to be placed here: https:#myfatoorah.readme.io/docs/test-token
#
# # Live Environment
# # base_url = "https:#api.myfatoorah.com"
# # api_key = "mytokenvalue" #Live token value to be placed here: https:#myfatoorah.readme.io/docs/live-token
#
# # Initaite Payment request data
# initiatepay_request = {
#     "InvoiceAmount": 100,
#     "CurrencyIso": "KWD"
# }
#
# # Getting the value of payment Method Id
# payment_method = initiate_payment(initiatepay_request)
#
# payment_method_list = []
# for item in range(len(payment_method)):
#     if payment_method[item]["IsDirectPayment"] == True:
#         y = [payment_method[item]["PaymentMethodEn"], payment_method[item]["PaymentMethodId"]]
#         payment_method_list.append(y)
# print(payment_method_list)
# while True:
#     payment_method_id = input("Kindly enter the number equivalent to the required payment method: ")
#     try:
#         if int(payment_method_id) in [el[1] for el in payment_method_list]:
#             break
#         else:
#             print("Kindly enter a correct direct payment method id")
#     except:
#         print("The input must be a number")
#
# # Execute Payment Request
# executepay_request = {
#     "paymentMethodId": payment_method_id,
#     "InvoiceValue": 50,
#     "CallBackUrl": "https://example.com/callback.php",
#     "ErrorUrl": "https://example.com/callback.php",
#     # Fill optional data
#     # "CustomerName"       : "fname lname",
#     # "DisplayCurrencyIso" : "KWD",
#     # "MobileCountryCode"  : "+965",
#     # "CustomerMobile"     : "1234567890",
#     # "CustomerEmail"      : "email@example.com",
#     # "Language"           : "en", #or "ar"
#     # "CustomerReference"  : "orderId",
#     # "CustomerCivilId"    : "CivilId",
#     # "UserDefinedField"   : "This could be string, number, or array",
#     # "ExpiryDate"         : "", # The Invoice expires after 3 days by default. Use "Y-m-d\TH:i:s" format in the "Asia/Kuwait" time zone.
#     # "SourceInfo"         : "Pure PHP", #For example: (Laravel/Yii API Ver2.0 integration)
#     # "CustomerAddress"    : $customerAddress,
#     # "InvoiceItems"       : $invoiceItems,
# }
#
# # Execute payment t get Invoice Id and Invoice URL
# invoice_id, invoice_url = execute_payment(executepay_request)
#
# # Required Data for direct Payment
# directpay_request = {
#     "PaymentType": "card",
#     "Bypass3DS": False,
#     "SaveToken": True,
#     "Token": "string",
#     "Card": {
#         "Number": "5123450000000008",
#         "ExpiryMonth": "05",
#         "ExpiryYear": "21",
#         "SecurityCode": "100",
#         "CardHolderName": "fname lname"
#     }
# }
#
# # Test Card Data for Visa/Master
# # {
# # "PaymentType": "card",
# # "Bypass3DS": False,
# # "SaveToken": False,
# # "Card": {
# #       "Number": "5453010000095539",
# #       "ExpiryMonth": "12",
# #       "ExpiryYear": "25",
# #       "SecurityCode": "300",
# #      }
# #      }
#
# response_directpay = direct_payment(directpay_request, invoice_url)
#
# if directpay_request["SaveToken"] == True:
#     saved_token = response_directpay["Token"]
#
#     directpay_request2 = {
#         "PaymentType": "token",
#         "Bypass3DS": False,
#         "Token": saved_token,
#         "Card": {
#             "SecurityCode": "100",
#             # "CardHolderName": "fname lname"
#         }
#     }
#     direct_payment(directpay_request2, invoice_url)
#
# cancel_token(saved_token)
