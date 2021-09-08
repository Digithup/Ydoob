import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites import requests
from django.shortcuts import render
from django.views import View

from DNigne import settings
from sales.models.orders import Order


class PaymentMyFatoorah(LoginRequiredMixin, View):
    '''
    Handle Stripe payment (Stripe API)
    '''

    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False,)
        context = {
            'STRIPE_PUBLIC_KEY': settings.MyFatoorah_api_key,
            'order': order
        }
        return render(self.request, 'payments/PaymentMyFatoorah.html', context)

    # Call API Function
    def call_api(api_url, api_key, request_data, request_type="POST"):
        request_data = json.dumps(request_data)
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}
        try:
            response = requests.request(request_type, api_url, data=request_data, headers=headers)
        except:
            print("An Error has occurred. Kindly check your API URL")
            exit()
        handle_response(response)
        return response





# Error Handle Function
def handle_response(response):
    try:     # Check if the response is a correct json file
        response_data = response.json()
        if "IsSuccess" in response_data.keys() and response_data["IsSuccess"] == True: #Suc
            return
        elif "ValidationErrors" in response_data.keys() and response_data["ValidationErrors"] != None:
            error = []
            for i in range(len(response_data["ValidationErrors"])):
                v_error = [response_data["ValidationErrors"][i]["Name"], response_data["ValidationErrors"][i]["Error"]]
                error.append(v_error)
        elif "ErrorMessage" in response_data.keys() and response_data["ErrorMessage"] != None:
            error = response_data["ErrorMessage"]
        elif "Message" in response_data.keys() and response_data["Message"] != None:
            error = response_data["Message"]
    except:
        if response.text == "": # In case of empty response
            error = "API key or API URL is not correct"
        else:
            error = "An Error has occuered. API response: ", response.text
    print(error)
    exit()