



class Basket():
    """_Provide default behaviours
    """
    def __init__(self, request):
        #store and remember user data with sessions
        self.session = request.session
        basket = self.session.get("skey")
        if "skey" not in request.session:
            basket = self.session["skey"] = {"Number": 1231231}
        self.basket = basket