from django.shortcuts import render

# Create your views here.



def basket_summary(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    return render(request, "store/basket/summary.html")