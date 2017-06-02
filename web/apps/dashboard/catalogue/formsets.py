from oscar.apps.dashboard.catalogue.formsets import StockRecordFormSet as OscarStockRecordFormSet


# we remove the currency and price fields as we will only use the cost_price field
class StockRecordFormSet(OscarStockRecordFormSet):

    def _construct_form(self, i, **kwargs):
        form = super(StockRecordFormSet, self)._construct_form(i, **kwargs)
        del form.fields['price_currency']
        del form.fields['price_excl_tax']
        # del form.fields['price_retail']
        return form