import pytest

from visma.api import VismaAPIException, VismaClientException
from visma.models import Customer, TermsOfPayment, CustomerInvoiceDraft


class TestCRUDCustomer:
    customer_number = 'test_customer'

    customer_id = None

    def test_create_customer(self):
        """
        Create a customer
        """

        print('Creating customer')
        customer = Customer(
            invoice_city='Helsingborg',
            invoice_postal_code='25234',
            name='TestCustomer AB',
            terms_of_payment_id='8f9a8f7b-5ea9-44c6-9725-9b8a1addb036',
            is_private_person=False,
            is_active=True)
        customer.save()

        self.customer_id = customer.id
        print(f'Created customer with id {self.customer_id}')

    def test_get_customer(self):
        """
        Retrieve a Customer
        """
        customer = Customer(
            invoice_city='Helsingborg',
            invoice_postal_code='25234',
            name='TestCustomer AB',
            terms_of_payment_id='8f9a8f7b-5ea9-44c6-9725-9b8a1addb036',
            is_private_person=False,
            is_active=True)
        customer.save()

        self.customer_id = customer.id
        customer = Customer.objects.get(self.customer_id)
        assert customer.name == 'TestCustomer AB'

    def test_update_customer(self):
        customer = Customer.objects.all()[0]
        customer.name = 'Changed Name TestCustomer AB'
        customer.save()
        customer_id = customer.id

        customer_again = Customer.objects.get(customer_id)
        assert customer_again.name == 'Changed Name TestCustomer AB'

    def test_delete_customer(self):
        """
        Delete a customer
        """
        customer = Customer(
            invoice_city='Helsingborg',
            invoice_postal_code='25234',
            name='TestCustomer AB',
            terms_of_payment_id='8f9a8f7b-5ea9-44c6-9725-9b8a1addb036',
            is_private_person=False,
            is_active=True)
        customer.save()

        self.customer_id = customer.id
        print(f'Deleting customer {self.customer_id}')
        Customer.objects.delete(self.customer_id)

    def test_delete_none_existent_customer(self):
        """
        If we delete customer that doesn't exist we should get an error.
        # TODO: should we look for internal error code of repsonse?
        """
        non_existent_id = 'e530798a-5821-4112-bc84-d2bc725772ee'
        with pytest.raises(VismaAPIException):
            Customer.objects.delete(non_existent_id)


class TestTermsOfPayment:

    def test_get_termsofpayment(self):
        top = TermsOfPayment.objects.all()
        assert len(top) > 0

    def test_no_update_allowed(self):
        with pytest.raises(VismaClientException):
            top = TermsOfPayment.objects.all()[0]
            top.number_of_days = 20
            top.save()


class TestCustomerInvoiceDraft:

    @pytest.fixture()
    def customer(self):
        customer = Customer(
            invoice_city='Helsingborg',
            invoice_postal_code='25234',
            name='TestCustomer AB',
            terms_of_payment_id='8f9a8f7b-5ea9-44c6-9725-9b8a1addb036',
            is_private_person=False,
            is_active=True)
        customer.save()
        yield customer
        customer.delete()

    def test_get_all_customer_invoice_drafts(self):
        """should not raise exception"""
        invoices = CustomerInvoiceDraft.objects.all()

    def test_create_customer_invoice_draft(self, customer):
        invoice = CustomerInvoiceDraft(customer_id=customer.id,
                                       invoice_customer_name='test_name',
                                       invoice_postal_code='25269',
                                       invoice_city='Helsingborg',
                                       customer_is_private_person=False)

        invoice.save()

        assert invoice.id is not None
