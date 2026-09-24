import pytest

class Discount():
    def __init__(self, price, age):
        self.price = price
        self.age = age

    def calculate_discount(self):
        if self.price <= 0:
            raise ValueError("Cena nie może być mniejsza lub równa zero!")
        if self.age <= 17:
            return self.price
        if self.age >= 18 and self.age <=64 :
            return self.price * 0.90
        if self.age >= 65:
            return self.price * 0.80


@pytest.fixture()
def person(request):
    price, age = request.param
    return Discount(price, age)

@pytest.mark.parametrize("person,expected",[
    ((100,17),100),
    ((100,64),90),
    ((100,65),80),
    ((100,66),80),
    ((1,30),0.90),
    ((100,18),90),
],indirect=["person"])
def test_calculate_discount(person,expected):
    assert person.calculate_discount() == expected

@pytest.mark.parametrize("person,expected",[
    ((0,10),ValueError),
     ((-1,62),ValueError),
],indirect=["person"])

def test_price_error(person,expected):
    with pytest.raises(expected):
        person.calculate_discount()
