class FullName(object):
    """
    Full name composite type
    """
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __composite_values__(self):
        return self.first_name, self.last_name

    def __repr__(self):
        if self.first_name and self.last_name:
            return ','.join([str(self.first_name), str(self.last_name)])
        elif self.first_name:
            return str(self.first_name)
        elif self.last_name:
            return str(self.last_name)
        else:
            return ''

    def __eq__(self, other):
        return isinstance(other, FullName) \
               and other.first_name == self.first_name \
               and other.last_name == self.last_name

    def __ne__(self, other):
        return not self.__eq__(other)


class FullAddress(object):
    """
    Full property address composite type
    """
    def __init__(self, address_line1, address_line2, address_city, address_state, address_zip):
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_city = address_city
        self.address_state = address_state
        self.address_zip = address_zip

    def __composite_values__(self):
        return self.address_line1, self.address_line2, self.address_city, self.address_state, self.address_zip

    def __repr__(self):
        full_address = ''

        address_line1 = self.address_line1 or ''
        address_line2 = self.address_line2 or ''
        address_city = self.address_city or ''
        address_state = self.address_state or ''
        address_zip = str(self.address_zip) if self.address_zip else ''

        if address_line1:
            full_address = f"{full_address} {address_line1}"
        if address_line2:
            full_address = f"{full_address} {address_line2}"
        if address_city:
            full_address = f"{full_address} {address_city}"
        if address_state:
            full_address = f"{full_address} {address_state}"
        if address_zip:
            full_address = f"{full_address} {address_zip}"

        return full_address.strip()

    def __eq__(self, other):
        return isinstance(other, FullAddress) and other.address_line1 == self.address_line1 \
               and other.address_line2 == self.address_line2 and other.address_city == self.address_city \
               and other.address_state == self.address_state and str(other.address_zip) == str(self.address_zip)

    def __ne__(self, other):
        return not self.__eq__(other)


class FullMailingAddress(object):
    """
    Full property address composite type
    """
    def __init__(self, address_line1, address_line2, address_line3):
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_line3 = address_line3

    def __composite_values__(self):
        return self.address_line1, self.address_line2, self.address_line3

    def __repr__(self):
        full_address = ''

        address_line1 = self.address_line1 or ''
        address_line2 = self.address_line2 or ''
        address_line3 = self.address_line3 or ''

        if address_line1:
            full_address = f"{full_address} {address_line1}"
        if address_line2:
            full_address = f"{full_address} {address_line2}"
        if address_line3:
            full_address = f"{full_address} {address_line3}"

        return full_address.strip()

    def __eq__(self, other):
        return isinstance(other, FullMailingAddress) and other.address_line1 == self.address_line1 \
               and other.address_line2 == self.address_line2 and other.address_line3 == self.address_line3

    def __ne__(self, other):
        return not self.__eq__(other)
