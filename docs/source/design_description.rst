.. _design_description:

Design Description
==================

This is my (eragnms) interpretation of how the design of the Visma package is done.

Marshmallow
-----------

In the model classes there are a Meta class. In the context of a class defining a
Marshmallow schema, the Meta class is used to provide meta-information about the
schema itself. This meta-information typically includes settings and options that
affect how the schema behaves or how it's used.

In marshmallow "load_only" is a list of field names that should be used for deserialization
only. While "dump_only" is a list of field names that should be used for serialization only.

Serialization: This process involves converting complex Python objects (such as instances of
classes) into a format that is suitable for storage or transmission, such as JSON or
dictionaries. Serialization is typically used when you want to represent your data in a portable and
easily consumable format. In Marshmallow, serialization is often performed using schemas, which
define how objects should be serialized.

Deserialization: This process is the reverse of serialization. It involves taking data in a
serialized format (such as JSON or dictionaries) and converting it back into complex Python
objects. Deserialization is commonly used when you receive data from an external source (such as an
API request or a database query) and need to convert it into objects that your application can work
with. In Marshmallow, deserialization is also done using schemas, which define how incoming data
should be converted into objects.

Serialization is performed using the dump() method of the schema, which converts the Python object
data into a dictionary.  Deserialization is performed using the load() method of the schema, which
converts the dictionary data into a Python object.

dump_only=True: This option tells Marshmallow that the field should only be included when
serializing (or "dumping") data. It will be ignored during deserialization (loading).

load_only=True: This option tells Marshmallow that the field should only be included when
deserializing (or "loading") data. It will be ignored during serialization (dumping

If a field is defined as optional in the Swagger API, you can represent that in the final Python
Marshmallow model by allowing None values for that field. In Marshmallow, you can achieve this using
the allow_none=True parameter when defining the field.

Use case create customer
------------------------

As a way to try to understand the design the use case of creating a customer using
the class Customer is described below.

When instantiating an object of the class Customer, the Customer class in models.py
is executed. In that class a lot of attributes are defined. Each attribute is given
a marshmallow field.
