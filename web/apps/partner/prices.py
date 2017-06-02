from oscar.apps.partner.prices import FixedPrice


class CostBasedPrice(FixedPrice):

    def __init__(self, currency, cost_price):
        excl_tax = cost_price 
        tax = 0
        super(CostBasedPrice, self).__init__(currency, excl_tax, tax)
