from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split

from .models import Cards


def home(request):
    return render(request, 'home.html')


def View_Data(request):
    cards = Cards.objects.all()
    return render(request, 'View_Data.html', {
        'cards': cards,
    })


def Clean_Data(request, card_id):
    d = Proc_Data(card_id, 1)
    return render(request, 'Clean_Data.html', {
        'split': d,
    })


def Build_Model(request, card_id):
    return HttpResponse(f'<p>Build Model detail view with id {card_id}</p>')


def Reports(request, card_id):
    return HttpResponse(f'<p>Reports detail view with id {card_id}</p>')


class Data_Preprocessing:
    def __init__(self, content):
        self.content = content

    def Read_Data(self):
        C = self.content.split("_")
        C = (int)(C[1])
        if C == 1:
                d = Cards.objects.exclude(content_1=-1.0)
        elif C == 2:
                d = Cards.objects.exclude(content_2=-1.0)
        elif C == 3:
                d = Cards.objects.exclude(content_3=-1.0)
        elif C == 4:
                d = Cards.objects.exclude(content_4=-1.0)
        elif C == 5:
                d = Cards.objects.exclude(content_5=-1.0)
        elif C == 6:
                d = Cards.objects.exclude(content_6=-1.0)
        elif C == 7:
                d = Cards.objects.exclude(content_7=-1.0)
        elif C == 8:
                d = Cards.objects.exclude(content_8=-1.0)
        elif C == 9:
                d = Cards.objects.exclude(content_9=-1.0)
        data = pd.DataFrame.from_records(d.values_list('customer','content_1','content_2',
                                           'content_3','content_4','content_5',
                                           'content_6','content_7','content_8','content_9',
                                           'express_no_transactions',
                                           'express_total_spend', 'metro_no_transactions',
                                           'metro_total_spend', 'superstore_no_transactions',
                                           'superstore_total_spend', 'extra_no_transactions',
                                           'extra_total_spend','fandf_no_transactions',
                                           'fandf_total_spend', 'petrol_no_transactions',
                                           'petrol_total_spend','direct_no_transactions',
                                           'direct_total_spend','gender','affluency',
                                           'county'))
        return data

    def Clean_Data(self, data):
        C = self.content.split("_")
        C = (int)(C[1])
        C1 = data
        V = "content_"
        cards = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for x in cards:
            if x == C:
                continue
            C1 = C1.drop([V + str(x)], axis=1)

        return C1

    def Missing_Values(self, C1):
        total = C1.isnull().sum().sort_values(ascending=False)
        percent = (C1.isnull().sum() / C1.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])

    def Convert_Cat(self, C1):
        C1 = C1.astype({self.content: int})
        C1 = pd.get_dummies(C1, columns=["gender"], prefix=["Gender"])
        C1["affluency"] = C1["affluency"].astype('category')
        C1["affluency_cat"] = C1["affluency"].cat.codes
        C1 = C1.drop(["affluency"], axis=1)
        C1["county"] = C1["county"].astype('category')
        C1["county_cat"] = C1["county"].cat.codes
        C1 = C1.drop(["county"], axis=1)

        return C1

    def Output_Var(self, C1):
        C1_Y = C1[self.content]

        return C1_Y

    def Input_Var(self, C1):
        C1_X = C1.drop([self.content, "customer.id"], axis=1)

        return C1_X

    def Normalise(self, C1_X):
        C1_X = ((C1_X - C1_X.min()) / (C1_X.max() - C1_X.min()))

        return C1_X

    def Split(self, C1_X, C1_Y, select):
        X_train, X_test, y_train, y_test = train_test_split(C1_X, C1_Y, test_size=0.2)
        if select == 1:
            return X_train
        elif select == 2:
            return X_test
        elif select == 3:
            return y_train
        else:
            return y_test


def Proc_Data(c, s):
    x = Data_Preprocessing(c)
    d = x.Read_Data()
    r = x.Clean_Data(d)
    m = x.Missing_Values(r)
    cc = x.Convert_Cat(r)
    o = x.Output_Var(cc)
    i = x.Input_Var(cc)
    n = x.Normalise(i)
    return x.Split(n, o, s)
