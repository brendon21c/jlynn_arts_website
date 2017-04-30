from django.shortcuts import render, redirect, get_object_or_404, render_to_response


def order_receipt(request):

    return render(request, 'order_receipt.html')
