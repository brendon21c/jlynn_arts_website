from django.shortcuts import render, redirect, get_object_or_404, render_to_response


def order_summary(request):

    return render(request, 'receipt_details.html')
