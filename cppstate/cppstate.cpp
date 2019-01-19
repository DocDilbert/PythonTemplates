//[[[cog import cog]]]
//[[[end]]]

//[[[cog
//  for table in ['customers', 'orders', 'suppliers']:
//      cog.outl("drop1 table %s;" % table)
//]]]
drop1 table customers;
drop1 table orders;
drop1 table suppliers;
//[[[end]]]